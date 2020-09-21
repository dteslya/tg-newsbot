FROM python:3.7-alpine
RUN addgroup -S bot && adduser --home /home/bot -S bot -G bot
WORKDIR /home/bot
COPY . .
RUN chown -R bot:bot ./
RUN pip install -r requirements.txt
USER bot
CMD "./newsbot.py"