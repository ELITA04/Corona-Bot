FROM rasa/rasa-sdk:1.10.0

USER root

WORKDIR /app

COPY docker/requirements.txt /app

COPY actions.py /app

COPY api_modules /app/api_modules

RUN pip3 install -r requirements.txt

CMD ["start", "--actions", "actions"]

USER 1001
