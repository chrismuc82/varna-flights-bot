
# Varna Flights Bot

A Python-based Telegram bot that provides real-time flight offers for various German airports departing from Varna, Bulgaria. The bot checks flight prices, provides updates, and sends notifications for one-way and roundtrip flights based on user preferences.

### Features
- **Real-time Flight Offers**: Fetches the latest one-way and roundtrip flight offers from Varna to various German cities using the Kiwi API (Tequila).
- **Personalized Alerts**: Users can subscribe to specific city offers and choose whether to receive updates for one-way or roundtrip flights.
- **Price Updates**: The bot ensures that users are notified of any cheaper flight offers or updated flight details.
- **Telegram Integration**: Notifications are sent directly to Telegram topics (organized by destination airports) for easy access to flight details.
- **Automated Updates via GitHub Actions**: The bot runs every 5 minutes on GitHub Actions, ensuring up-to-date flight information without the need for manual intervention.

### Technologies Used
- **Python**: The main programming language used for the bot.
- **Kiwi API (Tequila)**: To fetch flight data.
- **Telegram Bot API**: For sending flight updates to the user.
- **Gist**: For storing and managing flight offer data (prices and topics).
- **Requests Library**: For making HTTP requests to the APIs.
- **JSON**: For data storage and parsing.
- **GitHub Actions**: For automating the script to run every 5 minutes.

---

### Requirements

- Python 3.7+
- `requests` library
- A `.env` file for sensitive data like your Kiwi API key and Telegram Bot API key.
- GitHub repository set up with GitHub Actions for periodic execution (every 5 minutes).

---

### Setup

#### 1. Clone the repository:

```bash
git clone https://github.com/chrismuc82/varna-flights-bot.git
cd varna-flights-bot
```

#### 2. Install required Python packages:

```bash
pip install -r requirements.txt
```

#### 3. Set up environment variables:

Create a `.env` file in the project root and fill it with your API keys and other credentials:

```plaintext
KIWI_API_KEY=your_kiwi_api_key
TELEGRAM_API_KEY=your_telegram_bot_api_key
GROUP_ID=your_telegram_group_id
GIST_ID=your_gist_id
GIST_TOKEN=your_gist_token
```

---

### How to Use

1. **Start the bot**: Run the `main.py` file to start fetching flight offers.

```bash
python main.py
```

2. **GitHub Actions Setup**: The bot will run every 5 minutes on GitHub Actions, fetching the latest flight data and sending notifications to your Telegram group.

3. **Bot Functionality**: The bot fetches flight data for a specified period (e.g., 90 days in the future) and sends updates for the relevant destinations. You can modify which airports (topics) to subscribe to, and the bot will send notifications to the corresponding Telegram group based on the available offers.

4. **Topic Management**: The bot creates topics (threads) for each airport in the Telegram group, and each thread corresponds to a different destination city. The users can mute or unmute notifications for individual cities.

5. **Flight Data**: The bot stores flight data (prices, destinations, and timestamps) in a Gist, ensuring the data is persistent and accessible across different sessions.

---

### Contributing

Feel free to fork the repository, submit issues, or create pull requests. Contributions are welcome to improve the bot's functionality or add new features, such as more cities, advanced filtering, or more comprehensive notifications.

---

### Roadmap / Future Features

- **Expanded City Support**: Add more cities for departure and destination, covering more routes.
- **User Customization**: Allow users to filter offers by price range, airlines, and other preferences.
- **Enhanced Notification Logic**: Implement more refined push notifications based on user behavior and historical data.

---

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
