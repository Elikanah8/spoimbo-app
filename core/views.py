from django.shortcuts import render, redirect
from .models import Content, UserProfile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import datetime 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def landing(request):
    return render(request, 'landing.html')
import requests # Make sure to import this at the top

@login_required
def home(request):
    # 1. Get local database songs (Your uploaded ones)
    db_songs = Content.objects.filter(content_type='music')
    db_podcasts = Content.objects.filter(content_type='podcast')
    
    # 2. Check if user is searching
    query = request.GET.get('q')
    api_songs = []
    
    if query:
        # Search Deezer API
        url = f"https://api.deezer.com/search?q={query}"
        response = requests.get(url)
        data = response.json()
        
        # Process Deezer Results to match our format
        if 'data' in data:
            for item in data['data']:
                song_data = {
                    'title': item['title'],
                    'artist': item['artist']['name'],
                    'cover_image': item['album']['cover_medium'], # URL of image
                    'audio_file': item['preview'], # URL of mp3 preview
                    'is_api': True # Flag to tell template this is from internet
                }
                api_songs.append(song_data)

    # 3. Check Subscription (Same as before)
    try:
        profile = request.user.userprofile
        is_premium = profile.is_premium()
        is_registered = profile.is_paid_registration
    except:
        is_premium = False
        is_registered = False

    context = {
        'songs': db_songs,
        'podcasts': db_podcasts,
        'api_songs': api_songs, # New list from Deezer
        'is_premium': is_premium,
        'is_registered': is_registered,
        'search_query': query
    }
    return render(request, 'home.html', context)



# SIMULATED M-PESA PAYMENT (Since we don't have live API keys yet)
@login_required
def initiate_mpesa(request, amount):
    # In a real app, you would use requests to hit the Safaricom Daraja API here
    # Amount would be 10 (registration) or 30 (weekly sub)
    
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if int(amount) == 10:
        user_profile.is_paid_registration = True
        user_profile.save()
        return JsonResponse({'message': 'Registration Fee Paid! Welcome to Spoimbo.'})
    
    elif int(amount) == 30:
        # Add 7 days to subscription
        user_profile.subscription_expiry = datetime.datetime.now() + datetime.timedelta(days=7)
        user_profile.save()
        return JsonResponse({'message': 'Weekly Subscription Active! You can now skip songs.'})
        
    return JsonResponse({'message': 'Error'})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# In core/views.py
from django.shortcuts import get_object_or_404 # Add this import at the top if missing

@login_required
def toggle_favorite(request, song_id):
    song = get_object_or_404(Content, id=song_id)
    profile = request.user.userprofile
    
    if song in profile.favorites.all():
        profile.favorites.remove(song)
        liked = False
    else:
        profile.favorites.add(song)
        liked = True
        
    return JsonResponse({'liked': liked})

@login_required
def my_library(request):
    profile = request.user.userprofile
    # Get user's favorite songs
    my_songs = profile.favorites.filter(content_type='music')
    my_podcasts = profile.favorites.filter(content_type='podcast')
    
    return render(request, 'library.html', {
        'songs': my_songs, 
        'podcasts': my_podcasts
    })