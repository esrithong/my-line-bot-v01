from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)

app = Flask(__name__)
# line_bot_api = Channel access token
# handler = Channel secret
line_bot_api = LineBotApi('4OPjwBiZQWRlAmGTII1pdeLdygBdE7fBW9hkdsZ8t3SaJ/fnkCYEnJzC24mD0bBZtdEAM5UxZ7egUEAf7gjmQHLUUz8Lv4cjGwC3OZ/vAJmuXW1YYP/yvNo08cgrC0ZqOHB5aB0QC2n3g6DiCZFtkgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('501aad4d05afc7da48e8c5400c2f61e1')

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/webhook", methods=['POST'])
def webhook():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
    

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    #line_bot_api.reply_message(
        #event.reply_token,
        #TextSendMessage(text=event.message.text))
    
   text = event.message.text
    
   if text == 'พยากรณ์อากาศ':
       #quota = line_bot_api.get_message_quota()
       line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='กรุณาระบุจังหวัดและอำเภอที่ต้องการทราบ'),
            ]
       )
   
    elif text == 'นครปฐม เมืองนครปฐม':
        #quota = line_bot_api.get_message_quota()
        import requests
        import pandas as pd
        import warnings
        warnings.filterwarnings('ignore')
        from pythainlp import sent_tokenize, word_tokenize
        t = sent_tokenize(text, engine="whitespace")
        prov = t[0]
        amp = t[1]
        print(prov , amp)
        
        url = "https://data.tmd.go.th/nwpapi/v1/forecast/location/hourly/place"

        querystring = {"province":prov, "amphoe":amp, "fields":"tc, rh, rain, ws10m"}

        headers = {
            'accept': "application/json",
            'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjNlMTFlZmNiNDhhYzYzNTA3NjRkMzE4OGE4Yjk4ZTBkM2NiNTU5NTIxMTQxOThiYzU3MzJiMDA0ZTg4MTBkZmQ2ZTY1MjQyMzQxNjJjNjFlIn0.eyJhdWQiOiIyIiwianRpIjoiM2UxMWVmY2I0OGFjNjM1MDc2NGQzMTg4YThiOThlMGQzY2I1NTk1MjExNDE5OGJjNTczMmIwMDRlODgxMGRmZDZlNjUyNDIzNDE2MmM2MWUiLCJpYXQiOjE1NzcwODYyNDMsIm5iZiI6MTU3NzA4NjI0MywiZXhwIjoxNjA4NzA4NjQzLCJzdWIiOiI2ODEiLCJzY29wZXMiOltdfQ.Q2QVxHiGf9L-mEAk_dwTdjtoaoseSYBRW6M-OqdSYwCtVH5qKCq01LO6iBlz1mWvkkoaWy2-tzXInF5sPHxSMqAAsbZQnQ-0G4jnaQ1WDFE02rl2a92pgroLn99X2BrX2K_3kvEOgHymt0-AUXQ8DWH5vwwsLwB9oAa5KN6C7d2p4voNjhiN0a2hAJG0lFp2v-sDPQvqvZdH5taUZV-hGPrD-3mCYEjh6yPdepaBKBbHfyXOtjCskeyQUZ40qA989SbK7-3YvF4ZIe9RZIeLUYfrLbZnjDPeERWJRoaBIs7nVg1FzAc19v7aBMfo30ytLtNbXcQN42u2GQDN1wuDt5H_Hvac0e4gYuAevvJeumO2XJUO-aaR6eh5wD0ksEq1deeCm5bFGzaISdDscmCFkPxxDjy0_OD2qpz7rs97DLmfke6ihQYX1lLnYTi5QNKBQl7XEyWbU-2Rg17G2QRo1ufNMOOjedv9nBCbvBn3RBACR3G-nEVUbo8sQk8NoS9sYNzyKFcEBkyOXJ8W4vKF9u0Z0x24xyUbYXwjRmvTLq8EJGHrVu3gJs2IE1Y51ba019aJbNnsLrac1TrO2HF4NilDWc0K4k3f6UqyhBM2AInp7hpbRmRT1xnnGXxR0qE5EXzqpEaqEZ0r0XV8r8Zvf0D4l9F2XIQCcAa2p9zOFw4",
        }
        data = requests.request("GET", url, headers=headers, params=querystring).json()
        print (data)


        prov = data['WeatherForecasts'][0]['location']['province']
        lat  = data['WeatherForecasts'][0]['location']['lat']
        lon  = data['WeatherForecasts'][0]['location']['lon']
        temp = data['WeatherForecasts'][0]['forecasts'][0]['data']['tc']
        humi = data['WeatherForecasts'][0]['forecasts'][0]['data']['rh']
        rain = data['WeatherForecasts'][0]['forecasts'][0]['data']['rain']
        wind = data['WeatherForecasts'][0]['forecasts'][0]['data']['ws10m']
        time = data['WeatherForecasts'][0]['forecasts'][0]['time']

       
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='อุณหภูมิ '+"%.2f"%temp),
                TextSendMessage(text='ความชื้น '+"%.2f"%humi),
                TextSendMessage(text='ปริมาณฝน'+"%.2f"%rain),
                TextSendMessage(text='ความเร็วลม'+"%.2f"%wind),
                TextSendMessage(text='time:'+time)
            ]
        )

        
        
if __name__ == "__main__":
    app.run()
