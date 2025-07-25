# DeFi Vault Assistant Bot

A powerful Telegram bot that brings DeFi market data, alerts, education, and more directly to your Telegram chat.

## Features

- **Real-Time Market Data:** Fetches top DeFi tokens with price, 24h change, and market cap using CoinMarketCap API.
- **Custom Alerts:** Set price alerts for your favorite tokens and get notified instantly.
- **Daily Digest:** Receive a daily summary of the DeFi market.
- **Definitions & Explanations:** Get clear explanations of DeFi terms and concepts.
- **User-Friendly Commands:** Simple commands and inline buttons for easy interaction.

---

## Getting Started

### Prerequisites
- Python 3.10+
- Telegram Bot Token ([Get from BotFather](https://core.telegram.org/bots#botfather))
- CoinMarketCap API Key ([Get from CoinMarketCap](https://pro.coinmarketcap.com/account/))

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/defi-vault-assistant-bot.git
   cd defi-vault-assistant-bot
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Local Development

### 1. Set up Environment Variables
Create a `.env` file in the project root:
```
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here
COINMARKETCAP_API_KEY=your-coinmarketcap-api-key-here
SELF_AWAKE_URL=http://localhost:8000/  # Optional, for self-awake script
```

### 2. Run the Bot
```bash
python main.py
```

If you use the self-awake script, run both:
```bash
python main.py & python self_awake.py
```

---

## Deploying on Render

1. **Push your code to GitHub.**
2. **Create a new Web Service** on [Render](https://render.com/), connect your repo.
3. **Set environment variables** in the Render dashboard:
   - `TELEGRAM_BOT_TOKEN`
   - `COINMARKETCAP_API_KEY`
   - `SELF_AWAKE_URL` (set to your Render web service URL)
4. **Set the Start Command:**
   ```bash
   bash -c "python main.py & python self_awake.py"
   ```
5. **Deploy!**

---


## Usage

- `/start` — Show welcome message and main menu
- `/market` — Show top DeFi tokens (CoinMarketCap)
- `/alert` — Set a price alert
- `/digest` — Opt in to daily digest
- `/define <term>` — Get a definition of a DeFi term
- `/explain <concept>` — Get an explanation of a DeFi concept
---

## Troubleshooting
- **ModuleNotFoundError:** If you see errors about missing modules (e.g., `dotenv`, `google`), make sure all dependencies are listed in `requirements.txt` and installed.
- **KeyError for Environment Variables:** Ensure all required environment variables are set in your `.env` file (locally) or in the Render dashboard (production).
- **Coroutine Not Awaited Warning:** The alert scheduler is async-safe; if you modify alert logic, ensure async compatibility is maintained.
- **Service Sleeping on Render:** The Flask keepalive server and/or self-awake script help prevent your service from sleeping.

---

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## License
[MIT](LICENSE) 