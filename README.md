# DeFi Vault Assistant Bot

A powerful Telegram bot that brings DeFi market data, alerts, education, and more directly to your Telegram chat.

## Features

- **Real-Time Market Data:** Fetches top DeFi tokens with price, 24h change, and market cap. Automatically falls back to a backup API if the primary is unavailable.
- **Custom Alerts:** Set price alerts for your favorite tokens and get notified instantly.
- **Daily Digest:** Receive a daily summary of the DeFi market.
- **Definitions & Explanations:** Get clear explanations of DeFi terms and concepts.
- **Multilingual Support:** Supports multiple languages for a global audience.
- **User-Friendly Commands:** Simple commands and inline buttons for easy interaction.

---

## Getting Started

### Prerequisites
- Python 3.10+
- Telegram Bot Token ([Get from BotFather](https://core.telegram.org/bots#botfather))

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
SELF_AWAKE_URL=https://your-app-url.onrender.com/  # Optional, for self-awake script
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
   - `SELF_AWAKE_URL` (set to your Render web service URL)
4. **Set the Start Command:**
   ```bash
   bash -c "python main.py & python self_awake.py"
   ```
5. **Deploy!**

---

## Usage

- `/start` — Show welcome message and main menu
- `/top` — Show top DeFi tokens
- `/alert` — Set a price alert
- `/digest` — Opt in to daily digest
- `/define <term>` — Get a definition of a DeFi term
- `/explain <concept>` — Get an explanation of a DeFi concept
- `/language` — Change bot language

---

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## License
[MIT](LICENSE) 