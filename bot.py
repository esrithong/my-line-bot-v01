import json
import os
from flask import Flask
from flask import request
from flask import make_response


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
def MainFunction():

    #Getting intent from Dailogflow
    question_from_dailogflow_raw = request.get_json(silent=True, force=True)

    #Call generating_answer function to classify the question
    answer_from_bot = generating_answer(question_from_dailogflow_raw)
    
    #Make a respond back to Dailogflow
    r = make_response(answer_from_bot)
    r.headers['Content-Type'] = 'application/json' #Setting Content Type

    return r

def generating_answer(question_from_dailogflow_dict):

    #Print intent that recived from dialogflow.
    print(json.dumps(question_from_dailogflow_dict, indent=4 ,ensure_ascii=False))

    #Getting intent name form intent that recived from dialogflow.
    intent_group_question_str = question_from_dailogflow_dict["queryResult"]["intent"]["displayName"] 

    #Select function for answering question
    if intent_group_question_str == 'กินอะไรดี':
        answer_str = menu_recormentation()
    elif intent_group_question_str == 'BMI - Confirmed W and H': 
        answer_str = BMI_calculation(question_from_dailogflow_dict)
    else: answer_str = "ผมไม่เข้าใจ คุณต้องการอะไร"

    #Build answer dict 
    answer_from_bot = {"fulfillmentText": answer_str}
    
    #Convert dict to JSON
    answer_from_bot = json.dumps(answer_from_bot, indent=4) 
    
    return answer_from_bot

def menu_recormentation(): #Function for recommending menu
    menu_name = 'สุกี้แห้ง'
    answer_function = menu_name + ' สิ น่ากินนะ'
    return answer_function

def BMI_calculation(respond_dict): #Function for calculating BMI

    #Getting Weight and Height
    weight_kg = float(respond_dict["queryResult"]["outputContexts"][2]["parameters"]["Weight.original"])
    height_cm = float(respond_dict["queryResult"]["outputContexts"][2]["parameters"]["Height.original"])
    
    #Calculating BMI
    BMI = weight_kg/(height_cm/100)**2
    if BMI < 18.5 :
        answer_function = "คุณผอมเกินไปนะ"
    elif 18.5 <= BMI < 23.0:
        answer_function = "คุณมีนำ้หนักปกติ"
    elif 23.0 <= BMI < 25.0:
        answer_function = "คุณมีนำ้หนักเกิน"
    elif 25.0 <= BMI < 30:
        answer_function = "คุณอ้วน"
    else :
        answer_function = "คุณอ้วนมาก"
    return answer_function

if __name__ == "__main__":
    app.run()
