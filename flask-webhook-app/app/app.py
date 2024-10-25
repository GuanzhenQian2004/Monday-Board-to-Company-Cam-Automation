from flask import Flask, request, jsonify
import config
import requestItem
import buildProject

# Initialize the Flask app
app = Flask(__name__)

# Define the route to handle incoming webhooks from Monday.com
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    
    data = request.get_json()
    # Debug: Print received data from webhook
    print("\nRecieved Data From Webhook:\n", data, "\n")

    # Initial webhook verification setup
    if 'challenge' in data:
        challenge = data['challenge']
        return jsonify({'challenge': challenge}), 200


    event_type = data.get('event', {}).get('type', '')
    board_id = data.get('event', {}).get('boardId', '')
    group_name = data.get('event', {}).get('groupName', '')

    if event_type == 'create_pulse' and board_id == config.BOARD_ID and group_name == config.GROUP_NAME:
        item_name = data.get('event', {}).get('pulseName', 'Unknown Item')
        item_id = data.get('event', {}).get('columnValues', {}).get('text0').get("value")
        print(f"///// New item created: {item_name} (ID: {item_id}) /////")
        
        item_column_data = requestItem.get_item(config.MONDAY_API_TOKEN, item_id)
        print("\nParsed Data:\n", item_column_data, "\n")

        street_address = item_column_data["address"]["street address"]
        city = item_column_data["address"]["city"]
        state = item_column_data["address"]["state"]
        country = item_column_data["address"]["country"]
        latitude = item_column_data["address"]["latitude"]
        longitude = item_column_data["address"]["longitude"]
        contact_phone = item_column_data["phone"]
        contact_email = item_column_data["email"]

        project_response = buildProject.create_project(item_name, street_address, city, state, country, latitude, longitude, contact_email, contact_phone)
        print("\nProject Response:\n", project_response, '\n')


    # Respond to acknowledge
    return jsonify({"status": "Webhook received"}), 200

# Run the Flask app on a specified port
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

