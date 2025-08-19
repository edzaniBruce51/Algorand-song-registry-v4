from flask import Flask, render_template, request, redirect, flash, jsonify
import json
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback-secret-for-dev-only')

# BaaS API Configuration
BLOCKAPI_BASE_URL = os.getenv("BLOCKAPI_BASE_URL", "https://blockapi.co.za/api/v1")
BLOCKAPI_API_KEY = os.getenv("BLOCKAPI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Simple storage for songs (in production, use a database)
songs = []

@app.route("/")
def index():
    """View all registered songs"""
    return render_template("index.html", songs=songs)


@app.route("/register_song", methods=["POST"])
def register_song():
    try:
        title = request.form.get("title")
        url = request.form.get("url")
        price = int(request.form.get("price"))
        owner = request.form.get("owner")

        # Validate owner address (basic Algorand address validation)
        if not owner or len(owner) != 58:
            flash("Please provide a valid Algorand address (58 characters)", "error")
            return redirect("/")

        # Generate unique identifiers for tracking
        import time
        song_id = len(songs) + 1
        data_id = f"song_{int(time.time())}"  # Use timestamp for unique ID

        # Build song data for blockchain
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

        # Send to correct BaaS API endpoint
        response = requests.post(
            f"{BLOCKAPI_BASE_URL}/blockchainTask",
            json=payload,
            headers=headers,
            timeout=30
        )

        if response.status_code in [200, 201]:  # Accept both 200 and 201 as success
            # Parse the response to get BaaS task ID
            response_data = response.json()
            baas_task_id = response_data.get('data', {}).get('id')

            # Add to local storage for display with tracking info
            song_data['id'] = song_id
            song_data['data_id'] = data_id
            song_data['baas_task_id'] = baas_task_id
            song_data['status'] = 'pending'
            songs.append(song_data)
            flash(f"Song registered successfully! Tracking ID: {data_id}", "success")
            flash(f"BaaS Task ID: {baas_task_id} - Your song will be written to the blockchain shortly.", "info")
        else:
            flash(f"Error: {response.status_code} - {response.text}", "error")

    except Exception as e:
        flash(f"Error registering song: {e}", "error")

    return redirect("/")


@app.route("/webhook/blockchain-notification", methods=["POST"])
def blockchain_webhook():
    """Webhook to receive transaction complete notifications from BaaS platform"""
    try:
        webhook_data = request.get_json()

        # Log the full webhook data for debugging
        print(f"Received webhook: {webhook_data}")

        # Extract the identifiers we sent originally
        data_schema_name = webhook_data.get('dataSchemaName')
        data_id = webhook_data.get('dataId')

        # Extract transaction details
        transaction_id = webhook_data.get('transactionId')
        status = webhook_data.get('status')  # success, failed, etc.

        if data_schema_name == "songRegistry" and data_id:
            # Find the song in our local storage using data_id
            for song in songs:
                if song.get('data_id') == data_id:
                    # Update song status based on blockchain result
                    song['status'] = 'confirmed' if status == 'success' else 'failed'
                    song['blockchain_tx_id'] = transaction_id
                    print(f"Updated song {data_id}: status={song['status']}, tx_id={transaction_id}")
                    break

        return jsonify({"message": "Webhook processed successfully"}), 200

    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return jsonify({"error": "Webhook processing failed"}), 500


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
