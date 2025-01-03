FROM python:3.12

WORKDIR /app

RUN pip install --upgrade pip

# Run and install requirements of main folder
COPY ./app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 9000

CMD [ "python", "app.py" ]