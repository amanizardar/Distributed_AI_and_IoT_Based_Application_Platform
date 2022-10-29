from numpy import source
import paramiko
import json
import os
import sys

from azure.storage.fileshare import ShareFileClient
from azure.storage.fileshare import ShareDirectoryClient
from azure.storage.fileshare import ShareClient

# connection_string = "DefaultEndpointsProtocol=https;AccountName=storageias;AccountKey=tnxGtqqFpuRfoJMxRR7H5evonZ0P+2dZVoV+VSTHKqOSyxkMIihIUMsXQ7KM+eLguN2/b8ncl3S9+AStZRvImg==;EndpointSuffix=core.windows.net"
connection_string = "DefaultEndpointsProtocol=https;AccountName=storageias;AccountKey=tnxGtqqFpuRfoJMxRR7H5evonZ0P+2dZVoV+VSTHKqOSyxkMIihIUMsXQ7KM+eLguN2/b8ncl3S9+AStZRvImg==;EndpointSuffix=core.windows.net"
file_client = ShareClient.from_connection_string(conn_str=connection_string,share_name="testing-file-share",file_path="uploaded_file.py")
share_name="testing-file-share"

def create_directory(dir_name):
    try:
        dir_client = ShareDirectoryClient.from_connection_string(connection_string, share_name, dir_name)
        print("Creating directory:", share_name + "/" + dir_name)
        dir_client.create_directory()

    except Exception as ex:
        print("ResourceExistsError:", ex)

def download_azure_file(source_path,dir_name, file_name):
    try:
        source_file_path = source_path[2:] + "/"+ dir_name +"/"+file_name
        dest_file_name = dir_name +"/"+file_name
        file_client = ShareFileClient.from_connection_string(connection_string, share_name, source_file_path)
        with open(dest_file_name, "wb") as data:
            stream = file_client.download_file()
            data.write(stream.readall())
    except Exception as ex:
        print("ResourceNotFoundError:", ex)

def download_files(source_path,folder_name):
    file_is_directory = False
	
    os.mkdir(folder_name)

    my_directory_client = file_client.get_directory_client(directory_path=source_path + '/'+folder_name)
	
    my_list = list(my_directory_client.list_directories_and_files())
	
    for file in my_directory_client.list_directories_and_files():
        if file['name'][0]!='.':
            if file['is_directory']:
                download_files(source_path,folder_name+'/'+file["name"])
            else:
                download_azure_file(source_path,folder_name, file["name"])
                

#download_files("./AI_and_IoT_Application_Platform","Request_Manager")
source_path = sys.argv[1]
folder_name = sys.argv[2]
download_files(source_path,folder_name)

#download_files("./Aman_folder","Aman_folder")


print("Done")