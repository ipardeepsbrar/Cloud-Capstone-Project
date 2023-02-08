from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
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
        return render(request, 'djangoapp/about.html', context)
# ...


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
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
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)
# ...

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')
# ...

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
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
            user = User.objects.create_user(username=username, first_name=first_name,
                                             last_name=last_name, password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)

def get_dealerships(request):
    context = {}
    if request.method == "GET":
        if request.GET.get('state'):
            url = 'https://us-east.functions.appdomain.cloud/api/v1/web/515d3549-824b-4fa0-be7c-973b4ca817fe/dealership/state-dealers.json'
            dealerships = get_dealers_from_cf(url, state=request.GET.get('state'))
        else:
            url = 'https://us-east.functions.appdomain.cloud/api/v1/web/515d3549-824b-4fa0-be7c-973b4ca817fe/dealership/get-dealership.json'
            dealerships = get_dealers_from_cf(url)
            # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        context['dealerships'] = dealerships
        # return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)
       


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == 'GET':
        url = 'https://us-east.functions.appdomain.cloud/api/v1/web/515d3549-824b-4fa0-be7c-973b4ca817fe/dealership/get-reviews.json'
        
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        if type(reviews) is list:
            context['review_list'] = reviews
            print(context)
            # print(context['review_list'][0].sentiment)
            return render(request, 'djangoapp/dealer_details.html', context)
         
        else:
            return HttpResponse('Error : ' + reviews)
        
# ...
# Create a `add_review` view to submit a review
def add_review(request):
    dealerId=request.GET.get('dealer_id')
    authenticated = request.user.is_authenticated
    if authenticated:
        json_payload = {
                    "review": 
                        {
                            "id": 8,
                            "name": "Pardeep",
                            "dealership": 16,
                            "review": "Just a test by pardeep!",
                            "purchase": True,
                            "purchase_date": "10/16/2021",
                            "car_make": "Mercedes",
                            "car_model": "C340",
                            "car_year": 2020
                        }
                    }
        url = 'https://us-east.functions.appdomain.cloud/api/v1/web/515d3549-824b-4fa0-be7c-973b4ca817fe/dealership/review-post.json'
        result = post_request(url, json_payload=json_payload, dealer_id=dealerId)
        return HttpResponse(json.dumps(result))
# ...

