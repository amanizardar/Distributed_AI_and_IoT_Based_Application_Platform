FROM python:3
COPY . /app
WORKDIR /app
RUN pip3 install flask
RUN pip3 install PyJWT
RUN pip3 install requests
RUN pip3 install flask_sqlalchemy
RUN pip3 install flask_login
RUN pip3 install pymongo
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
ENTRYPOINT ["python3"]
CMD ["app.py","5001"]
