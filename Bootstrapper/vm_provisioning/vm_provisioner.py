# Import the needed credential and management objects from the libraries.
from azure.identity import AzureCliCredential
from pymongo import MongoClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
import os
import json
import time
import threading

def dict_reduce(parent_dict, child_dict):
    for key in child_dict:
        del parent_dict[key]
    return parent_dict


def provision_vm():
    cmd = 'az login --service-principal -u "70d4dd84-669a-442b-bd60-0aac99f75f47" -p "T4C9OhLGk4M.DGX7YUkvegE-B2LP2SyT0l" --tenant "031a3bbc-cf7c-4e2b-96ec-867555540a1c"'
    os.system(cmd)
    
    print(os.getcwd() + "\n")
    print(f"Provisioning a virtual machine...some operations might take a minute or two.")

    # Acquire a credential object using CLI-based authentication.
    credential = AzureCliCredential()
    group_flag = False
    network_flag = False
    vm_flag = False
    # Retrieve subscription ID from environment variable.
    f = open('./Bootstrapper/subscription_config.json')
    subs = json.load(f)
    subscription_id = subs["id"]

    CONNECTION_STRING = "mongodb://root:root@cluster0-shard-00-00.llzhh.mongodb.net:27017,cluster0-shard-00-01.llzhh.mongodb.net:27017,cluster0-shard-00-02.llzhh.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-u1s4tk-shard-0&authSource=admin&retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    ip_dbname = client['AI_PLATFORM']
    IP_ADDRESSES = ip_dbname["MODULE_URL"]

    # Step 1: Provision a resource group

    # Obtain the management object for resources, using the credentials from the CLI login.
    resource_client = ResourceManagementClient(credential, subscription_id)

    # Constants we need in multiple places: the resource group name and the region
    # in which we provision resources. You can change these values however you want.
    file = open('./Bootstrapper/network_resource_config.json')
    v_net = json.load(file)

    RESOURCE_GROUP_NAME = v_net["RESOURCE_GROUP_NAME"]           #"IAS_AZURE_GROUP_TEST"
    LOCATION =  v_net["LOCATION"]                                #"centralindia"
    AZURE_GROUP_DETAILS = ip_dbname["AZURE_GROUP_DETAILS"]

    for item in resource_client.resource_groups.list():
        if item.name == RESOURCE_GROUP_NAME:
            group_flag = True

    # Provision the resource group.
    if group_flag == False:
        rg_result = resource_client.resource_groups.create_or_update(RESOURCE_GROUP_NAME,
            {
                "location": LOCATION
            }
        )
        print(f"Provisioned resource group {rg_result.name} in the {rg_result.location} region")
    else:
        print(f"Resource group {LOCATION} already present in the {LOCATION} region")
    # For details on the previous code, see Example: Provision a resource group
    # at https://docs.microsoft.com/azure/developer/python/azure-sdk-example-resource-group


    # Step 2: provision a virtual network

    # A virtual machine requires a network interface client (NIC). A NIC requires
    # a virtual network and subnet along with an IP address. Therefore we must provision
    # these downstream components first, then provision the NIC, after which we
    # can provision the VM.

    # # Network and IP address names
    VNET_NAME = v_net["VNET_NAME"]                      #"IAS_AZURE_VNET_TEST"
    SUBNET_NAME = v_net["SUBNET_NAME"]                  #"IAS_AZURE_SUBNET_TEST"
    IP_NAME = v_net["IP_NAME"]                          #"IAS_AZURE_IP_TEST"
    IP_CONFIG_NAME = v_net["IP_CONFIG_NAME"]            #"IAS_AZURE_IPCONFIG_TEST"
    NIC_NAME =  v_net["NIC_NAME"]                       #"IAS_AZURE_NIC_TEST"
    nic_id = ''
    # Obtain the management object for networks
    network_client = NetworkManagementClient(credential, subscription_id)

    for item in network_client.virtual_networks.list(RESOURCE_GROUP_NAME):
        if item.name == VNET_NAME:
            network_flag = True

    # Provision the virtual network and wait for completion
    if network_flag == False:
        poller = network_client.virtual_networks.begin_create_or_update(RESOURCE_GROUP_NAME,
            VNET_NAME,
            {
                "location": LOCATION,
                "address_space": {
                    "address_prefixes": ["10.0.0.0/16"]
                }
            }
        )
        vnet_result = poller.result()
        print(f"Provisioned virtual network {vnet_result.name} with address prefixes {vnet_result.address_space.address_prefixes}")

        # Step 3: Provision the subnet and wait for completion
        poller = network_client.subnets.begin_create_or_update(RESOURCE_GROUP_NAME, 
            VNET_NAME, SUBNET_NAME,
            { "address_prefix": "10.0.0.0/24" }
        )
        subnet_result = poller.result()
        
        AZURE_GROUP_DETAILS = ip_dbname["AZURE_GROUP_DETAILS"]
        # a = AZURE_GROUP_DETAILS.find_one({'RESOURCE_GROUP_NAME':RESOURCE_GROUP_NAME}) 
        # if a != None:
        AZURE_GROUP_DETAILS.insert_one({
            'RESOURCE_GROUP_NAME' : RESOURCE_GROUP_NAME,
            'VNET_NAME' : VNET_NAME,
            "LOCATION" : LOCATION,
            'SUBNET_NAME' : SUBNET_NAME,
            'SUBNET_ID' : subnet_result.id
        })
        print(f"Provisioned virtual subnet {subnet_result.name} with address prefix {subnet_result.address_prefix}")

        # Step 4: Provision an IP address and wait for completion
        

        
    # else:
    #     NIC_DETAILS = ip_dbname["NIC_DETAILS"]
    #     obj = NIC_DETAILS.find_one({"resource_group_name" : RESOURCE_GROUP_NAME,
    #         "vnet_name" : VNET_NAME,
    #         "subnet_name" : SUBNET_NAME})
    #     nic_id = obj['nic_id']
    #     print("Subnet Already present")


    # Step 6: Provision the virtual machine
    f1 = open('./Bootstrapper/vm_provisioning/vm_provisioning_config.json')
    f2 = open('./Bootstrapper/vm_user_config.json')
    vm_s = json.load(f1)
    vm_s2 = {}
    vm_user = json.load(f2)

    provisioned_vm = []
    # Obtain the management object for virtual machines
    compute_client = ComputeManagementClient(credential, subscription_id)
    for item in compute_client.virtual_machines.list(RESOURCE_GROUP_NAME):
        for key in vm_s:
            if item.name == vm_s[key]["VM_NAME"]:
                print(item.name +" Already Present!")
                vm_s2[key] = vm_s[key] 
                # del vm_s[key]
                
    intersection = vm_s2.keys() & vm_s.keys()
    
    reduced_dict = dict_reduce(vm_s, intersection)
    vm_s = reduced_dict
    # f3 = open('../configuration_details.json')
    # config_details = json.load(f3)

    for key in vm_s:
    # Step 5: Provision the network interface client
        poller = network_client.public_ip_addresses.begin_create_or_update(RESOURCE_GROUP_NAME,
            vm_s[key]['ip_name'],
            {
                "location": LOCATION,
                "sku": { "name": "Standard" },
                "public_ip_allocation_method": "Static",
                "public_ip_address_version" : "IPV4"
            }
        )

        ip_address_result = poller.result()

        subnet_result = AZURE_GROUP_DETAILS.find_one({'SUBNET_NAME' : SUBNET_NAME})
        subnet_id = subnet_result['SUBNET_ID']

        print(f"Provisioned public IP address {ip_address_result.name} with address {ip_address_result.ip_address}")    
        poller = network_client.network_interfaces.begin_create_or_update(RESOURCE_GROUP_NAME,
            vm_s[key]['nic_name'], 
            {
                "location": LOCATION,
                "ip_configurations": [ {
                    "name":  vm_s[key]['ip_config_name'],
                    "subnet": { "id": subnet_id },
                    "public_ip_address": {"id": ip_address_result.id }
                }]
            }
        )

        nic_result = poller.result()

        ip_address_details = {
            "resource_group_name" : RESOURCE_GROUP_NAME,
            "vnet_name" : VNET_NAME,
            "subnet_name" : SUBNET_NAME, 
            "ip_name" : ip_address_result.name,
            "ip_config_name" : vm_s[key]['ip_config_name'],
            "ip_address" : ip_address_result.ip_address,
            "location": LOCATION,
            "address_space": {
                    "address_prefixes": ["10.0.0.0/16"]
            },
            "ip_configurations": [ {
                    "name": vm_s[key]['ip_config_name'],
                    "subnet": { "id": subnet_id },
                    "public_ip_address": {"id": ip_address_result.id }
                }],
            "nic_name" : nic_result.name,
            "nic_id" : nic_result.id
        }
        nic_id = ip_address_details['nic_id']
        # NIC_DETAILS = ip_dbname["NIC_DETAILS"]
        # NIC_DETAILS.insert_one(ip_address_details)
        # json_object = json.dumps(ip_address_details, indent = 4)
        # with open("../configuration_details.json", "w") as outfile:
        #     outfile.write(json_object)
        print(f"Provisioned network interface client {nic_result.name}")
        print(f"Provisioning virtual machine "+ str(vm_s[key]["VM_NAME"]) +"; this operation might take a few minutes.")

        # Provision the VM specifying only minimal arguments, which defaults to an Ubuntu 18.04 VM
        # on a Standard DS1 v2 plan with a public IP address and a default virtual network/subnet.

        poller = compute_client.virtual_machines.begin_create_or_update(RESOURCE_GROUP_NAME, vm_s[key]["VM_NAME"],
            {
                "location": LOCATION,
                "storage_profile": {
                    "image_reference": {
                        "publisher": 'Canonical',
                        "offer": vm_s[key]["offer"],        #"UbuntuServer",
                        "sku": vm_s[key]["sku"],            #"16.04.0-LTS",
                        "version": "latest"
                    }
                },
                "hardware_profile": {
                    "vm_size": "Standard_DS1_v2"
                },
                "os_profile": {
                    "computer_name": vm_s[key]["VM_NAME"],
                    "admin_username": vm_user["username"],
                    "admin_password": vm_user["password"]
                },
                "network_profile": {
                    "network_interfaces": [{
                        "id": nic_id,
                    }]
                }        
            }
        )

        vm_result = poller.result()
        provisioned_vm.append(vm_result)
        VM_DETAILS = ip_dbname["VM_DETAILS"]
        VM_DETAILS.insert_one({
            "name": vm_s[key]["VM_NAME"],
            "group": RESOURCE_GROUP_NAME,
            "ip" : ip_address_result.ip_address,
            "username" : vm_user["username"],
            "password" : vm_user["password"],
            "status":"active",
            "first_free_port":9000
        })
        
        print(f"Provisioned virtual machines : {provisioned_vm}")
        cmd = "az vm open-port --resource-group "+RESOURCE_GROUP_NAME+" --name "+vm_s[key]["VM_NAME"]+" --port '*' --priority 600"
        os.system(cmd)
        cmd = "az vm stop -g "+RESOURCE_GROUP_NAME+" -n "+vm_s[key]["VM_NAME"]
        os.system(cmd)
        cmd = "az vm start -g "+RESOURCE_GROUP_NAME+" -n "+vm_s[key]["VM_NAME"]
        os.system(cmd)
