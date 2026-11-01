import json
from urllib.parse import quote
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from .models import CarModel
from .restapis import get_request, post_review, analyze_review_sentiments

@require_POST
def login_user(request):
    try:
        data = json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    user = authenticate(request, username=data.get('userName'), password=data.get('password'))
    if user is None:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    login(request, user)
    return JsonResponse({'status': 'Authenticated', 'userName': user.username})

@require_POST
def logout_request(request):
    logout(request)
    return JsonResponse({'status': 200})

@require_POST
def registration(request):
    try:
        data = json.loads(request.body)
        username = data.get('userName', '').strip()
        if not username or len(username) > 150:
            raise ValueError('A username of at most 150 characters is required')
        user = User(username=username, first_name=data.get('firstName', ''), last_name=data.get('lastName', ''), email=data.get('email', ''))
        validate_password(data.get('password', ''), user)
        user.set_password(data['password'])
        user.save()
    except (ValueError, KeyError, ValidationError, IntegrityError) as error:
        return JsonResponse({'error': str(error)}, status=400)
    login(request, user)
    return JsonResponse({'status': 200, 'userName': user.username})

def api_result(key, endpoint):
    try:
        return JsonResponse({'status': 200, key: get_request(endpoint)})
    except requests.RequestException:
        return JsonResponse({'error': 'The dealership service is unavailable'}, status=503)

@require_GET
def get_dealerships(request, state='All'):
    endpoint = 'fetchDealers' if state == 'All' else f'fetchDealers/{quote(state, safe="")}'
    return api_result('dealers', endpoint)

@require_GET
def get_dealer_details(request, dealer_id):
    return api_result('dealer', f'fetchDealer/{dealer_id}')

@require_GET
def get_dealer_reviews(request, dealer_id):
    try:
        reviews = get_request(f'fetchReviews/dealer/{dealer_id}')
        for review in reviews:
            review['sentiment'] = analyze_review_sentiments(review['review'])
        return JsonResponse({'status': 200, 'reviews': reviews})
    except requests.RequestException:
        return JsonResponse({'error': 'The review service is unavailable'}, status=503)

@require_GET
def get_cars(request):
    cars = [{'CarMake': model.car_make.name, 'CarModel': model.name, 'CarYear': model.year} for model in CarModel.objects.select_related('car_make').all()]
    return JsonResponse({'CarModels': cars})

@require_POST
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Please log in'}, status=401)
    try:
        data = json.loads(request.body)
        if not data.get('review', '').strip():
            raise ValueError('Review text is required')
        data['dealership'] = int(data['dealership'])
        data['car_year'] = int(data['car_year'])
        if not 2015 <= data['car_year'] <= 2023:
            raise ValueError('Year must be between 2015 and 2023')
        data['name'] = request.user.get_full_name() or request.user.username
        result = post_review(data)
        return JsonResponse({'status': 200, 'review': result})
    except (ValueError, KeyError):
        return JsonResponse({'error': 'Invalid review details'}, status=400)
    except requests.RequestException:
        return JsonResponse({'error': 'The review service is unavailable'}, status=503)
