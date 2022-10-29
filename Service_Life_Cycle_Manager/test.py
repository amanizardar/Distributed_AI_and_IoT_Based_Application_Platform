import os
hostname = "20.233.38.212" 
response = os.system("ping -t 1 -c 1 " + hostname)
if response == 0:
    print(hostname, 'is up!')
else:
    print(hostname, 'is down!')