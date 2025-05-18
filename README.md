# bignugget

**Telegram bot for (future) alert notifications and generating a map of active alarm regions in Ukraine**

---

## Description

`bignugget` is a lightweight Telegram bot written in Python that:
- Periodically queries a Ukrainian alarms API and saves the data to a local JSON file (`alerts_data.json`)
- Generates a color-coded map of Ukraine, highlighting regions where an alarm is active
- Presents the user with a menu offering two actions:  
  1. 🗺️ Show the current alarm map  
  2. 🚨 Retrieve the current list of alarms in text form  
- Built using **aiogram** and **Pillow**

## Requirements

- Python 3.12 or higher  
- Libraries: `aiogram`, `Pillow`, `python-dotenv`, `alerts-in-ua`

---

## Quick Start

0. **Create token in [BotFather](t.me/BotFather) and [Alerts in ua](https://devs.alerts.in.ua/)**
1. **Clone the repository**  
   ```bash
   git clone https://github.com/mLeviGen/bignugget.git
   cd bignugget
   ```
2. **Create a virtual environment**
   ```bash
   python3.12 -m venv .venv
   ```
   On Linux/macOS:
   ```bash
   source .venv/bin/activate
   ```
   On Windows:
   ```bash
   .\.venv\Scripts\activate
   ```
3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install aiogram Pillow python-dotenv alerts-in-ua
   ```
4. **Configure environment variables**
   Create a file named `.env` in the project root with the following contents:
   ```bash
   TELEGRAM_BOT_TOKEN=<your BotFather token>
   ALERTS_IN_UA_TOKEN=<your alerts_in_ua API key>
   ```
5. **Run the bot**
   ```bash
   python main.py
   ```

## Additionally

- To adjust the alarms update interval, modify the `asyncio.sleep(7)` line in `app/handlers/alerts_event.py`.
- To customize the map appearance, update the base image at `app/images/UK2.png` and the region masks in `app/images/menus/`.
- Use Python’s logging module for debugging; change the level in `main.py` via `logging.basicConfig(level=logging.DEBUG)`.

   
   
