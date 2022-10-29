FROM python:3
COPY . /app
WORKDIR /app
RUN pip3 install flask
RUN pip3 install pymongo
RUN pip3 install requests
ENV FLASK_APP=backend.py
# CMD [ "python3", "-m" , "scheduler.py", "--host=0.0.0.0"]
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
