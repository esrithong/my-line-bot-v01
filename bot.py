import json
import os

from flask import Flask
from flask import request
from flask import make_response

import linebot
from linebot.models import *
from linebot import *
from linebot import (LineBotApi, WebhookHandler)
'''
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
'''
line_bot_api = LineBotApi('ZdDlzPzU2/VBLtW7GCdJq9VFW61tDUXtTKnLJdSLgswx1oS0FODSgBSxpvdIASb2WhmetKizcWP7Rm7VwsGudUgZ8w69PuspqMP3Elauwuz5M4IEqnYCgKDQ1f3UD8fvNnMVlaW3mf8aRJU/nGnTkAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('cb489aedab482e519846c563f4cad0ca')
'''
cred = credentials.Certificate("nogizaka46-chatbot-scca-firebase-adminsdk-p2ju8-b011e4f89b.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
'''
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello'


@app.route('/webhook', methods=['POST'])
def webhook():

    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):

    # Parsing the POST request body into a dictionary for easy access.
    req_dict = json.loads(request.data)

    # Accessing the fields on the POST request boduy of API.ai invocation of the webhook
    intent = req_dict["queryResult"]["intent"]["displayName"]

    if intent == 'A_Test':
        speech = 'ทดสอบสำเร็จ Github !!!!'
        '''
        doc_ref = db.collection(u'Nogizaka46').document(u'A_Test')
        doc = doc_ref.get().to_dict()
        print(doc)

        engName = doc['EngName']
        thName = doc['ThName']
        speech = f'ชื่อภาษาอังกฤษ คือ  {engName} ชื่อภาษาไทย คือ {thName} ทดสอบสำเร็จ'
        '''

    else:

        speech = "ทดสอบไม่สำเร็จ"

    res = makeWebhookResult(speech)

    return res

def makeWebhookResult(speech):

    return {
  "fulfillmentText": speech
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
