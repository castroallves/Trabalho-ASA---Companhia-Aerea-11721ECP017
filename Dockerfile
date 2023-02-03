# syntax=docker/dockerfile:1
FROM ubuntu
RUN apt-get update && apt-get upgrade
RUN apt-get install python3-pip -y && apt-get install python-dev-is-python3 -y
#&& apt-get install python-dev -y
RUN apt-get install sqlite3 libsqlite3-dev -y
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY  app.py database.py storage.db models.py routes.py settings.py requirements.txt /root/folder/
WORKDIR /root/folder/
EXPOSE 5000
RUN pip install -r requirements.txt
RUN pip install flask
CMD ["python","app.py"]
