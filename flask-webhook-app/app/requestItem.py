import requests
import json
import re  # For cleaning the phone number

def parse_location(column_value):
    try:
        # Load the location data from the column value (which is a JSON string)
        address_data = json.loads(column_value)
        
        # Extract the full address, latitude, and longitude
        full_address = address_data.get("address", "N/A")
        latitude = address_data.get("lat", "N/A")
        longitude = address_data.get("lng", "N/A")
        
        # Split the full address into components, provide "N/A" fallback for missing components
        address_components = full_address.split(",") if full_address != "N/A" else ["N/A", "N/A", "N/A", "N/A"]
        address = {}
        address["street address"] = address_components[0].strip() if len(address_components) > 0 else "N/A"
        address["city"] = address_components[1].strip() if len(address_components) > 1 else "N/A"
        address["state"] = address_components[2].strip() if len(address_components) > 2 else "N/A"
        address["country"] = address_components[3].strip() if len(address_components) > 3 else "N/A"
        if address["country"] == "USA":
            address["country"] = "US"
        
        # Add latitude and longitude to the address dictionary
        address["latitude"] = latitude if latitude else "N/A"
        address["longitude"] = longitude if longitude else "N/A"
        
        # Return the address with latitude and longitude
        return address
    except json.JSONDecodeError:
        return {
            "street address": "N/A",
            "city": "N/A",
            "state": "N/A",
            "country": "N/A",
            "latitude": "N/A",
            "longitude": "N/A"
        }

def parse_phone(column_value):
    try:
        # Load the phone data from the column value (which is a JSON string)
        phone_data = json.loads(column_value)

        # Extract the raw phone number
        raw_phone_number = phone_data.get("phone", "N/A")
        
        # Clean the phone number: Remove non-digit characters
        clean_phone_number = re.sub(r'\D', '', raw_phone_number)
        
        # Keep only the rightmost 10 digits
        if len(clean_phone_number) > 10:
            clean_phone_number = clean_phone_number[-10:]

        # Return the cleaned phone number or "N/A"
        return clean_phone_number if clean_phone_number else "N/A"
    except json.JSONDecodeError:
        return "N/A"

def parse_email(column_value):
    try:
        # Load the email data from the column value (which is a JSON string)
        email_data = json.loads(column_value)
        
        # Extract email address
        email_address = email_data.get("email", "N/A")
        
        # Return the email address
        return email_address if email_address else "N/A"
    except json.JSONDecodeError:
        return "N/A"

# Function to retrieve the item and process the column values
def get_item(apiKey, itemID):
    # Define API URL and headers for the request
    apiUrl = "https://api.monday.com/v2"
    headers = {"Authorization" : apiKey, "API-Version" : "2023-04"}
    
    # GraphQL query to fetch the item details by itemID
    query = f"""query {{
    items (ids: {itemID}) {{
        column_values {{
        column {{
            id
            title
        }}
        id
        type
        value
        }}
    }}
    }}"""

    # Send the POST request to the Monday.com API
    data = {'query' : query}
    response = requests.post(url=apiUrl, json=data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Load the response data
        data = response.json()

        # Initialize result dictionary
        result = {
            "address": "N/A",
            "phone": "N/A",
            "email": "N/A"
        }
        
        # Process the item data
        item = data.get("data", {}).get("items", [])[0]
        for column in item.get("column_values", []):
            column_title = column.get("column", {}).get("title")
            column_value = column.get("value", None)

            # Call the respective function based on the column title
            if column_title == "Location" and column_value:
                result["address"] = parse_location(column_value)
            elif column_title == "Phone Number" and column_value:
                result["phone"] = parse_phone(column_value)
            elif column_title == "Email Address" and column_value:
                result["email"] = parse_email(column_value)
        
        # Return the result dictionary
        return result
    else:
        # If the request failed, return a dictionary with "N/A" for each value
        return {
            "address": "N/A",
            "phone": "N/A",
            "email": "N/A"
        }

