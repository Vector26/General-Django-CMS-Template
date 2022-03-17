FROM python:3.8-alpine
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  
COPY ./requirements.txt .
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add jpeg-dev zlib-dev libjpeg
RUN pip install -r requirements.txt
COPY ./src .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]