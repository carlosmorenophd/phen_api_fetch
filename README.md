# Fetching micro backend for phenotypical data


This repository provides a system for fetching phenotypic data. The system was built using Docker for easy installation. Below are the general steps for installation.

**Note:** This project requires a prerequisite service [phen_api_store](https://github.com/carlosmorenophd/phen_api_store) to be running on your server for successful installation.

## Requirements:

### Hardware Requirements: 

The recommended computer for deploying this application should have at least a quad-core processor, 4GB of RAM, and 250GB of hard disk space for initial testing.

These requirements are specifically for the Phen_API_STORE. Additional systems will be installed on the same machine. For experimental and production use, consider upgrading to a system with an eight-core 16-thread processor, 24GB of RAM, and 2.5TB of storage, similar to our current setup.

### Operating System: 

Ubuntu `22.04` is the recommended operating system due to its up-to-date kernel and configurations that are optimized for application deployment. While Windows, macOS, or other systems can be used, they will require installing Docker in a Linux container with x86-64 architecture.

### Software Requirements: 

Docker is the only software required for this project. Please install it from the [official repository](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04) to ensure compatibility and proper execution of the following commands.


## Run application

The project utilizes multiple microservices. A Docker network will be created to facilitate inter-service communication.

```shell
docker network create phen-net
```
**Note:** If a network already exists, skip this instruction.


1. Rename the file `example.env` to `.env` put the variables form user, password, host and ip for database and the port to expose the api service:


```
DATABASE=database_mariadb
DATABASE_HOST=host_mariadb
DATABASE_PORT=port_mariadb
DATABASE_USERNAME=user_mariadb
DATABASE_PASSWORD=password_user_mariadb
PORT_API=8002
```
**Notes:**
* Ensure all database connection parameters are correctly configured and that network connectivity between the API server and the database server is established.

2. Command to run the container

```shell
docker compose -f compose.yaml up -d
```

## Check application running

To confirm the application is running, access the following URL in a web browser:

`http://{the_ip_server}:{port_on_variable_PORT_API}`

For example:

On a local machine with the port set to 8002, the URL would be:

`http://localhost:8002/api/v1/docs`

![Running API](README/img/Phen_api_fetch.png)


## About author


In collaboration with the [Universidad Autonoma del Estado de Mexico](https://www.uaemex.mx/), supported by [CONAHCYT](https://conahcyt.mx/) scholarships and supported by [CIMMYT](https://www.cimmyt.org/es/), this project was created. For new features, changes, or improvements, please reach out to:

Student, Ph.D. Juan Carlos Moreno Sanchez

* **[Scholar email](mailto:jcmorenos001@alumno.uaemex.mx)**
* **[Personal email](mailto:carlos.moreno.phd@gmail.com)**


