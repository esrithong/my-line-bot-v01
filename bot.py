import json
import os

from flask import Flask
from flask import request
from flask import make_response

import linebot
from linebot.models import *
from linebot import *
from linebot import (LineBotApi, WebhookHandler)

# line_bot_api = Channel access token
# handler = Channel secret
line_bot_api = LineBotApi('ZdDlzPzU2/VBLtW7GCdJq9VFW61tDUXtTKnLJdSLgswx1oS0FODSgBSxpvdIASb2WhmetKizcWP7Rm7VwsGudUgZ8w69PuspqMP3Elauwuz5M4IEqnYCgKDQ1f3UD8fvNnMVlaW3mf8aRJU/nGnTkAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('cb489aedab482e519846c563f4cad0ca')

app = Flask(__name__)


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
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run()
