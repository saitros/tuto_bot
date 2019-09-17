# -*- coding: utf-8 -*-

import requests
from flask import Flask, request, Response
from Tuto02 import find_user_row, user_counter
import numpy as np

#delete_msg_url = 'https://api.telegram.org/bot{API_KEY}/deleteMessage'.format(API_KEY=API_KEY)
API_KEY = '895060666:AAFgAc-apPHZWK3Pi8lNHIB8iGCgfFfxmPg'

app = Flask(__name__)

#def msg_delete(chat_id, msg_id):
#    request = Request(delete_msg_url)
#    request.get_method = lambda: 'GET'
#    response_body = urlopen(request).read().decode('utf-8')
#    print(response_body)


def parse_message(message):
    """
    telegram 에서 data 인자를 받아옴
    data 내부 구조를 이해해야 한다.
    
    Retuen :    
    chat_id = 사용자 아이디 코드
    msg = 사용자 대화 내용    
    """
    chat_id = message['message']['chat']['id']
    msg = message['message']['text']
    name = message['message']['chat']['last_name'] + message['message']['chat']['first_name']
    #                          '이'                 +  '준호'
    # = '이준호'
    return chat_id, msg, name


def send_message(chat_id, text='hello'):
    """
    chat_id : 사용자 아이디 코드
    text : 사용자 대화내용

    Return :
    함수에 변수를 할당할때 text='hello' 라고 선언
    --> text에 관련된 값이 전달되지 않으면 hello를 default로 사용
    
    사용자에게 메세지를 보내는 내용의 함수   
    """
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)
    params = {'chat_id': chat_id, 'text': '안녕!'}

    response = requests.post(url, json=params)
    print(response)
    return response


def send_welcome_msg(chat_id):
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)
    welcome_msg_set = ['어서와! 챗봇은 처음이지?', '안녕! 반가워 처음이지 챗봇은?', 'ㅎㅇ', '처음뵙겠습니다. 챗봇이라고합니다.']
    params = {'chat_id': chat_id, 'text': np.random.choice(welcome_msg_set)}
    requests.post(url, json=params)


# 경로 설정, URL 설정
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        message = request.get_json()
                
        # parse_message 함수는 두가지 return 값을 가진다 (chat_id, msg)
        # 순서대로 chat_id, msg의 변수로 받아준다.
        chat_id, msg, name = parse_message(message)

        user_row, is_welcome = find_user_row(chat_id, name)
        
        user_counter(user_row)
        
        if is_welcome:
            send_welcome_msg(chat_id)
            break
        
        
        # send_message 함수에 두가지 변수를 전달
        send_message(chat_id, msg)
        
        # 여기까지 오류가 없으면 서버상태 200 으로 반응
        
        return Response('ok', status=200)
    else:
        return 'Hello World!'

#saitros_bot
        
@app.route('/about')
def about():
  return 'About page'


if __name__ == '__main__':
    app.run(port = 5000)

