FROM ruby:2.4-slim-stretch

ENV APP_DIR='/app'
WORKDIR $APP_DIR

COPY . /app

RUN apt-get update && \
    apt-get install -y build-essential && \
    bundle install --jobs 20

CMD ["puma", "--config",  "puma.rb", \
             "--bind",    "tcp://localhost:4567", \
             "--log-requests"]
