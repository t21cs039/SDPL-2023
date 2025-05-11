import requests
from datetime import datetime

def get_weather_data(address):
    api_key = "8fc0c6f4d87f3ed595e66cb523f42b06"
    url = f"http://api.openweathermap.org/data/2.5/forecast"

    params = {
        "q": address,
        "appid": api_key,
        "lang": "ja",
        "units": "metric",
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        weather_data = response.json().get("list", [])
        
        result = []
        noon_entries = [entry for entry in weather_data if entry["dt_txt"].split(' ')[1] == '12:00:00']

        for day_data in noon_entries[:5]:
            # UNIX タイムスタンプを datetime オブジェクトに変換
            date_time = datetime.utcfromtimestamp(day_data["dt"])
            # フォーマットを指定して文字列に変換
            formatted_date_time = date_time.strftime("%Y-%m-%d %H:%M")

            data = {
                "気温": day_data["main"]["temp"],
                "湿度": day_data["main"]["humidity"],
                "天気": day_data["weather"][0]["description"],
                "風速": day_data["wind"]["speed"],
                "日程": formatted_date_time,
            }
            result.append(data)

        return result
    else:
        return None

