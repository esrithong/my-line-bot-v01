#from flask import Flask, request, abort
#from linebot import (LineBotApi, WebhookHandler)
#from linebot.exceptions import (InvalidSignatureError)
#from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
from __future__ import unicode_literals

import datetime
import errno
import json
import os
import sys
import tempfile
from argparse import ArgumentParser

from flask import Flask, request, abort, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
#from linebot.models import (
    #MessageEvent, TextMessage, TextSendMessage,
    #SourceUser, SourceGroup, SourceRoom,
    #TemplateSendMessage, ConfirmTemplate, MessageAction,
    #ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    #PostbackAction, DatetimePickerAction,
    #CameraAction, CameraRollAction, LocationAction,
    #CarouselTemplate, CarouselColumn, PostbackEvent,
    #StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    #ImageMessage, VideoMessage, AudioMessage, FileMessage,
    #UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    #MemberJoinedEvent, MemberLeftEvent,
    #FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    #TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    #SeparatorComponent, QuickReply, QuickReplyButton,
    #ImageSendMessage)

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
       quota = line_bot_api.get_message_quota()
       line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='กรุณาระบุจังหวัดและอำเภอที่ต้องการทราบ'),
            ]
       )
   
    
if __name__ == "__main__":
    app.run()
