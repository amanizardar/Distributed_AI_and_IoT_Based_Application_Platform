FROM python:3
COPY . /app
WORKDIR /app
RUN pip3 install kafka-python
RUN pip3 install flask
RUN pip3 install pymongo
RUN pip3 install requests
RUN pip3 install schedule

ENV FLASK_APP=sensor_registration.py
# CMD [ "python3", "-m" , "sensor_registration.py", "--host=0.0.0.0"]
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
ENTRYPOINT ["python3"]
CMD ["sensor_registration.py","6001"]