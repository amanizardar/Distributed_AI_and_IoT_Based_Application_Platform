FROM python:3
COPY . /app
WORKDIR /app
RUN pip3 install flask
RUN pip3 install paramiko
RUN pip3 install numpy
RUN pip3 install pymongo
RUN pip3 install schedule
RUN pip3 install requests
#RUN pip3 install distutils
RUN pip install azure-storage-file-share
#ENV FLASK_APP=dashboard.py
# CMD [ "python3", "-m" , "scheduler.py", "--host=0.0.0.0"]
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
ENTRYPOINT ["python3"]
CMD ["Dashboard.py","5005"]
