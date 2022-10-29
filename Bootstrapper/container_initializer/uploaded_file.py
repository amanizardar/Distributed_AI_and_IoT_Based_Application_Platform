# from azure.common.credentials import ServicePrincipalCredentials 

# from azure.mgmt.resource import ResourceManagementClient 

# from azure.mgmt.compute import ComputeManagementClient

# from azure.mgmt.network import NetworkManagementClient

# from azure.mgmt.compute.models import DiskCreateOption

# #  from azure.common.credentials import ServicePrincipalCredentials
# # from azure.mgmt.resource import ResourceManagementClient
# # from azure.mgmt.compute import ComputeManagementClient
# # from azure.mgmt.network import NetworkManagementClient
# # from azure.mgmt.compute.models import DiskCreateOption

# SUBSCRIPTION_ID = '7c95ac93-35ff-4a0d-8d75-aabcd44f61ee'
# GROUP_NAME = 'Test'
# LOCATION = 'South India'
# VM_NAME = 'VM1'

SUBSCRIPTION_ID = 'e469496e-1288-4e2c-97c5-77fad883bc8a'
GROUP_NAME = 'IAS_PROJECT'
# LOCATION = 'South India'
VM_NAME = 'TESTVM1'


# def get_credentials():

#     credentials = ServicePrincipalCredentials(
#         client_id = 'a2f3c351-f547-4438-8606-b1ab7de9093f',
#         secret = '-.a7Q~WLiTPuUnOM3QAVm5c3zQB_dmJfPTwoV',
#         tenant = '031a3bbc-cf7c-4e2b-96ec-867555540a1c'
#     )

#     return credentials

# credentials = get_credentials()

# resource_group_client = ResourceManagementClient(
#     credentials,
#     SUBSCRIPTION_ID
# )
# network_client = NetworkManagementClient(
#     credentials,
#     SUBSCRIPTION_ID
# )
# compute_client = ComputeManagementClient(
#     credentials,
#     SUBSCRIPTION_ID
# )

# def get_vm(compute_client):
#     vm = compute_client.virtual_machines.get(GROUP_NAME, VM_NAME, expand='instanceView')
#     # print("hardwareProfile")
#     # print("   vmSize: ", vm.hardware_profile.vm_size)
#     # print("\nstorageProfile")
#     # print("  imageReference")
#     # print("    publisher: ", vm.storage_profile.image_reference.publisher)
#     # print("    offer: ", vm.storage_profile.image_reference.offer)
#     # print("    sku: ", vm.storage_profile.image_reference.sku)
#     # print("    version: ", vm.storage_profile.image_reference.version)
#     # print("  osDisk")
#     # print("    osType: ", vm.storage_profile.os_disk.os_type.value)
#     # print("    name: ", vm.storage_profile.os_disk.name)
#     # print("    createOption: ", vm.storage_profile.os_disk.create_option.value)
#     # print("    caching: ", vm.storage_profile.os_disk.caching.value)
#     # print("\nosProfile")
#     # print("  computerName: ", vm.os_profile.computer_name)
#     # print("  adminUsername: ", vm.os_profile.admin_username)
#     # print("  provisionVMAgent: {0}".format(vm.os_profile.windows_configuration.provision_vm_agent))
#     # print("  enableAutomaticUpdates: {0}".format(vm.os_profile.windows_configuration.enable_automatic_updates))
#     # print("\nnetworkProfile")
#     # for nic in vm.network_profile.network_interfaces:
#     #     print("  networkInterface id: ", nic.id)
#     # print("\nvmAgent")
#     # print("  vmAgentVersion", vm.instance_view.vm_agent.vm_agent_version)
#     # print("    statuses")
#     # for stat in vm.instance_view.vm_agent.statuses:
#     #     print("    code: ", stat.code)
#     #     print("    displayStatus: ", stat.display_status)
#     #     print("    message: ", stat.message)
#     #     print("    time: ", stat.time)
#     # print("\ndisks");
#     # for disk in vm.instance_view.disks:
#     #     print("  name: ", disk.name)
#     #     print("  statuses")
#     #     for stat in disk.statuses:
#     #         print("    code: ", stat.code)
#     #         print("    displayStatus: ", stat.display_status)
#     #         print("    time: ", stat.time)
#     # print("\nVM general status")
#     # print("  provisioningStatus: ", vm.provisioning_state)
#     # print("  id: ", vm.id)
#     # print("  name: ", vm.name)
#     # print("  type: ", vm.type)
#     # print("  location: ", vm.location)
#     # print("\nVM instance status")
#     for stat in vm.instance_view.statuses:
#         print("  code: ", stat.code)
#         print("  displayStatus: ", stat.display_status)



# get_vm(compute_client)
# print("------------------------------------------------------")
# input('Press enter to continue...')









from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient

# credential = ClientSecretCredential(
#     tenant_id='031a3bbc-cf7c-4e2b-96ec-867555540a1c',
#     client_id='a2f3c351-f547-4438-8606-b1ab7de9093f',
#     client_secret='-.a7Q~WLiTPuUnOM3QAVm5c3zQB_dmJfPTwoV'
# )

credential = ClientSecretCredential(
    tenant_id='031a3bbc-cf7c-4e2b-96ec-867555540a1c',
    client_id='c8143046-faf2-48b7-b373-eb12f5040cd5',
    client_secret='vqP7Q~XOGUQIV9~c2KVwSORVMXNRq11_o~I8A'
)


compute_client = ComputeManagementClient(
    credential=credential,
    subscription_id=SUBSCRIPTION_ID
)

vm = compute_client.virtual_machines.get(GROUP_NAME, VM_NAME, expand='instanceView')
# for stat in vm.instance_view.statuses:
#         print("  code: ", stat.code)
#         print("  displayStatus: ", stat.display_status)

stat = vm.instance_view.statuses
print(stat[1].display_status)