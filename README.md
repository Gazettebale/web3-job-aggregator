# 🚀 Web3 Jobs Pro

**Professional Web3/Crypto job aggregator with real APIs and optimized scraping**

Find thousands of Web3 jobs from multiple sources in one beautiful interface.

## ✨ Features

- 🎯 **Real APIs** - Greenhouse & Lever JSON APIs (no auth needed!) + optimized scraping
- 🌍 **Multi-language** - English & French support
- 🎨 **Modern UI** - Cyberpunk-inspired design with smooth animations
- ⚡ **Parallel Fetch** - All sources scanned simultaneously for speed
- 📱 **Responsive** - Works on all devices
- 🔍 **Smart Filters** - 50+ keyword categories (roles, tech, chains, sectors)
- 💾 **Export** - Download results as JSON
- 🔄 **Deduplication** - Smart duplicate detection across sources

## 📊 Data Sources (15+)

### 🟢 API-Powered (Reliable, structured JSON)

**Greenhouse Job Board API** (54 companies, public, no auth):
- Coinbase, Kraken, Blockchain.com, Robinhood, Fireblocks, Chainalysis
- Ledger, BitGo, Circle, Paxos, Anchorage Digital, Figment
- Uniswap Labs, Paradigm, ConsenSys, OpenSea, dYdX, Compound, Aave
- Arbitrum, Optimism, Celestia, EigenLayer, StarkWare, Immutable
- Sui/Mysten Labs, Aptos Labs, ZetaChain, Startale (Astar)
- Galaxy Digital, Gauntlet, Polychain Capital, Multicoin, Pantera Capital
- Wormhole, Eco Protocol, Nethermind, Biconomy, Nansen, Messari
- Dune Analytics, LayerZero, Axelar, Rarible, and more...

**Lever Postings API** (36 companies, public, no auth):
- Crypto.com, Binance, Animoca Brands, CertiK
- Polygon, Chainlink, Offchain Labs, Arbitrum Foundation
- Ethereum Foundation, Solana Foundation, Aztec, zkSync, Nibiru
- Alchemy, QuickNode, The Graph, Tenderly, Phantom, WalletConnect
- Worldcoin, Wintermute, Flow Traders, Token Metrics
- Mythical Games, Sky Mavis (Axie), The Sandbox
- Protocol Labs, Filecoin, Livepeer, Kadena, LUKSO, POAP, and more...

**Web3.career API** (optional, needs free API key):
- Sign up at [web3.career/web3-jobs-api](https://web3.career/web3-jobs-api)
- Set `WEB3CAREER_API_KEY` env variable
- 27,000+ jobs database, hourly updates

### 🔵 Scraping Sources

- **CryptocurrencyJobs.co** - Leading crypto job board
- **Web3.career** - 70,000+ jobs database
- **CryptoJobsList** - Running since 2017
- **Remote3** - Remote-first Web3 jobs
- **CryptoJobs.com** - AI-powered job portal
- **Crypto.Jobs** - Community of 4,000+ enthusiasts
- **BeInCrypto Jobs** - Major crypto media job board
- **JobStash** - Web3 job aggregator
- **Crypto-Careers** - Enterprise-level crypto jobs
- **Dragonfly Job Board** - VC portfolio companies
- **Solana Job Board** - Solana ecosystem jobs
- **Avalanche Job Board** - Avalanche ecosystem jobs
- **Ethereum Job Board** - Ethereum-focused positions
- **Midnight Network** - Cardano sidechain jobs
- **Block (Square/Cash App)** - Fintech/crypto giant

**Result: 2000+ jobs aggregated from 90+ companies via API + 15 job boards**

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open http://localhost:5000
```

### Deploy to Render

1. Push to GitHub
2. Go to [render.com](https://render.com)
3. New Web Service → Connect your repo
4. Deploy!

**Free tier works perfectly!**

## 🔧 Configuration

### Add More Greenhouse Companies

Edit `job_aggregator.py`:
```python
self.greenhouse_companies = [
    ('company-slug', 'Company Name'),
    # Find the slug from: boards.greenhouse.io/{slug}
]
```

### Add More Lever Companies

```python
self.lever_companies = [
    ('company-slug', 'Company Name'),
    # Find the slug from: jobs.lever.co/{slug}
]
```

### Toggle Sources On/Off

```python
self.sources = {
    'source_name': {
        'enabled': True,  # Toggle here
        'type': 'api'     # or 'scraping'
    }
}
```

### Add More Languages

Edit `app.py` translations dict:
```python
'es': {
    'title': 'Web3 Jobs Pro',
    'subtitle': 'Encuentra tu próximo trabajo en crypto',
    # ...
}
```

## 🏗️ Architecture

```
web3-jobs-pro/
├── app.py                  # Flask server + API endpoints
├── job_aggregator.py       # Core aggregator (APIs + scraping)
├── requirements.txt        # Python dependencies
├── static/
│   ├── css/style.css       # Cyberpunk-themed UI
│   └── js/app.js           # Frontend logic
└── templates/
    └── index.html          # Main template (Jinja2)
```

**Key Design Decisions:**
- Greenhouse & Lever use their **official public JSON APIs** (no scraping needed, more reliable)
- Scraping sources use **CSS selectors with fallback strategies** (not fragile regex)
- **Parallel execution** with ThreadPoolExecutor (6 workers) for speed
- **Smart deduplication** normalizes titles/companies before comparison
- **Background search** with polling to avoid HTTP timeouts

## 📝 License

MIT License - Use it however you want!

## 🙏 Credits

Built by [@_Gazettebale](https://twitter.com/_Gazettebale) for the Web3 community

---

**Star ⭐ this repo if you find it useful!**
