# Distributed_AI_and_IoT_Based_Application_Platform

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
with respective sensor/controller types using data uploaded in their config file.t the end of this process, the end user can
view all the deployed applications and the available sensor/controller instances based on the bound type and then choose
the sensor instances according to his/her preferences. The sensors/ controllers would be managed by the Sensor- Controller
service and the deployment would be managed by the deployment service and the node manager service.

## Use Cases/Requirements

#### Platform Initialize
- Initialize a number of Virtual machines / containers on the Host as configured by the configurator.
- Sets up the environment on VMs for module deployment.
- Deploys and starts all the services.

#### Request manager
- Providing GUI to users to interact with platform services, enabling:
- App developer Uploading Application
- Data Scientist Host AI models
- Platform Configurator Manage Sensors
- End User to consume different services provided by hosted applications.
- Managing users
- Making appropriate calls to end points

#### Deployment manager
- Provides UI to upload pickle, config, contract files.
- Generates docker file and wrapper file
- Deploys docker and wrapper file on a VM(Azure).
- Node manager
- Responsible for initiating node instances
- Responsible for init file generation

#### Node manager
- Responsible for initiating node instances
- Responsible for init file generation

#### Server Lifecycle manager
- Manages deployment servers and their status
- Responsible for fault tolerance of nodes
- Responsible for initiating nodes with necessary packages and modules


#### Load Balancer
- Responsible for finding out the best node to deploy the application.
- Looks for relevant stats and returns chosen node’s ip address for deployment.


#### Authentication & Authorization Manager
- Creating Database of each of the 4 user types
- Providing end points

#### Sensor Manager
- This module is responsible for handling the sensors, starting from registering it for the very first time to
fetching and preprocessing data and sending it to the application.
- Module also deals with the registration and configuration of the controllers.

#### Scheduler
- Responsible for handling requests
- Schedules pending jobs from the queue and sends them to the deployment module.


#### Monitoring Manager
- Responsible for continuously monitoring the status of all the other modules.
- Logs are taken care of by the logging service. It checks if the log file content


## Different roles of the users

- Data scientists can upload pickle, config and contract files

- App developers can upload source files, config and contract files

- Platform configurer registers sensor types into the platform and then he/she can register
sensor/controller instances corresponding to those types, alongwith information about those instances
like location

- End user will be able to view all the applications that are deployed on the platform and then he/she can
select an application which they want to use and also select the sensor/controller instances based on their
locations which they want to bind with that application

## Environment

- Operating System : Linux, Ubuntu 20.4 LTS
- Nature of Interaction: The platform services can be accessed by the users of the 4 different roles though
a web GUI in a secured way.Inside the platform the module microservices would interact with each other using a messaging
system with technologies like Apache Kafka or using REST API endpoints. The sensor instances would send data to the platform through Apache Kafka.
- Environment for deployment: The Nodes for deployment would be created using docker containers inside Azure VMs.
- Unified Database used by the Platform: We shall use Azure SQL database or MongoDb Database for creating the registries and data entry tables for the platform

## Technologies used
#### Python 
Most of the implementation would be done based on python as it provides the language constructs that
satisfies most of our requirements for the integration and implementation of the modules and also it
provides efficient ways to integrate with other technologies like Azure services, database technologies etc.
that we would be using in our project.

#### Flask
Flask provides compatible ways to integrate with python for creating API endpoints.
We would use Flask to create all our API and UI endpoints.
#### Apache Kafka
Kafka would be used as the messaging queue for interaction between the modules.
#### Docker
Docker provides ways to package and containerize applications using the commands. As it is
an efficient way to interact with the remote virtual machines using commands so docker is
our choice of technology for containerizing the applications and models and host them in
the remote VMs.
#### Bash
 We plan to use bash scripting for initiating the system commands in the platform modules.
 HTML, CSS, JS, Bootstrap
 For our unified UI, we will be using frontend technologies like HTML, CSS, JS and Bootstrap to
create the dashboards and other UI interfaces.
#### Azure Services
Azure VMs : We plan to use Azure VM resources for our hosted remote machine which would
act as the servers and nodes for the service deployment.
#### Database Technologies
 For implementing the unified database of our platform, we plan on using either Azure SQL or
MongoDB depending on our needs during implementation.

## Project Reports 
1. [Design Documents](https://github.com/amanizardar/Distributed_AI_and_IoT_Based_Application_Platform/tree/main/Documentations/Design_Documents).  
2. [Requirement_Documents](https://github.com/amanizardar/Distributed_AI_and_IoT_Based_Application_Platform/tree/main/Documentations/Requirement_Documents).



