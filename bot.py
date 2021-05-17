from flask import Flask, request
from linebot import *

app = Flask(__name__)

line_bot_api = LineBotApi('4OPjwBiZQWRlAmGTII1pdeLdygBdE7fBW9hkdsZ8t3SaJ/fnkCYEnJzC24mD0bBZtdEAM5UxZ7egUEAf7gjmQHLUUz8Lv4cjGwC3OZ/vAJmuXW1YYP/yvNo08cgrC0ZqOHB5aB0QC2n3g6DiCZFtkgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('501aad4d05afc7da48e8c5400c2f61e1')

@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    # print(body)
    req = request.get_json(silent=True, force=True)
    intent = req["queryResult"]["intent"]["displayName"]
    text = req['originalDetectIntentRequest']['payload']['data']['message']['text']
    reply_token = req['originalDetectIntentRequest']['payload']['data']['replyToken']
    id = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    disname = line_bot_api.get_profile(id).display_name

    print('id = ' + id)
    print('name = ' + disname)
    print('text = ' + text)
    print('intent = ' + intent)
    print('reply_token = ' + reply_token)

    reply(intent, text, reply_token, id, disname)

    return 'OK'

def reply(intent,text,reply_token,id,disname):
    if intent == 'กินอะไรดี':
        text_message = TextSendMessage(text='ผัดไทยไหม')
        line_bot_api.reply_message(reply_token,text_message)

if __name__ == "__main__":
    app.run()
