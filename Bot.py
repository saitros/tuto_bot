# -*- coding: utf-8 -*-

import json
import requests
from flask import Flask, request, Response


app = Flask(__name__)


# 경로 설정, URL 설정
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        message = request.get_json()
        
        with open('response.json', 'w', encoding='UTF-8') as f:
            json.dump(message, f, indent=4, ensure_ascii=False)
                     
        chat_id, msg = parse_message(message)
        send_message(chat_id, msg)
        
        return Response('ok', status=200)
    else:
        return 'Hello World!'

@app.route('/Home')
def myhome():
    return  'myHome'

# Python 에서는 실행시킬때 __name__ 이라는 변수에
# __main__ 이라는 값이 할당
if __name__ == '__main__':
    app.run(port = 5000)
