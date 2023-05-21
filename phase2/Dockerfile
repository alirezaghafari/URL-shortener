FROM python:3.11.0a6-alpine3.15

ENV PORT=6010
ENV TIME_TO_EXPIRE=5
ENV API_ENDPOINT="https://api.rebrandly.com/v1/links"
ENV API_KEY="209c1dd479d6432580e07ddecae1aab8"
ENV URL="https://www.youtube.com/channel/UCHK4HD0ltu1-I212icLPt3g"

WORKDIR .
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python url-shortener.py   
