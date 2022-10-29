FROM bitnami/azure-cli:latest
COPY . /app
WORKDIR /app
USER root
RUN apt-get update
RUN apt-get install -y python-pip
RUN pip3 install flask
RUN pip3 install pymongo
RUN pip3 install requests
RUN pip3 install paramiko
RUN pip3 install azure-mgmt-resource
RUN pip3 install azure-mgmt-compute
RUN pip3 install azure-mgmt-network
RUN pip3 install azure-identity
RUN pip3 install azure-mgmt-extendedlocation==1.0.0b2
RUN pip install azure-storage-file-share

#CMD python3 initializer.py
ENTRYPOINT ["python3"]
CMD ["initializer.py","8000"]