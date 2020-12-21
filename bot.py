from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)

app = Flask(__name__)

line_bot_api = LineBotApi('GUVQt/DB7ceOg6lfpFiMBeR5NamR83+nudAjLKI4D1LbmLj5WvXYms7RZWLWFs3eT+tzRaF6W6gjs2teKpD1I/IuPLV9+dhVIGs65vy1+d3kbsOJAP+5XJowpCX5ds8HGS0GjBQ8U2AZlMP8epTPdQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c375fa7eadfb0997e7729120e4dccc10')

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
