from requests import get
import requests
import json
from enum import Enum
ip = get("https://api.ipify.org").text
# print("My public IP address : ", ip)

Loca_key = "629c0582301b2c6479a51dbcecf88a84"
url = "http://api.ipstack.com/"+ip+"?access_key=" + Loca_key
r = requests.get(url)
j = json.loads(r.text)
# print(j)
# print("\n")

lon = j['longitude']  # 경도
lat = j['latitude']  # 위도
# 경도,위도 확인
# print("경도:", round(lon, 5), " 위도:", round(lat, 5))

Weath_key = "a486d675c4fcd3133f525612ff8a2e85"
api = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={Weath_key}"

result = requests.get(api)
print(result.text, "\n", "\n")
data = json.loads(result.text)

weather = data["weather"][0]["main"]
#  print(type(weather)) -> str
#  print(weather)


class WEATHER(Enum):

    Thunderstorm = 0  # 뇌우
    Drizzle = 1  # 이슬비
    Rain = 2
    Snow = 3
    Mist = 4  # 안개
    Haze = 5  # 실안개
    Dust = 6  # 꽃가루?
    Fog = 7  # 안개
    Clear = 8
    Clouds = 9

    def compare_weather(self, other_weather):
        if self.name == other_weather:
            return True
        else:
            return False


for weather_type in WEATHER:
    if weather_type.compare_weather(weather):
        print(weather_type.value)



