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
- Pera Wallet with TestNet ALGO (for transaction fees ~0.001 ALGO per song)

### Setup

1. **Clone and install dependencies:**
```bash
git clone https://github.com/edzaniBruce51/song-registry-smart-contract.git
cd song-registry-smart-contract
pip install -r requirements.txt
```

2. **Configure environment:**
   - Copy your 25-word mnemonic from Pera Wallet
   - Create a `.env` file in the project directory:
   ```
   ALGOWALLET_MNEMONIC=your 25 word mnemonic phrase here
   ```

3. **Run the app:**
```bash
python app.py
```

Visit `http://127.0.0.1:5000` to register and view songs.

## Features

- **Zero-cost song registration** (only network fees ~0.001 ALGO)
- **Permanent blockchain storage** in transaction notes
- **Public verification** via Algorand Explorer
- **No smart contract complexity** - just simple payment transactions
- **Human-readable JSON** metadata on the blockchain

## Example Transaction Note
```json
{
  "application": "songRegistry",
  "version": 3,
  "title": "My Song",
  "url": "https://example.com/song.mp3",
  "price": 5,
  "owner": "GLQZZC3SKIHGOAPAYDXG2D5WZJ3NBSIPXPCB3JF62KBOTZRF6VTCL65FWM"
}
```

## Tech Stack

- **Frontend:** Flask, HTML, CSS
- **Blockchain:** Algorand TestNet (zero-value payments)
- **Data Storage:** Transaction notes (JSON format)
- **APIs:** Algorand Node API + Indexer API
- **Wallet:** Pera Wallet integration

## Architecture Benefits

✅ **Simplified Development** - No smart contract deployment or maintenance
✅ **Cost Effective** - Only pay minimal network fees
✅ **Transparent** - All data visible on public blockchain explorers
✅ **Immutable** - Permanent record of song registrations
✅ **Accessible** - Standard blockchain APIs work out-of-the-box

## Business Value

Perfect for businesses wanting blockchain benefits without blockchain complexity:
- Proof of ownership and timestamping
- Public verification capabilities
- Minimal technical overhead
- Universal accessibility via standard APIs
