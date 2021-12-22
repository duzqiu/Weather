#!/usr/bin/python
# -*- coding:utf8 -*- 

import requests
import json

class PostWeatherMsg(object):

    def __init__(self):
        self.weatherUrl = "https://restapi.amap.com/v3/weather/weatherInfo"
        self.weatherKey = "e851ac44c1f52e6e8143df71e58181ae"
        self.extensions = "base" # base实况 all预报
        self.weatherCity = "310100" # 310100
        self.weatherOutput = "JSON"
        
        self.tokenUrl = "https://api.weixin.qq.com/cgi-bin/token"
        self.tokenGrantType = "client_credential"
        self.tokenAppid = "wx93f0cc08624df826"
        self.tokenSecret = "e69da013773afc3f784a4db9ca9504df"

        self.sendUrl = "https://api.weixin.qq.com/cgi-bin/message/template/send"


    def get_weather_base(self):
        params = {
            "key": self.weatherKey,
            "city": self.weatherCity,
            "extensions": "base",
            "output": self.weatherOutput
        }

        resp = requests.get(self.weatherUrl, params=params)
        resp_json = resp.json()
        resp_city = resp_json[ "lives"][0]['province'] + resp_json[ "lives"][0]['city'] # 省份城市
        resp_weather = resp_json['lives'][0]['weather'] # 目前天气
        resp_temperature = resp_json['lives'][0]['temperature'] # 目前温度
        resp_winddirection = resp_json['lives'][0]['winddirection'] # 目前风向
        resp_windpower = resp_json['lives'][0]['windpower'] # 目前风力等级
        resp_humidity = resp_json['lives'][0]['humidity'] # 目前空气湿度
        resp_reporttime = resp_json['lives'][0]['reporttime'] # 预报发布时间
        text = f"""   城市：{resp_city}
    预报时间：{resp_reporttime}
    预报天气：{resp_weather}
    目前温度：{resp_temperature}℃
    目前风向：{resp_winddirection}
    目前风力等级：{resp_windpower}级
    目前空气湿度：{resp_humidity}"""
        return text

    def get_weather_all(self):
        params = {
            "key": self.weatherKey,
            "city": self.weatherCity,
            "extensions": "all",
            "output": self.weatherOutput
        }

        resp = requests.get(self.weatherUrl, params=params)
        resp_json = resp.json()
        resp_city = resp_json['forecasts'][0]['province'] + resp_json['forecasts'][0]['city'] #省份城市
        resp_reporttime = resp_json['forecasts'][0]['reporttime'] # 预报发布时间
        resp_weather_list = resp_json['forecasts'][0]['casts'] # 未来几天天气列表
        # resp_weather01 = resp_weather_list[0]
        resp_weather02 = resp_weather_list[1]
        # resp_weather03 = resp_weather_list[2]
        # resp_weather04 = resp_weather_list[3]
        resp_weather02_date = resp_weather02['date'] # 日期
        resp_weather02_week = resp_weather02['week'] # 星期几
        resp_weather02_dayweather = resp_weather02['dayweather'] # 白天天气现象
        resp_weather02_nightweather = resp_weather02['nightweather'] # 晚间天气现象
        resp_weather02_daytemp = resp_weather02['daytemp'] # 白天温度
        resp_weather02_nighttemp = resp_weather02['nighttemp'] # 晚间温度
        resp_weather02_daywind = resp_weather02['daywind'] # 白天风向
        resp_weather02_nightwind = resp_weather02['nightwind'] # 晚间风向
        resp_weather02_daypower = resp_weather02['daypower'] # 白天风力
        resp_weather02_nightpower = resp_weather02['nightpower'] # 晚间风力
        text = f"""   城市：{resp_city}
    预报时间：{resp_reporttime}
    预报日期：{resp_weather02_date}    星期几：{resp_weather02_week}
    白天天气：{resp_weather02_dayweather}         晚间天气：{resp_weather02_nightweather}
    白天温度：{resp_weather02_daytemp}℃    晚间温度：{resp_weather02_nighttemp}℃
    白天风向：{resp_weather02_daywind}     晚间风向：{resp_weather02_nightwind}
    白天风力：{resp_weather02_daypower}级    晚间风力：{resp_weather02_nightpower}级
        """
        return text
    
    def get_send_token(self):
        params = {
            "grant_type": self.tokenGrantType,
            "appid": self.tokenAppid,
            "secret": self.tokenSecret
        }

        resp = requests.get(self.tokenUrl, params=params)
        token = resp.json()['access_token']
        return token

    def send_weather(self, token, text, template_id):
        data = {
            "touser": 'og3la5lJmkKcsYxo7nE2eR6ZgTRg',
            "template_id": template_id,
            "data": {
                "content":{
                    "value": text,
                    "color": "#FFFFF",
                    } 
                }
            }
        resp = requests.post(
            self.sendUrl, params={'access_token': token}, 
            data=json.dumps(data,ensure_ascii=False).encode('utf-8')
            )

if __name__ == '__main__':
    today_id = "N2-wD6MY2BTJV2jwadrWhiaHnO6RjrLl6Xp0W2ntn1M"
    # tom_id = "WFoNGl5nWYbYn-hvmbYqn3y3MOuLWJB4TCxheJpm_fg"
    weather = PostWeatherMsg()
    send_token = weather.get_send_token()
    send_base_text = weather.get_weather_base()
    # send_all_text = weather.get_weather_all()
    weather.send_weather(send_token, send_base_text, today_id)
    # weather.send_weather(send_token, send_all_text, tom_id)
    