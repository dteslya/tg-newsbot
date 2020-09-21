#!/usr/bin/env python3

import requests
from glom import glom
import datetime
import telebot
import logging

bot = telebot.TeleBot("1357156471:AAHwAQe3FCxANbdtLdyPZwqoTuQmDDDsBrQ")

# Logging
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)  # Outputs debug messages to console.


@bot.message_handler(commands=["start", "help"])
def start_message(message):
    response_message = "Hello! To get the news for the last 7 days type /news.\n"
    bot.send_message(message.chat.id, response_message, parse_mode="Markdown")


@bot.message_handler(commands=["news"])
def send_text(message):
    articles = news()
    response_message = ""
    for item in sorted(articles, key=lambda i: i["publishedAt"]):
        date = datetime.datetime.strptime(item["publishedAt"], "%Y-%m-%dT%H:%M:%S%z")
        date_f = date.strftime("%b %d, %Y")
        response_message = response_message + (
            f"🔹 [{date_f}] {item['source']['name']} [{item['title']}]({item['url']})\n\n"
        )
    bot.send_message(message.chat.id, response_message, parse_mode="Markdown", disable_web_page_preview=True)


def news():
    """Get news from specified sources for the last 7 days"""
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)

    url = "http://newsapi.org/v2/everything?"
    parameters = {
        "pageSize": 10,  # maximum is 100
        "apiKey": "ccdb606181bd4e178269567a0711ff00",  # your own API key
        "from": today.strftime("%Y-%m-%d"),
        "to": week_ago.strftime("%Y-%m-%d"),
        "domains": ["www.rbc.ru", "meduza.io", "bbc.com"],
        # "domains": ["meduza.io", "bbc.com"],
        "language": "ru",
        "sortBy": "popularity",
    }
    response = requests.get(url, params=parameters)

    spec = (
        "articles",
        [
            {
                "title": "title",
                "url": "url",
                "urlToImage": "urlToImage",
                "publishedAt": "publishedAt",
                "source": "source",
            }
        ],
    )
    news = glom(response.json(), spec)
    return news


print("TeleBot. Listening ...")
bot.polling(none_stop=True, interval=0)
