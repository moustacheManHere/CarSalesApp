FROM python:3.11.5
RUN apt-get update -y
RUN apt-get install build-essential -y

WORKDIR /app-docker
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]