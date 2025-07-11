FROM python:3.13-slim
RUN apt update && apt install -y git

WORKDIR /build

COPY ./requirements.txt /build/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN apt purge -y git

COPY ./app /build/app

VOLUME /build/data

EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]