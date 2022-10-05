FROM python:3.8

WORKDIR /movie-otaku-post
COPY requirements.txt /movie-otaku-post/
RUN pip3 install -r requirements.txt
COPY . /movie-otaku-post/

CMD python3 bot.py
