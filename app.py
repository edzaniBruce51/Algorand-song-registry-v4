from flask import Flask, render_template, request, redirect, flash, jsonify
import json   # For encoding and decoding JSON data.
import os     # Access environment variables
import requests    # To send HTTP requests to the BaaS API
from dotenv import load_dotenv   #Loads .env file for secret configuration
from datetime import datetime, timezone     # Used for timestamps in UTC.

load_dotenv()

app = Flask(__name__)  #Initializes Flask app.
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback-secret-for-dev-only')   # Loads secret key for session management and flash messages.

# BaaS API Configuration
BLOCKAPI_BASE_URL = os.getenv("BLOCKAPI_BASE_URL", "https://blockapi.co.za/api/v1")
BLOCKAPI_API_KEY = os.getenv("BLOCKAPI_API_KEY")    # API key for authentication
WEBHOOK_URL = os.getenv("WEBHOOK_URL")      # Where the BaaS platform will POST blockchain notifications.

# Simple in-memory storage for registered songs (in production, use a database)
# This is a Python list in memory. While the Flask app is running, the songs list exists in RAM.
# Every element is a dictionary containing song info. 
# If your app restarts or redeploys, the list is cleared.
songs = []

@app.route("/")
def index():
    """View all registered songs"""
    return render_template("index.html", songs=songs) # passes the current songs list to display all registered songs.


@app.route("/register_song", methods=["POST"])
def register_song():
    # Get form data
    try:
        title = request.form.get("title")
        url = request.form.get("url")
        price = int(request.form.get("price"))
        owner = request.form.get("owner")

        # Validate owner address/ basic Algorand address validation
        if not owner or len(owner) != 58:
            flash("Please provide a valid Algorand address (58 characters)", "error")
            return redirect("/")

        # Generate unique identifiers for tracking / Generate unique IDs
        import time
        song_id = len(songs) + 1  # Local tracking
        data_id = f"song_{int(time.time())}"  # Use timestamp for unique ID

        # Prepare song data for blockchain
        song_data = {
            "application": "songRegistry",
            "version": 4,
            "title": title,
            "url": url,
            "price": price,
            "owner": owner,  # Use the address provided by user
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z" # timestamp format 
        }

        # Prepare BaaS API payload according to their specification
        payload = {
            "dataSchemaName": "songRegistry",  # Table/schema name from sender perspective
            "dataId": data_id,                 # Row ID from sender perspective
            "jsonPayload": song_data           # The actual data to be hashed and stored
        }

        # Try different header formats - blockapi.co.za might use different auth
        headers = {
            "X-API-Key": BLOCKAPI_API_KEY,  # Common API key format
            "Content-Type": "application/json"
        }

        # Send request to correct BaaS API endpoint
        response = requests.post(
            f"{BLOCKAPI_BASE_URL}/blockchainTask",
            json=payload,
            headers=headers,
            timeout=30
        )

        # Handle response
        if response.status_code in [200, 201]:  # Accept both 200 and 201 as success
            # Parse the response to get BaaS task ID
            response_data = response.json()
            baas_task_id = response_data.get('data', {}).get('id')

            # Add to local storage for display with tracking info
            song_data['id'] = song_id
            song_data['data_id'] = data_id
            song_data['baas_task_id'] = baas_task_id
            song_data['status'] = 'pending' 
            songs.append(song_data)    #Saves song locally with a pending status until the blockchain confirms
            flash(f"Song registered successfully! Tracking ID: {data_id}", "success")
            flash(f"BaaS Task ID: {baas_task_id} - Your song will be written to the blockchain shortly.", "info")
        else:
            flash(f"Error: {response.status_code} - {response.text}", "error")

    except Exception as e:
        flash(f"Error registering song: {e}", "error")

    return redirect("/")

# Receive blockchain updates
@app.route("/webhook/blockchain-notification", methods=["POST"])
def blockchain_webhook():
    try:
        webhook_data = request.get_json(silent=True)
        if not webhook_data:
            print("Webhook error: no JSON body")
            return jsonify({"error": "Invalid webhook"}), 400

        print(f"Received webhook: {webhook_data}")

        data_id = webhook_data.get("dataId")
        results = webhook_data.get("BlockchainResults", [])

        tx_id = None
        explorer_url = None
        success_flag = None

        if results and isinstance(results, list):
            first = results[0]
            tx_id = first.get("transactionId")
            explorer_url = first.get("transactionExplorerUrl")
            success_flag = first.get("isSuccess")

        # Update your in-memory songs list
        for song in songs:
            if song.get("data_id") == data_id:
                if success_flag is True:
                    song["status"] = "confirmed"
                elif success_flag is False:
                    song["status"] = "failed"
                else:
                    song.setdefault("status", "pending")

                if tx_id:
                    song["blockchain_tx_id"] = tx_id
                if explorer_url:
                    song["explorer_url"] = explorer_url

                print(f"Updated song {data_id}: {song}")
                break

        return jsonify({"message": "Webhook processed successfully"}), 200

    except Exception as e:
        print(f"Webhook exception: {e}")
        return jsonify({"error": str(e)}), 500


# Application Runner.
# Starts Flask server on Render or local machine.
# Uses environment variable PORT if provided.
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))