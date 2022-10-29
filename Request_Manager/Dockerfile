FROM python:3
COPY . /app
WORKDIR /app
RUN pip3 install flask
RUN pip3 install PyJWT
RUN pip3 install pymongo
RUN pip3 install requests
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
ENTRYPOINT ["python3"]
CMD ["app.py","5000"]
