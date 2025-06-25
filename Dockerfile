FROM python:3.10-slim
RUN apt-get update && apt-get install -y chromium chromium-driver
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV CHROME_BINARY=/usr/bin/chromium
CMD ["python", "app.py"]
