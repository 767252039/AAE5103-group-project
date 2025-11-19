import requests
from typing import Optional, Dict, Any

def deepseek_chat(input_content):
    API_KEY = "YOUR-API-KEY-HERE" # Replace with your actual Deepseek API key
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "you are a chat robot in an airlines website"},
            {"role": "user", "content": input_content}
        ],
        "stream": False
    }
    print('Wait for a minute, I need time to think...')
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        print(result['choices'][0]['message']['content'])
    else:
        print("requests fail：", response.status_code)
    print(response.json())

def get_hko_weather(data_type: str = "fnd", lang: str = "en") -> Optional[Dict[Any, Any]]:
    base_url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"
    params = {
        "dataType": data_type,
        "lang": lang
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()
        response.raise_for_status()
        return data

    except Exception as e:
        print(f"error occurs!  {e}")
        return None

def current_weather_info(data: Dict[str, Any]):
    if data.get("soilTemp"):
        print(f"Today's temperature: {data.get('soilTemp')[0].get('value')} °C")

def three_days_weather(data: Dict[str, Any]):
    if data.get('generalSituation'):
        print(f"General infomation :\n\t⚠️{data['generalSituation']}")

    if data.get('weatherForecast'):
        forecast_data = data.get('weatherForecast')
        day_1 = forecast_data[0]
        print(f'Date : {day_1.get("week")}, {day_1.get("forecastDate")[6:8]}/{day_1.get("forecastDate")[5:7]}/{day_1.get("forecastDate")[0:4]}')
        print(f'\t🌡️Temperature: {day_1.get("forecastMintemp").get("value")}~{day_1.get("forecastMaxtemp").get("value")} °C')
        day_2 = forecast_data[1]
        print(f'Date : {day_2.get("week")}, {day_2.get("forecastDate")[6:8]}/{day_2.get("forecastDate")[5:7]}/{day_2.get("forecastDate")[0:4]}')
        print(f'\t🌡️Temperature: {day_2.get("forecastMintemp").get("value")}~{day_2.get("forecastMaxtemp").get("value")} °C')
        day_3 = forecast_data[2]
        print(f'Date : {day_3.get("week")}, {day_3.get("forecastDate")[6:8]}/{day_3.get("forecastDate")[5:7]}/{day_3.get("forecastDate")[0:4]}')
        print(f'\t🌡️Temperature: {day_3.get("forecastMintemp").get("value")}~{day_3.get("forecastMaxtemp").get("value")} °C')


if __name__ == "__main__":
    weather_data = get_hko_weather()
    three_days_weather(weather_data)
    current_weather_info(weather_data)
    while True:
        content = input("I'm an airlines assistant. How can I help you?\n")
        deepseek_chat(content)