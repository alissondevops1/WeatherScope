
import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel,
    QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        # 🔐 API KEY (recomendo futuramente usar .env)
        self.API_KEY = "d1ef2c754d9c51631dc73ed3f78e1372"

        # 🧩 Widgets
        self.city_label = QLabel("Weather App")
        self.city_input = QLineEdit()
        self.search_button = QPushButton("Search")
        self.refresh_button = QPushButton("Refresh")
        self.clear_button = QPushButton("Clear")

        self.result_label = QLabel("")
        self.emoji_label = QLabel("")
        self.details_label = QLabel("")
        self.history_label = QLabel("Recent searches")
        self.history_list = QListWidget()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setWindowIcon(QIcon("assets/icons/weather.png"))
        self.setFixedSize(400, 500)

        # Layout principal
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.clear_button)

        main_layout.addWidget(self.city_label)
        main_layout.addWidget(self.city_input)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.result_label)
        main_layout.addWidget(self.emoji_label)
        main_layout.addWidget(self.details_label)
        main_layout.addWidget(self.history_label)
        main_layout.addWidget(self.history_list)

        self.setLayout(main_layout)

        # 🔗 Conexões
        self.search_button.clicked.connect(self.get_weather)
        self.refresh_button.clicked.connect(self.get_weather)
        self.clear_button.clicked.connect(self.clear_fields)
        self.history_list.itemClicked.connect(self.load_history_city)
        self.city_input.returnPressed.connect(self.get_weather)

        # 🎯 Alinhamento
        self.city_label.setAlignment(Qt.AlignCenter)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.details_label.setAlignment(Qt.AlignCenter)

        # ✨ Placeholder
        self.city_input.setPlaceholderText("Enter a city (e.g. London)")

        # 🎨 Estilo moderno (dark mode)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: #ffffff;
                font-family: Segoe UI;
            }

            QLabel#title {
                font-size: 28px;
                font-weight: bold;
            }

            QLineEdit {
                padding: 10px;
                border-radius: 10px;
                background-color: #2c2c3e;
                border: 1px solid #444;
                font-size: 16px;
            }

            QPushButton {
                padding: 10px;
                border-radius: 10px;
                background-color: #4a4af4;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #6a6aff;
            }

            QLabel#result {
                font-size: 22px;
                margin-top: 15px;
            }

            QLabel#emoji {
                font-size: 60px;
            }

            QLabel#details {
                font-size: 16px;
                color: #cccccc;
            }
        """)

        # IDs para style
        self.city_label.setObjectName("title")
        self.result_label.setObjectName("result")
        self.emoji_label.setObjectName("emoji")
        self.details_label.setObjectName("details")

    def get_weather(self):
        city = self.city_input.text().strip()

        if not city:
            self.show_error("Please enter a city name.")
            return

        self.result_label.setText("Fetching weather...")
        self.emoji_label.clear()
        self.details_label.clear()

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.API_KEY}&units=metric"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            self.display_weather(data)

        except requests.exceptions.HTTPError:
            self.show_error("City not found.")
        except requests.exceptions.ConnectionError:
            self.show_error("No internet connection.")
        except requests.exceptions.Timeout:
            self.show_error("Request timed out.")
        except requests.exceptions.RequestException:
            self.show_error("Something went wrong.")

    def display_weather(self, data):
        city = data["name"]
        country = data["sys"]["country"]

        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        description = data["weather"][0]["description"].title()
        weather_id = data["weather"][0]["id"]

        emoji = self.get_weather_emoji(weather_id)

        self.result_label.setText(
            f"📍 {city}, {country}\n\n"
            f"{temp:.0f}°C (Feels like {feels_like:.0f}°C)\n"
            f"{description}"
        )

        self.emoji_label.setText(emoji)

        self.details_label.setText(
            f"💧 Humidity: {humidity}%\n"
            f"🌬 Wind: {wind} m/s"
        )
        if city not in [
            self.history_list.item(i).text()
            for i in range(self.history_list.count())
        ]:
            self.history_list.addItem(city)

    def show_error(self, message):
        self.result_label.setText(message)
        self.emoji_label.clear()
        self.details_label.clear()

    def clear_fields(self):
        self.city_input.clear()
        self.result_label.clear()
        self.emoji_label.clear()
        self.details_label.clear()

    def load_history_city(self, item):
        self.city_input.setText(item.text())
        self.get_weather()

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return "🌍"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())