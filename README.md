# Distributed_AI_and_IoT_Based_Application_Platform
Built the distributed fault-tolerant platform that supports deploy-
ment and interaction of applications, AI/ML models and IoT sen-
sor/controllers.  
The platform provides unified UI to handle the request from data
scientist, platform developer, application developer & end user.  

The platform is capable of managing end-to-end service starting
from authorization, AI/ML module deployment, sensors and appli-
cation deployment & binding of the module and sensors with the
application and scheduling.  
The deployment service checks the load on a Node(VM) and de-
ploys the application as a new container on VM by accessing remote
docker servers.  
Each service is running as an independent docker container and
communicates via Kafka. The platform is capable of restarting any
service on any unexpected failure event.  


In this project, we plan to design and implement an unified application platform that supports deployment of and
interaction between applications, AI/ML models and IoT sensors/controllers. The platform will consist of multiple services
which can be accessed by the users of different roles through an unified UI that communicates with the request manager
service acting as a secured gateway over the other underlying services. The different roles include the Data Scientist,
Platform Configurer, End Application Developer and End User. Each of these users can interact with the platform after valid
authentication.
After the Data Scientist creates and trains a model using an IDE of his/her choice in his local environment they can
upload that model along with a contract file (that contains the pre-processing and post-processing function which needs to
be used on the data that is passed on/ retrieved from this model.) and a config file to the platform for deployment. The
deployment service would use the config file to deploy the model as a service on a separate node and this model can then
be used using an api endpoint. On the other hand, the Platform Configurer can register new sensor and controller types on
the platform and then for each type they can register instances for those sensors and controllers. After this the end
application developer can deploy his/her application using the deployment service of the platform and bind that service
with respective sensor/controller types using data uploaded in their config file. At the end of this process, the end user can
view all the deployed applications and the available sensor/controller instances based on the bound type and then choose
the sensor instances according to his/her preferences. The sensors/ controllers would be managed by the Sensor- Controller
service and the deployment would be managed by the deployment service and the node manager service.



