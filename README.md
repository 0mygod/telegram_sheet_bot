# Telegram Google Sheet Production Bot

This bot fetches daily production and WIP data from a Google Sheet and displays it line-wise using Telegram.

## ⚙️ Setup

### 1. Required Environment Variables

Set the following in Railway or locally using `.env`:

- `TELEGRAM_TOKEN` = Your Telegram bot token
- `SHEET_URL` = Shareable Google Sheet URL (with public access or same service account access)

### 2. File Required

- `credentials.json` – Google service account key (download from Google Cloud Console)

### 3. Deploy on Railway

1. Go to [https://railway.app](https://railway.app)
2. Click **New Project** → Deploy from GitHub
3. Upload this repo
4. Add the environment variables above
5. Upload `credentials.json` in the "Files" tab
6. Watch logs – Bot will start polling

## ✅ Bot Commands

- `/start` – Start the bot and select production line

Enjoy automated line-wise tracking!
