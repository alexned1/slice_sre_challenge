FROM python:3.8.5-slim-buster

ENV APP_DIR='/app-sidecar'
WORKDIR $APP_DIR

COPY . $APP_DIR

RUN pip3 install requests polling

CMD ["/app-sidecar/monitor-metrics.py"]