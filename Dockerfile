# build docker image
# docker build -t jujihoon01/py-study-instagram .

FROM python:3.8.16

COPY . /home/app
WORKDIR /home/app

RUN pip3 install -r requirements.txt

EXPOSE 8000
CMD ["python","manage.py","runserver","0.0.0.0:8000"]

# run docker image
# docker run --name py-study-instagram -p 8000:8000 -d jujihoon01/py-study-instagram