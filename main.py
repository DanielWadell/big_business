from flask import Flask, request
import requests
import random
import os
port = int(os.environ.get("PORT", 5000))

used = []
app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def summary():
    response = requests.get("https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-newsfeed", headers={"X-RapidAPI-Key":"29180c2784msha6aad19076e8d65p1dadd5jsn88b8e10ea1cf"},
                                                                                        params={"category":"generalnews"}).json()
    
    print(response)
    response_obj = {
        "fulfillmentText":" ",
        "fulfillmentMessages": [{"text": {"text": []}}],
        "source": " "
    }
    
    for item in response['items']['result']:
        response_obj['fulfillmentMessages'][0]['text']['text'].append(item['summary'][0:350])

        
    rand = random.randint(0, len(response_obj['fulfillmentMessages'][0]['text']['text'])-1)
    if rand not in used:
        response_obj['fulfillmentText'] = response_obj['fulfillmentMessages'][0]['text']['text'][rand]
        used.append(rand)
    else:
        response_obj['fulfillmentText'] = 'No more information updates'
        used.clear()

    return response_obj
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)