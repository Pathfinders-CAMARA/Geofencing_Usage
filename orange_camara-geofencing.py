import requests
import json
'''
https://developer.orange.com/apis/camara-sandbox-geofencing-orange-lab/getting-started
https://developer.orange.com/apis/camara-sandbox-geofencing-orange-lab/api-reference?view=rapidoc#delete-/subscriptions/-subscriptionId-
'''

def get_access_token(client_id, client_secret, scope):
    token_url = 'https://api.orange.com/oauth/v3/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope
    }
    response = requests.post(token_url, data=payload)
    response_data = response.json()
    access_token = response_data.get('access_token')
    return response_data['access_token']


def geofencing_post_entered(access_token, phone_number, latitude, longitude, radius):
    '''
      Create a subscription for a device to receive notifications when a device enters a specified area
    '''
    url = f"{API_URL}/simulated"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'x-correlator': 'area1_50'
    }
    data = {
        "protocol": "HTTP",
        "sink": SINK,
        "types": [
            "org.camaraproject.geofencing-subscriptions.v0.area-entered"
        ],
        "config": {
            "subscriptionDetail": {
                "device": {
                    "phoneNumber": phone_number
                },
                "area": {
                    "areaType": "CIRCLE",
                    "center": {
                        "latitude": latitude,
                        "longitude": longitude
                    },
                    "radius": radius
                }
            },
            "initialEvent": True,
            "subscriptionMaxEvents": 10,
            "subscriptionExpireTime": "2025-04-22T05:40:58.47Z"
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()


def geofencing_post_left(access_token, phone_number, latitude, longitude, radius):
    '''
      Create a subscription for a device to receive notifications when a device exits a specified area
    '''
    url = f"{API_URL}/simulated"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'x-correlator': 'geo_correlator'
    }
    data = {
        "protocol": "HTTP",
        "sink": SINK,
        "types": [
            "org.camaraproject.geofencing-subscriptions.v0.area-left"
        ],
        "config": {
            "subscriptionDetail": {
                "device": {
                    "phoneNumber": phone_number
                },
                "area": {
                    "areaType": "CIRCLE",
                    "center": {
                        "latitude": latitude,
                        "longitude": longitude
                    },
                    "radius": radius
                }
            },
            "initialEvent": True,
            "subscriptionMaxEvents": 10,
            "subscriptionExpireTime": "2025-04-22T05:40:58.47Z"
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()


def geofencing_get(access_token):
    '''
    Retrieve a list of geofencing event subscription(s)
    '''
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'x-correlator': 'geo_correlator'
    }
    response = requests.get(API_URL, headers=headers)
    return response.json()


def geofencing_get_id(access_token, subscription_id):
    '''
    Retrieve geofencing subscription information for a given subscription ID.
    '''
    url = f"{API_URL}/{subscription_id}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'x-correlator': 'geo_correlator'
    }
    response = requests.get(url, headers=headers)
    return response.json()


def geofencing_delete_id(access_token, subscription_id):
    """
    Usuwa geofencing subscription o danym ID.
    """
    url = f"{API_URL}/{subscription_id}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'x-correlator': 'geo_correlator'
    }
    response = requests.delete(url, headers=headers)
    if response.status_code in (202, 204):
        return {
            "status_code": response.status_code,
            "message": "Subscription deleted (no JSON in response)."
        }

    try:
        return response.json()
    except ValueError:
        return {
            "status_code": response.status_code,
            "raw_response": response.text
        }


if __name__ == "__main__":

    # Replace 'your_client_id' and 'your_client_secret' with actual values
    client_id = 'YY'
    client_secret = 'XX'
    scope = ""

    #######################################################################################
    API_URL = 'https://api.orange.com/camara/geofencing/orange-lab/v0/subscriptions'

    #######################################################################################
    SINK = 'https://webhook.site/d8788cf3-53ae-403f-a950-993645caaa39'

    #######################################################################################
    '''
    *-*-*-*-*-*-*-*-*-**-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**-*-*-*-*-*-*-*-*-*
        All subscriptions created from the requesting client_id are provided
    *-*-*-*-*-*-*-*-*-**-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**-*-*-*-*-*-*-*-*-*
    '''
    phone_number = "+33699901031" # https://developer.orange.com/apis/camara-sandbox-geofencing-orange-lab/getting-started#:~:text=48.785%2C%202.305%2C2000)%20work-,very%20well%20%3B,-)
    latitude = "48.79"
    longitude = "2.265"
    radius = 2000 

    sub_id = "217f6e6f-9b37-4e88-8c9b-901e2f4cff6a"

    access_token = get_access_token(client_id, client_secret, scope)
    #response = geofencing_post_entered(access_token, phone_number, latitude, longitude, radius)
    #response = geofencing_post_left(access_token, phone_number, latitude, longitude, radius)
    #response = geofencing_get_id(access_token, sub_id)
    response = geofencing_get(access_token)
    #response = geofencing_delete_id(access_token, sub_id)
    print(json.dumps(response, indent=4))

