# ============================================
# SKYPULSE v3.0 - Hava Durumu Web Uygulaması
# ============================================

from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from datetime import datetime

app = Flask(__name__)

API_KEY = "dbf78f4f1221331c540dafbe83e0c60d"
BASE_URL = "https://api.openweathermap.org/data/2.5"


def get_weather_animation(weather_id, icon):
    is_night = "n" in str(icon)
    weather_id = int(weather_id)
    if 200 <= weather_id < 300: return "thunderstorm"
    elif 300 <= weather_id < 400: return "drizzle"
    elif 500 <= weather_id < 600: return "rain"
    elif 600 <= weather_id < 700: return "snow"
    elif 700 <= weather_id < 800: return "mist"
    elif weather_id == 800: return "clear-night" if is_night else "clear"
    elif weather_id > 800: return "clouds-night" if is_night else "clouds"
    return "clear"


def get_wind_direction(deg):
    """Rüzgar derecesini yön metnine çevirir."""
    dirs = ["K", "KKD", "KD", "DKD", "D", "DGD", "GD", "GGD",
            "G", "GGB", "GB", "BGB", "B", "BKB", "KB", "KKB"]
    idx = round(deg / 22.5) % 16
    return dirs[idx]


def get_uv_info(lat, lon):
    """UV indeks bilgisini çeker (OpenWeatherMap One Call yerine basit tahmin)."""
    # Ücretsiz planda UV API yok, saat ve enlem bazlı tahmin yapıyoruz
    hour = datetime.now().hour
    abs_lat = abs(lat)

    if hour < 6 or hour > 20:
        uv = 0
    elif hour < 8 or hour > 18:
        uv = 1
    elif hour < 10 or hour > 16:
        uv = 3 if abs_lat < 35 else 2
    else:
        if abs_lat < 25: uv = 9
        elif abs_lat < 35: uv = 7
        elif abs_lat < 45: uv = 5
        elif abs_lat < 55: uv = 3
        else: uv = 2

    if uv <= 2: level, color, advice = "Düşük", "#22c55e", "Güneş gözlüğü yeterli"
    elif uv <= 5: level, color, advice = "Orta", "#eab308", "Güneş kremi önerilir"
    elif uv <= 7: level, color, advice = "Yüksek", "#f97316", "Güneş kremi şart, şapka takın"
    elif uv <= 10: level, color, advice = "Çok Yüksek", "#ef4444", "Dışarı çıkmaktan kaçının"
    else: level, color, advice = "Aşırı", "#7c3aed", "Kesinlikle dışarı çıkmayın"

    return {"index": uv, "level": level, "color": color, "advice": advice}


def get_weather_advice(temp, weather_id, wind_speed, humidity):
    """Hava durumuna göre akıllı giyim ve aktivite tavsiyeleri."""
    tips = []
    weather_id = int(weather_id)

    # Sıcaklık
    if temp <= 0:
        tips.append({"icon": "🧥", "text": "Kalın mont, bere ve eldiven şart!"})
    elif temp <= 10:
        tips.append({"icon": "🧥", "text": "Mont veya kalın ceket alın"})
    elif temp <= 18:
        tips.append({"icon": "🧶", "text": "Hafif ceket veya hırka yeterli"})
    elif temp <= 25:
        tips.append({"icon": "👕", "text": "Tişört havası, güzel bir gün!"})
    elif temp <= 32:
        tips.append({"icon": "🧴", "text": "Güneş kremi sürmeyi unutmayın"})
    else:
        tips.append({"icon": "🥵", "text": "Aşırı sıcak! Gölgede kalın, bol su için"})

    # Yağış
    if 200 <= weather_id < 300:
        tips.append({"icon": "⛈️", "text": "Fırtına var, dışarı çıkmayın"})
    elif 300 <= weather_id < 600:
        tips.append({"icon": "☂️", "text": "Şemsiye almayı unutmayın"})
    elif 600 <= weather_id < 700:
        tips.append({"icon": "❄️", "text": "Kar var, kaymayan ayakkabı giyin"})
    elif 700 <= weather_id < 800:
        tips.append({"icon": "🌫️", "text": "Sis var, araç kullanırken dikkat"})

    # Rüzgar
    if wind_speed > 40:
        tips.append({"icon": "🌪️", "text": "Şiddetli rüzgar, dikkatli olun"})
    elif wind_speed > 25:
        tips.append({"icon": "💨", "text": "Rüzgarlı, şapkanızı tutun"})

    # Nem
    if humidity > 80 and temp > 25:
        tips.append({"icon": "😓", "text": "Bunaltıcı nem, hafif giysiler tercih edin"})

    return tips[:4]  # En fazla 4 tavsiye


def get_current_weather(city):
    try:
        url = f"{BASE_URL}/weather"
        params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "tr"}
        response = requests.get(url, params=params)

        if response.status_code == 404:
            return {"error": "Şehir bulunamadı. Lütfen geçerli bir şehir adı girin."}
        if response.status_code == 401:
            return {"error": "API anahtarı geçersiz. Lütfen API key'inizi kontrol edin."}

        data = response.json()
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
        sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")
        sunrise_dt = datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_dt = datetime.fromtimestamp(data["sys"]["sunset"])
        is_night = datetime.now() < sunrise_dt or datetime.now() > sunset_dt

        weather_id = data["weather"][0]["id"]
        icon = data["weather"][0]["icon"]
        temp = round(data["main"]["temp"])
        wind_speed = round(data["wind"]["speed"] * 3.6, 1)
        wind_deg = data["wind"].get("deg", 0)
        humidity = data["main"]["humidity"]
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]

        weather = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp": temp,
            "feels_like": round(data["main"]["feels_like"]),
            "humidity": humidity,
            "wind_speed": wind_speed,
            "wind_deg": wind_deg,
            "wind_dir": get_wind_direction(wind_deg),
            "description": data["weather"][0]["description"].capitalize(),
            "icon": icon,
            "weather_id": weather_id,
            "pressure": data["main"]["pressure"],
            "temp_min": round(data["main"]["temp_min"]),
            "temp_max": round(data["main"]["temp_max"]),
            "visibility": round(data.get("visibility", 10000) / 1000, 1),
            "clouds": data["clouds"]["all"],
            "sunrise": sunrise,
            "sunset": sunset,
            "is_night": is_night,
            "animation": get_weather_animation(weather_id, icon),
            "uv": get_uv_info(lat, lon),
            "advice": get_weather_advice(temp, weather_id, wind_speed, humidity),
        }
        return weather

    except requests.exceptions.ConnectionError:
        return {"error": "İnternet bağlantınızı kontrol edin."}
    except Exception as e:
        return {"error": f"Bir hata oluştu: {str(e)}"}


def get_today_hourly(city):
    try:
        url = f"{BASE_URL}/forecast"
        params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "tr"}
        response = requests.get(url, params=params)
        if response.status_code != 200: return []
        data = response.json()
        today = []
        for item in data["list"]:
            dt = datetime.fromtimestamp(item["dt"])
            if dt.date() != datetime.now().date(): continue
            today.append({
                "hour": dt.strftime("%H:%M"),
                "temp": round(item["main"]["temp"]),
                "feels_like": round(item["main"]["feels_like"]),
                "description": item["weather"][0]["description"].capitalize(),
                "icon": item["weather"][0]["icon"],
                "humidity": item["main"]["humidity"],
                "wind_speed": round(item["wind"]["speed"] * 3.6, 1),
                "rain_chance": round(item.get("pop", 0) * 100),
            })
        return today
    except Exception:
        return []


def get_forecast(city):
    try:
        url = f"{BASE_URL}/forecast"
        params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "tr"}
        response = requests.get(url, params=params)
        if response.status_code != 200: return []
        data = response.json()
        daily_data = {}

        for item in data["list"]:
            dt = datetime.fromtimestamp(item["dt"])
            date_str = dt.strftime("%Y-%m-%d")
            if dt.date() == datetime.now().date(): continue
            if date_str not in daily_data:
                daily_data[date_str] = {
                    "temps": [], "humidity": [], "wind": [],
                    "descriptions": [], "icons": [],
                    "dt": dt, "pressure": [], "clouds": [], "pop": [],
                    "hourly": [],
                }
            d = daily_data[date_str]
            d["temps"].append(item["main"]["temp"])
            d["humidity"].append(item["main"]["humidity"])
            d["wind"].append(item["wind"]["speed"] * 3.6)
            d["descriptions"].append(item["weather"][0]["description"])
            d["icons"].append(item["weather"][0]["icon"])
            d["pressure"].append(item["main"]["pressure"])
            d["clouds"].append(item["clouds"]["all"])
            d["pop"].append(item.get("pop", 0) * 100)
            d["hourly"].append({
                "hour": dt.strftime("%H:%M"),
                "temp": round(item["main"]["temp"]),
                "feels_like": round(item["main"]["feels_like"]),
                "description": item["weather"][0]["description"].capitalize(),
                "icon": item["weather"][0]["icon"],
                "humidity": item["main"]["humidity"],
                "wind_speed": round(item["wind"]["speed"] * 3.6, 1),
                "rain_chance": round(item.get("pop", 0) * 100),
            })

        forecasts = []
        for date_str in sorted(daily_data.keys())[:5]:
            d = daily_data[date_str]
            dt = d["dt"]
            desc = max(set(d["descriptions"]), key=d["descriptions"].count)
            mid = len(d["icons"]) // 2
            forecasts.append({
                "date": dt.strftime("%d %b"),
                "day_name": get_turkish_day(dt.weekday()),
                "temp": round(sum(d["temps"]) / len(d["temps"])),
                "temp_min": round(min(d["temps"])),
                "temp_max": round(max(d["temps"])),
                "description": desc.capitalize(),
                "icon": d["icons"][mid],
                "humidity": round(sum(d["humidity"]) / len(d["humidity"])),
                "wind_speed": round(sum(d["wind"]) / len(d["wind"]), 1),
                "pressure": round(sum(d["pressure"]) / len(d["pressure"])),
                "clouds": round(sum(d["clouds"]) / len(d["clouds"])),
                "rain_chance": round(max(d["pop"])),
                "hourly": d["hourly"],
            })
        return forecasts
    except Exception:
        return []


def get_turkish_day(n):
    return ["Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"][n]


# ============================================
# ROUTE'LAR
# ============================================

@app.route("/")
def home():
    return render_template("index.html", favorites=get_favorites(request))

@app.route("/weather", methods=["POST"])
def weather():
    city = request.form.get("city", "").strip()
    favorites = get_favorites(request)
    if not city:
        return render_template("index.html", error="Lütfen bir şehir adı girin.", favorites=favorites)
    current = get_current_weather(city)
    if "error" in current:
        return render_template("index.html", error=current["error"], favorites=favorites)
    forecast = get_forecast(city)
    today_hourly = get_today_hourly(city)

    # Arama geçmişini güncelle
    history = get_history(request)
    if city not in history:
        history.insert(0, city)
    history = history[:6]

    resp = make_response(render_template("index.html",
        weather=current, forecast=forecast, today_hourly=today_hourly,
        city=city, favorites=favorites, history=history))
    resp.set_cookie("history", json.dumps(history), max_age=365*24*60*60)
    return resp

@app.route("/api/detect-location")
def detect_location():
    try:
        r = requests.get("http://ip-api.com/json/?lang=tr", timeout=5)
        d = r.json()
        if d["status"] == "success":
            return jsonify({"city": d["city"]})
        return jsonify({"error": "Konum tespit edilemedi"}), 400
    except Exception:
        return jsonify({"error": "Konum servisi kullanılamıyor"}), 500

@app.route("/api/favorites", methods=["POST"])
def toggle_favorite():
    data = request.get_json()
    city = data.get("city", "").strip()
    if not city: return jsonify({"error": "Şehir adı gerekli"}), 400
    favorites = get_favorites(request)
    if city in favorites:
        favorites.remove(city)
        action = "removed"
    else:
        if len(favorites) >= 5:
            return jsonify({"error": "En fazla 5 favori"}), 400
        favorites.append(city)
        action = "added"
    resp = make_response(jsonify({"favorites": favorites, "action": action}))
    resp.set_cookie("favorites", json.dumps(favorites), max_age=365*24*60*60)
    return resp

def get_favorites(req):
    try: return json.loads(req.cookies.get("favorites", "[]"))
    except: return []

def get_history(req):
    try: return json.loads(req.cookies.get("history", "[]"))
    except: return []

if __name__ == "__main__":
    app.run(debug=True)
