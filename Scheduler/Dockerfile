FROM python:3
COPY . /app
WORKDIR /app
RUN pip3 install flask
RUN pip3 install pymongo
RUN pip3 install schedule
RUN pip3 install requests
RUN pip3 install uuid
ENV FLASK_APP=schedule_request.py
# CMD [ "python3", "-m" , "scheduler.py", "--host=0.0.0.0"]
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
ENTRYPOINT ["python3"]
CMD ["schedule_request.py","5011"]
