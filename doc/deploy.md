# Docker compose deployment

## Docker files
- `docker-compose.yml` This file defines the services, networks, and volumes for your Docker application. It's essential for orchestrating the containers.
- `Dockerfile-java` This file is used to build the Docker image for Ruthelde. It will include instructions for setting up the Java environment and deploying the Java application.
- `Dockerfile-streamlit`  This file is for building the Docker image for a Streamlit application, likely including Python dependencies and Streamlit specific setup.

## Prerequisites
- Docker installed on your machine. You can download it from [here](https://www.docker.com/products/docker-desktop).
- Docker compose installed on your machine. You can download it from [here](https://docs.docker.com/compose/install/).
- Git installed on your machine. You can download it from [here](https://git-scm.com/downloads).

## Deployment steps
1. Clone the repository to your local machine.
2. Navigate to the root directory of the repository.
3. Run the following command to build the Docker images and start the containers in the background.
```bash
docker-compose up --build -d
```
4. Verify that the containers are running by running the following command.
```bash
docker-compose ps
```
You should see both `java` and `streamlit` containers running.
5. Open your browser and navigate to `http://server-ip:8501` to access the Streamlit application.

## Stopping the containers
To stop the containers, run the following command.
```bash
docker-compose down
```
This will stop and remove the containers, networks, and volumes created by `docker-compose up`.

## Troubleshooting
- If you encounter any issues, you can check the logs of the containers by running the following command.
```bash
docker-compose logs
```

## Cleaning up
- To remove the Docker images and volumes created by `docker-compose up`, run the following command.
```bash
docker-compose down --rmi all --volumes
```
- To remove files created by the application, you can manually delete them in directory `files/optimization/`, `files/optimization_ms/`, `files/setup/`, `files/spectra/` and `files/target/`.

## Service details
Here I will describe the services in more detail to help you understand how they work together.
### Java service
1. Base Image: It uses openjdk:11 as the base image, ensuring that Java 11 is available in the container for running your application.
2. File Copying: Copies Ruthelde_Server.jar from the Ruthelde_Shell_Tools/Ruthelde_Server directory of your project into the /app directory inside the container.
3. Port Exposure: Exposes port 9090, indicating that the Java application listens on this port.
4. Command: Starts the Java server by running java -jar Ruthelde_Server.jar 9090, indicating that the server will run on port 9090.

Ensure that Ruthelde_Server.jar is available in the Ruthelde_Shell_Tools/Ruthelde_Server directory of your project.
Ensure that port 9090 is not blocked by the server's firewall or in use by another application.

### Streamlit service
1. Base Image: It uses adoptopenjdk:11-jre-hotspot as the base image, which provides Java Runtime Environment (JRE) 11 along with a hot spot compiler. This allows both Java and Python to be run in the same container.
2. Python Installation: The Dockerfile updates the package list and installs Python 3 and pip (Python's package installer) to ensure Python scripts can be executed within the container.
3. Working Directory: Sets /app as the working directory inside the container, similar to the Java Dockerfile.
4. Dependencies: Copies the requirements.txt file from the root directory of your project into the /app directory inside the container and installs the Python dependencies using pip.
5. File Copying: Copies the Streamlit application `app.py` from the root directory of your project into the /app directory inside the container. Also copies `files` and `src` directories.
6. Port Exposure: Exposes port 8501, indicating that the Streamlit application listens on this port.
7. Command: Starts the Streamlit application by running streamlit run app.py, making the application available on port 8501.

Ensure that the requirements.txt file is available in the root directory of your project and contains the necessary Python dependencies.
Ensure that the `app.py` file, `files` and `src` directory are available in the root directory of your project.
Ensure that port 8501 is not blocked by the server's firewall or in use by another application.



