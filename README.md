## Fetch Data Engineering Take-Home Assessment ##
This application is designed to process user login behavior data from an AWS SQS queue, mask sensitive information, and store the results in a Postgres database. The application uses Docker containers for local development and testing and is currently designed for local testing and deployment. This document consists of the prerequisites for this application to run successfully locally, the steps to run this application, and answers questions pertaining to selecting the right deployment tools, addressing potential challenges, and ensuring that the deployment aligns with organizational policies and best practices.

This project is the solution for the Data Engineering assignment.

## Pre-requisites ##
Installation of :
- Docker
- docker-compose
- awscli-local 
- psql

## Steps to run the application ##

1. Clone the repository
```bash
git clone https://github.com/kdgursahani/fetch-data-takehome.git
```
2. Navigate to the repository folder, and run the command:
```bash
docker-compose up
```
3. Navigate to the src folder within the repository, and run the code to test local access:
```bash
python ./sqs_read_mask.py "http://localhost:4566/000000000000/login-queue"

```
4. Connect to the Postgres database, and verify the table is created
```bash
psql -d postgres -U postgres -p 5432 -h localhost -W
postgres=# select * from user_logins;
```
5. Navigate to the repository folder, and run the following command to stop the container, once data has been written to Postgres successfully:
```bash
docker-compose down
```
## Q and A ##
1. How would you deploy this application in production?
 - Ensure that the decoding of the base64 encoding retrieves the correct values for the IP and device_id fields,
   to ensure that data is not corrupted or lost.
 - Within our development stage, we can investigate whether there are any tables negatively affected by this creation of the user_logins table. 
 - We should discuss with internal stakeholders to whom this data is valuable, to understand its frequency of usage to appropriately schedule its run.
 - We can request code reviews from other engineers with similar experience.
 - Since the application is containerized, Kubernetes cluster can be used to simplify deployment and
   ensure consistent behavior across different environments.
   
2. What other components would you want to add to make this production-ready?
 - If the process of connecting to the Postgres database is a frequent one, we can create a postgres_operations.py file
   consists of the appropriate function to connect to Postgres.
 - This callable method can be used for other similar applications as well, within the company's shared repository.
   This would reduce redundancy in code.
 - As mentioned earlier, Kubernetes cluster would simplify deployment on a large scale.
 - Upon understanding its frequency of usage, we can utilize the CronJob resource to schedule
   the execution of this application regularly.

3. How can this application scale with a growing dataset?
 - Utilizing Kubernetes provides some generally applicable features such as deployment, scaling, and load balancing.
 - This would ensure that the workload is scaled with the increased demand, i.e., growing dataset.

5. How can PII be recovered later on?
- Since base64 encoding is reversible, creating a script that reads from the user_logins table in the Postgres
database and unmasking the masked_ip and masked_device_id fields to their original value would be possible. 
- Eventually, this script can be made available to analysts with the appropriate permissions, to execute on demand via Apache Airflow and
achieve the desired results.

5. What are the assumptions you made?
- Local Development Environment: The provided instructions assume a local development environment using Docker and 
local instances of AWS SQS and Postgres.
- AWS CLI and Localstack: Assumed the availability of the AWS CLI and Localstack for local testing.
- Simplified PII Masking: The PII masking logic is simplified for demonstration purposes. We should probably consider more
sophisticated PII masking techniques in a real-world scenario.


