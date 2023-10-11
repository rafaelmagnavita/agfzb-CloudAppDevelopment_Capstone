from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, DealerReview, DealerReviewForm
from .restapis import get_dealers_from_cf,get_request, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, './about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, './contact.html', context)

def login_request(request):
    context = {}
    if request.method == "GET":
        return render(request, './user_login.html', context)

    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, './user_login.html', context)
    else:
        return render(request, './user_login.html', context)


def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, './registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, './registration.html', context)


def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://rafaelmagnav-3000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Return a list of dealer short name
        context['dealerships'] = dealerships
        return render(request, 'djangoapp/index.html', context)
        # return HttpResponse(dealer_names)


def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = f"https://rafaelmagnav-5000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context['dealer_reviews'] = dealer_reviews
        url2 = "https://rafaelmagnav-3000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        dealerships = get_dealers_from_cf(url2)
        
        dealership_name = next((dealer.full_name for dealer in dealerships if dealer.id == dealer_id), None)

        context['dealership_name'] = dealership_name
        return render(request, 'djangoapp/dealer_details.html', context)

def add_review(request, dealer_id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    
    dealer = CarDealer.objects.get(id=dealer_id)


    if request.method == 'GET':
        # Render the form for a GET request
        form = DealerReviewForm()  # Use your actual form class here
        return render(request, "djangoapp:add_review", {'form': form, 'dealer': dealer})

    elif request.method == 'POST':
        car_make = request.POST.get('car_make')  
        car_model = request.POST.get('car_model')
        car_year = request.POST.get('car_year')
        sentiment = None
        id = request.POST.get('id')
        name = request.POST.get('name')
        dealership = request.POST.get('dealership')
        review_text = request.POST.get('review')
        purchase = request.POST.get('purchase')
        purchase_date = request.POST.get('purchase_date')

        # Format time and purchase_date
        review_time = datetime.utcnow().isoformat()
        purchase_year = datetime.strptime(purchase, '%Y-%m-%d').strftime("%Y")

        # Create a dictionary object called review
        review_data = {
            'car_make': car_make,
            'car_model': car_model,
            'car_year': car_year,
            'sentiment': sentiment,
            'id': id,
            'name': name,
            'dealership': dealership,
            'review': review_text,
            'purchase': purchase,
            'purchase_date': purchase_date,
            'review_time': review_time,
            'purchase_year': purchase_year,
        }

        json_payload = {'review': review_data}
        post_url = 'https://rafaelmagnav-5000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review'
        response = post_request(post_url, json_payload, dealerId=dealer_id)

        # Redirect user to the dealer details page
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)