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
        url = "https://data.tmd.go.th/nwpapi/v1/forecast/location/hourly/place"

        querystring = {"province":u"นครปฐม", "amphoe":u"เมืองนครปฐม", "fields":"tc, rh, rain, ws10m"}

        headers = {
            'accept': "application/json",
            'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjMxZTY0MDU0NzFlOTBhY2E0ZDE4NTJmNWY3MjBmNzlkZDEyYWJlZWM2MmY0YzcyNDk4YjE0ZmFlZjFiMzcyNDZkMWE2OWFlN2U1Y2FiY2QyIn0.eyJhdWQiOiIyIiwianRpIjoiMzFlNjQwNTQ3MWU5MGFjYTRkMTg1MmY1ZjcyMGY3OWRkMTJhYmVlYzYyZjRjNzI0OThiMTRmYWVmMWIzNzI0NmQxYTY5YWU3ZTVjYWJjZDIiLCJpYXQiOjE2MTIwMDkzNzEsIm5iZiI6MTYxMjAwOTM3MSwiZXhwIjoxNjQzNTQ1MzcxLCJzdWIiOiI2ODEiLCJzY29wZXMiOltdfQ.WYE4mH6RVRO2el2rxgbtr1TxmTgxRS3N9147P1M889k9Ds2H4VIXrO6SbljNn_JB_yohEZ2QIYN-DfUQvipjY5LBs-iJCV9V0PT-DdmLL6fRw2zVVtaoDA_PzrJWmMurQTcmlaDPsNDGPwK3INESW5-5ZMg0Ssp4IGzGi2CFgfe_3rva4_pa64gCBd4GeKVwrLqaO_ds-8787pwsAMhA8EO61qCL4AX1H7WYis86RO4nAquqTq6OyJ-zoOyokQHfYbDfcYo5GrZCISGr9HwtwbKhbou3XQh2fKjXAJMuIyjYwkXfwaifDAYmWc-mSYyEWPWgjmFzbCfzV65EEJtHRydGZsXpFyHPzbcdfKuAYQxfMbZ8l8YTxs22wRNqNkz6TPJlJMeQ7Cr_J_SUYDFgv4xNPqRpoVemjUZF2rCx7TyObPBewrsLzkUQ66OvAr5afadlZsgBstu-8l-lx57JmveMALLEWbfSpBcY89_a36kaxDUontS0n1W53EEyd-8Wxwj9FE02LVDfxt6Clb6dJtF9tfV8QdbMYHUErCMhMbniyyUwcU44FRfrbWSL7qyf6Q_wwwk34dYfliqGbhC5yJEByQ6vM3uz8E_KQeEjQtbyMHxU2TMPyX3YWc3dTHDnPfFDRSozI7rbmqC4fbz6aoFs5hZQfoSuo4cViM0G0Qc",
        }
        data = requests.request("GET", url, headers=headers, params=querystring).json()
        #print (data)


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
