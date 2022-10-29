import paramiko
import json
import os
from flask import Flask , request
from pymongo import MongoClient
from azure.mgmt.compute import ComputeManagementClient
from azure.storage.fileshare import ShareFileClient
from azure.storage.fileshare import ShareDirectoryClient
from azure.storage.fileshare import ShareClient

connection_string = "DefaultEndpointsProtocol=https;AccountName=storageias;AccountKey=tnxGtqqFpuRfoJMxRR7H5evonZ0P+2dZVoV+VSTHKqOSyxkMIihIUMsXQ7KM+eLguN2/b8ncl3S9+AStZRvImg==;EndpointSuffix=core.windows.net"
file_client = ShareClient.from_connection_string(conn_str=connection_string,share_name="testing-file-share",file_path="uploaded_file.py")
share_name="testing-file-share"

def create_directory(dir_name):
    try:
        dir_client = ShareDirectoryClient.from_connection_string(connection_string, share_name, dir_name)
        print("Creating directory:", share_name + "/" + dir_name)
        dir_client.create_directory()

    except Exception as ex:
        print("ResourceExistsError:", ex.message)

def Upload_file_and_create_dir(folder_name,filepath):
    try:
        create_directory(folder_name)
        destination_file_path=folder_name+'/'+os.path.basename(filepath)
        print(destination_file_path)
        file_client = ShareFileClient.from_connection_string(connection_string, share_name, destination_file_path)

        with open(filepath, "rb") as source_file:
            file_client.upload_file(source_file)

        print("Succesfully Uploaded")
    except Exception as E:
        print("File_NOT_found Error")