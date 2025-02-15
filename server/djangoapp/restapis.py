import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


#`get_request` to make HTTP GET requests
def get_request(url, api_key=None, **kwargs):
    # print(kwargs)
    print("GET from {} ".format(url))
    try:
        # # Call get method of requests library with URL and parameters
        if api_key:
            response = requests.get(url, params=kwargs['params_dict'], headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey',api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs,)
            
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        # json_data = json.dumps(response.text)
        return json_data
    except:
        print("Network exception occurred")


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    response = requests.post(url, params=kwargs, json=json_payload)
    return json.loads(response.text)


# get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    if kwargs.get('state'):
        state = kwargs['state']
        json_result = get_request(url, state=state)
        if json_result:
            dealers = json_result['result']
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                    id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                    short_name=dealer["short_name"],
                                    state=dealer["state"], zip=dealer["zip"])
            results.append(dealer_obj)
    else:
        json_result = get_request(url)
        if json_result:
            dealers = json_result['result']['rows']
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# def get_dealer_by_id( kwargs):
#     url = 
#     response = get_request(url, kwargs)
#     print(response)


# get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, *args):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealership=args[0])
    if json_result:
        if json_result.get('body', False):
            review_list = json_result['body']
            for item in review_list:
                if item['purchase'] == True: 
                    print('with')
                    review_obj = DealerReview(
                        dealership = item["dealership"],
                        name = item["name"],
                        purchase = item["purchase"],
                        review = item["review"],
                        purchase_date = item["purchase_date"],
                        car_make = item["car_make"],
                        car_model = item["car_model"],
                        car_year = item["car_year"],
                        sentiment = analyze_review_sentiments(item['review']),
                        id = item["id"])
                    results.append(review_obj)

                if item['purchase'] == False:
                    print('without')
                    review_obj = DealerReview(
                        dealership = item["dealership"],
                        name = item["name"],
                        purchase = item["purchase"],
                        review = item["review"],
                        purchase_date = None,
                        car_make = None,
                        car_model = None,
                        car_year = None,
                        sentiment = analyze_review_sentiments(item['review']),
                        id = item["id"])
                    # results.append(review_obj.review)
                    results.append(review_obj)
        else:
            return "No reviews for this dealership yet."
    # print(results)
    return results

# `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/ee1b2a37-53f1-4a16-a521-12cb78fe725d/v1/analyze"
    api_key = "WnfKeuh1ZxkR0JdxI5aHN30r6tEm-eb0AkZw7y2gwaZl"
    params_dict = {'text': text, 'version': '2022-04-07', 'features': 'sentiment', "return_analyzed_text": True}
    response = get_request(url, api_key, params_dict=params_dict)
    sentiment = response['sentiment']['document']['label']
    return sentiment