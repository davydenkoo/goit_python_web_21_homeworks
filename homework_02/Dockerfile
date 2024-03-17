FROM python:3.11.5-alpine

WORKDIR /app

COPY . .

RUN pip install colorama

ENTRYPOINT [ "python", "personal_assistant_bot/main.py" ]
