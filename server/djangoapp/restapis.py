import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

def get_request(url, api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    
    try:
        if api_key:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], _id=dealer_doc["_id"], _rev=dealer_doc["_rev"],
                                   state=dealer_doc["state"])
            results.append(dealer_obj)

    return results


def get_dealer_reviews_from_cf(url, dealer_id, **kwargs):
    results = []
    json_result = get_request(url, id=dealer_id, **kwargs)
    
    if json_result:
        reviews = json_result
        for review in reviews:
            dealer_doc = review
            sentiment = analyze_review_sentiments(dealer_doc["review"])
            review_obj = DealerReview(dealership=dealer_doc["dealership"], name=dealer_doc["name"], purchase=dealer_doc["purchase"],
                                   review=dealer_doc["review"], purchase_date=dealer_doc["purchase_date"], car_make=dealer_doc["car_make"],
                                   car_model=dealer_doc["car_model"], car_year=dealer_doc["car_year"], sentiment=sentiment, id=dealer_doc["id"]
                                )
            results.append(review_obj)

    return results


def analyze_review_sentiments(dealerreview):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/f12c0902-455f-4c31-92fa-de6dce857143"
    api_key = "sSFTUPEM7iqJ4TAqvN8HY3xqyXLumFLkuHCpO112tecc"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01', authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    
    response = natural_language_understanding.analyze(
        text=dealerreview + "helo helo helo. this is a comment",
        features=Features(sentiment=SentimentOptions(targets=[dealerreview + "helo helo helo. this is a comment"]))
    ).get_result()
    
    
    label = response['sentiment']['document']['label']

    return label


