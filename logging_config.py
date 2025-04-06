import logging
import sys

# Erstelle einen Handler für die Konsolenausgabe
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Erstelle einen Handler für die Dateiausgabe
file_handler = logging.FileHandler('varna_flights_bot.log')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Konfiguriere den Root-Logger
logging.basicConfig(level=logging.DEBUG, handlers=[console_handler, file_handler])
