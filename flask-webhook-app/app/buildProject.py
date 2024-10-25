#Reference: https://docs.companycam.com/reference/createproject

def create_project(name, street_address, city, state, country, latitude, longitude, contact_email, contact_phone):
    import requests
    from config import COMPANY_CAM_API_TOKEN

    url = "https://api.companycam.com/v2/projects"

    # Construct the payload using parameters
    payload = {
        "name": name,  # Project name and contact name are the same
        "address": {
            "street_address_1": street_address,
            "city": city,
            "state": state,
            "country": country
        },
        "coordinates": {
            "lat": latitude,
            "lon": longitude
        },
        "primary_contact": {
            "name": name,  # Reuse the name parameter for the contact name
            "email": contact_email,
            "phone_number": contact_phone
        }
    }
    
    # Set up headers
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {COMPANY_CAM_API_TOKEN}"
    }

    # Make the POST request
    response = requests.post(url, json=payload, headers=headers)

    # Return the response
    if response.status_code == 201:
        print("///// Project created successfully! /////")
        return response.json()
    else:
        print(f"Failed to create project. Status Code: {response.status_code}")
        return response.text


