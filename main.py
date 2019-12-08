from flask import Flask, request
import requests
import os
port = int(os.environ.get("PORT", 5000))
from flask_ngrok import run_with_ngrok
from flask_assistant import Assistant, tell

    # to see the full request and response objects
    # set logging level to DEBUG
import logging
logging.getLogger('flask_assistant').setLevel(logging.DEBUG)

app = Flask(__name__)
# run_with_ngrok(app)
assist = Assistant(app, project_id='GOOGLE_CLOUD_PROJECT_ID')

@assist.action('Demo')
def hello_world():
    speech = 'Microphone check 1, 2 what is this?'
    return tell(speech)

@app.route('/webhook')
def summary():
    response = requests.get("https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-news", headers={"X-RapidAPI-Key":"29180c2784msha6aad19076e8d65p1dadd5jsn88b8e10ea1cf"},
                                                                                        params={"category":"NBEV"}).json()
    
    print(response)
    response_obj = {
        "fulfillmentText":" ",
        "fulfillmentMessages": [{"text": {"text": []}}],
        "source": " "
    }
    
    for item in response['items']['result']:
        response_obj['fulfillmentMessages'][0]['text']['text'].append(item['summary'][0:250])
        

    # return response['items']['result'][0]['summary']
    return response_obj
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)