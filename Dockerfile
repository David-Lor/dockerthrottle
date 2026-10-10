FROM python:alpine

RUN apk --no-cache update && \
		apk --no-cache add docker-cli

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app
WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python"]
CMD ["."]
