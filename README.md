# Song Registry v4 - BaaS Integration

A Flask web application that stores song metadata on the Algorand blockchain through a Blockchain as a Service (BaaS) platform integration. Features asynchronous processing and webhook notifications!

## How It Works

This v4 approach uses BaaS (Blockchain as a Service) integration:
- Sends **JSON payloads** to BlockAPI BaaS platform
- Receives **immediate confirmation** and queues for blockchain processing
- Gets **webhook notifications** when blockchain write completes
- Provides **asynchronous, scalable** blockchain integration

## Quick Start

### Prerequisites
- Python 3.7+

### Setup

1. **Clone and install dependencies:**
```bash
git clone https://github.com/edzaniBruce51/Algorand-song-registry-v4.git
cd Algorand-song-registry-v4
pip install -r requirements.txt
```

2. **Configure environment:**
  FLASK_SECRET_KEY=your_flask_secret
  BLOCKAPI_BASE_URL=https://blockapi.co.za/api/v1
  BLOCKAPI_API_KEY=your_api_key_here
  WEBHOOK_URL=https://your-service.onrender.com/webhook/blockchain-notification

3. **Run the app:**
```bash
python app.py
```

Visit `http://127.0.0.1:5000` to register and view songs.

## Features

- **No wallet setup required** ((BaaS handles blockchain access)
- **Asynchronous writes** with webhooks for transaction confirmation
- **Public verification** via Algorand Explorer (transaction ID stored)
- **Simple metadata registry** - (song title, URL, price, owner)
- **Flash messages** show success/errors in UI

## Example Payload Sent to Baas
{
  "dataSchemaName": "songRegistry",
  "dataId": "song_1724209000",
  "jsonPayload": {
    "application": "songRegistry",
    "version": 4,
    "title": "My Song",
    "url": "https://example.com/song.mp3",
    "price": 5,
    "owner": "GLQZZC3SKIHGOAPAYDXG2D5WZJ3NBSIPXPCB3JF62KBOTZRF6VTCL65FWM",
    "timestamp": "2025-08-20T08:00:00Z"
  }
}


## Tech Stack

- **Frontend:** HTML, Flash Messages 
- **Blockchain:** Flask (Python)
- **Data Storage:** In-memory (songs list; not persistent)
- **Blockchain:** Algorand (via BlockAPI Baas)
- **Deployment:** Render

## Architecture Benefits

✅ **Simplified Development** - No smart contract deployment or maintenance, BaaS handles complexity
✅ **Webhook-driven** - updates -> async & scalable
✅ **Transparent** - Transaction IDs verifiable on Algorand Explorer
✅ **No private keys** - no risk of wallet exposure 


## Business Value

Perfect for businesses wanting blockchain benefits without blockchain complexity:
- Proof of ownership and timestamping
- Public verification capabilities
- Minimal technical overhead
- Easy integration into existing apps
