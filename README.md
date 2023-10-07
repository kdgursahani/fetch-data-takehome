## Fetch Data Engineering Take-Home Assessment ##
This application is designed to process user login behavior data from an AWS SQS queue, mask sensitive information, and store the results in a Postgres database. The application uses Docker containers for local development and testing.

This project is the solution for the Data Engineering assignment given in the below link:
https://fetch-hiring.s3.amazonaws.com/data-engineer/pii-masking.pdf

# Pre-requisites
Installation of Docker, docker-compose, awscli-local, and psql.

# Steps to run the application

1. Clone the repository
```bash
git clone https://github.com/kdgursahani/fetch-data-takehome.git
```
2. Navigate to the repository folder, and run the command:
'''bash
docker-compose up
'''
3. Navigate to the src folder within the repository, and run the code to test local access:
'''bash
python ./sqs_read_mask.py "http://localhost:4566/000000000000/login-queue"

