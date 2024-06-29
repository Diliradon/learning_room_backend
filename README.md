# Learning Room Backend

## Instructions for Project Setup Using Docker

This project utilizes Docker Compose to manage isolated environments containing Django application and PostgreSQL database. This guide will help you quickly set up and run the project on your machine.

### Prerequisites

Before you begin, make sure the following are installed on your machine:

- Docker: [Installation Instructions](https://www.docker.com/products/docker-desktop/)
- Docker Compose: [Installation Instructions](https://docs.docker.com/compose/install/)

## Instructions

### Clone the Repository

Open your terminal or command prompt and clone this repository:

```bash
git clone https://github.com/Diliradon/learning_room_backend
Configure Environment
Copy the sample environment configuration file .env.example to .env:

bash
Copy code
cp .env.example .env
Edit the .env file and set the necessary environment variable values.

Start Docker Compose
Use Docker Compose to bring up the entire environment:

bash
Copy code
docker-compose up --build
The --build option instructs Docker Compose to rebuild all images if they do not exist or have changed.

Check Operation
After a successful launch, open your web browser and go to:

arduino
Copy code
http://localhost:8000/
If everything is working correctly, you should see the landing page of your Django application.

Stopping and Cleaning Up
To stop the containers, run:

bash
Copy code
docker-compose down
This command will stop and remove all containers associated with the project.

Creating a Superuser
Open another terminal (when the project is running in Docker).

Check the name of the image in which the project is running with the command:

bash
Copy code
docker-compose ps
Enter the project's local terminal using the command:

bash
Copy code
docker exec -it <container_name_from_previous_command> bash
Once inside the terminal, run the command:

bash
Copy code
python manage.py createsuperuser
Follow the prompts to create a superuser. Recommended credentials:

Email: user@admin.com
Password: user1234