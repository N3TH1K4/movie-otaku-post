FROM python:3.8

WORKDIR /movie-otaku-post

COPY . /movie-otaku-post/

CMD python3 bot.py
