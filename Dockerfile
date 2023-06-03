FROM 3.11.3-slim

COPY . /home/app
WORKDIR /home/app

RUN pip3 install -r requirements.txt

EXPOSE 8000
CMD ["python","manage.py","runserver","0.0.0.0:8000"]