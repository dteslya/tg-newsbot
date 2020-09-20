#!/usr/bin/env python3

import requests
from glom import glom
import datetime
import telebot
bot = telebot.TeleBot("1357156471:AAHwAQe3FCxANbdtLdyPZwqoTuQmDDDsBrQ");


@bot.message_handler(commands=['start','help'])
def start_message(message):
    response_message = (
        "Hello! To get the news for the last 7 days type /news.\n"
    )
    bot.send_message(message.chat.id, response_message, parse_mode="Markdown")


@bot.message_handler(commands=['news'])
def send_text(message):
    articles = news()
    response_message = ''
    for item in articles:
        response_message = response_message + (f"{item['title']}\n{item['url']}\n")
    bot.send_message(message.chat.id, response_message, parse_mode="Markdown")


def news():
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)

    url = ('http://newsapi.org/v2/everything?'
           'domains=www.rbc.ru&'
           'from=' + today.strftime('%Y-%m-%d') + '&to=' + week_ago.strftime    ('%Y-%m-%d') + '&'
           'sortBy=publishedAt&'
           'apiKey=ccdb606181bd4e178269567a0711ff00')
    response = requests.get(url)

    spec = (
        'articles', [{
            'title': 'title',
            'url': 'url',
            'urlToImage': 'urlToImage',
            'publishedAt': 'publishedAt',
        }]
    )
    news = glom(response.json(), spec)
    return news


print('TeleBot. Listening ...')
bot.polling(none_stop=True, interval=0)
