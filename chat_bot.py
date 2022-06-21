import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import pandas as pd
import telegram
from CBF import CBF
from random_keyword import print_random_keyword

token = '5569336973:AAHuk9BSs66Uq2fv7kuwNLCPVshMthsMXvA'
id = '5541102425'

bot = telegram.Bot(token=token)   # 봇 정의

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()

df = pd.read_pickle("pickle_review_data_frame")

'''
1. 사용자에게 키워드 입력을 요구
2. 사용자가 입력한 키워드를 받아서 처리
3-1. 키워드가 있을 경우, 키워드에 해당되는 장소 반환
3-2. 키워드가 없을 경우, 키워드를 랜덤으로 5개 제공, 키워드 다시 입력 요구
'''

# 1 -> 나중에 문구 수정
bot.send_photo(chat_id=id, photo=open('main.PNG', 'rb'))
bot.sendMessage(chat_id=id, text="가고 싶은 여행지의 키워드를 입력해주세요.")

def handler(update, context):
    # 2
    user_text = update.message.text # 사용자가 보낸 메세지

    k_list = sum(df['키워드'].to_list(), [])
    # 3-1.
    if user_text in k_list:
        best_tourist_attractions, honey_tourist_attractions = CBF(user_text, df)

        for i in best_tourist_attractions:
            bot.sendMessage(chat_id=id, text=f"추천하는 여행지는: {i}")  # 추천 여행지

        for j in honey_tourist_attractions:
            bot.sendMessage(chat_id=id, text=f"꿀 여행지는: {j}")  # 꿀 여행지

    #3-2
    else:
        key_list = print_random_keyword(k_list)
        bot.sendMessage(chat_id=id, text="검색한 키워드를 찾을 수 없습니다. 시스템의 추천 키워드는 다음과 같습니다.")
        for k in key_list:
            bot.sendMessage(chat_id=id, text=f"{k}")
        bot.sendMessage(chat_id=id, text="다시 가고 싶은 여행지의 키워드를 입력해주세요.")

echo_handler = MessageHandler(Filters.text, handler)
dispatcher.add_handler(echo_handler)
