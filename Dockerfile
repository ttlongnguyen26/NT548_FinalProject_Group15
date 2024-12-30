FROM python:3.12

WORKDIR /NT548_FINALPROJECT_GROUP15/app

RUN pip install --upgrade pip

# Run and install requirements of main folder
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY /NT548_FinalProject_Group15/app .

EXPOSE 9000

CMD [ "python", "app.py" ]