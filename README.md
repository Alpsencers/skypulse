# ⚡ SkyPulse — Real-Time Weather Application

A modern, animated, and feature-rich weather web application built with Python Flask.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-4.0-orange?logo=chartdotjs&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 🔍 **City Search** — Search weather for any city worldwide
- 🌡️ **Real-Time Weather** — Temperature, humidity, wind speed, pressure, visibility, cloud coverage
- 📅 **5-Day Forecast** — Interactive clickable cards with detailed daily breakdowns
- 📈 **Temperature & Humidity Chart** — Interactive Chart.js visualization
- 🎨 **Dynamic Weather Animations** — Rain, snow, sun, thunderstorm, fog, clouds, and stars
- 🌙 **Dark/Light Theme** — One-click theme toggle with persistent preference
- 📍 **Geolocation** — IP-based automatic city detection
- ⭐ **Favorite Cities** — Save up to 5 frequently checked cities (cookie-based)
- ⏰ **Live Clock & Date** — Real-time clock display in Turkish format
- 📱 **Fully Responsive** — Optimized for mobile, tablet, and desktop

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| Backend | Python, Flask |
| Frontend | HTML5, CSS3 (Glassmorphism, CSS Animations), Vanilla JavaScript |
| API | OpenWeatherMap API, ip-api.com (Geolocation) |
| Charting | Chart.js |
| Typography | Google Fonts (Outfit, JetBrains Mono) |

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- OpenWeatherMap API key ([free signup](https://openweathermap.org/api))

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/skypulse.git
cd skypulse

# Install dependencies
pip install -r requirements.txt

# Add your API key in app.py
# API_KEY = "your_api_key_here"

# Run the application
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## 📁 Project Structure

```
skypulse/
├── app.py              # Flask backend & API integration
├── templates/
│   └── index.html      # Frontend (HTML + CSS + JS)
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # Documentation
```

## 🌦️ Supported Weather Animations

| Weather | Animation |
|---------|-----------|
| ☀️ Clear | Glowing sun with pulse effect |
| 🌙 Clear Night | Twinkling star field |
| 🌧️ Rain | Falling raindrops |
| ❄️ Snow | Rotating snowflakes |
| ⛈️ Thunderstorm | Rain + lightning flashes |
| ☁️ Cloudy | Drifting cloud layers |
| 🌫️ Fog/Mist | Flowing fog layers |

## 🖥️ Screenshots

> Add screenshots of your application here.

## 📝 License

This project is licensed under the MIT License.

---

⭐ Star this repo if you found it useful!
