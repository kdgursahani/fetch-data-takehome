import json
import os
from subprocess import run, PIPE
import psycopg2
from mask_sqs_data import *
from write_masked_data import *
from dotenv import load_dotenv


def read_from_sqs_queue(queue_url):
    """
    Reads messages from an AWS Queue, from the specified queue_url.
    Calls the mask_pii() function to mask device_id and ip fields.
    Calls the delete_message() function to delete a message after successful processing.
    Parameters: Queue url of an AWS Queue.
    Returns: A list of messages from the AWS Queue, filtering out the corrupted messages.
    """
    messages = []

    while True:
        # Use awslocal command for local testing
        command = [
            'awslocal',
            'sqs',
            'receive-message',
            '--queue-url',
            queue_url
        ]
        result = run(command, stdout=PIPE, stderr=PIPE, text=True, shell=True)
        
        if result.stdout:

            response = json.loads(result.stdout)
            message = response['Messages'][0]
            body = json.loads(message['Body'])
            receipt_handle = message['ReceiptHandle']

            try:
                # Mask PII fields
                masked_data = mask_pii(body)
                print(masked_data)
                messages.append((masked_data, receipt_handle))
                delete_message(queue_url, receipt_handle)

            except Exception as e:
                print(f"Error processing message: {e}." + " The body of the message is shown below.")
                delete_message(queue_url, receipt_handle)
                print(body)
        else:

            break 

    return messages


def delete_message(queue_url, receipt_handle):
    """
    Deletes a message after succesfully processing it
    """

    command = [
        'awslocal',
        'sqs',
        'delete-message',
        '--queue-url',
        queue_url,
        '--receipt-handle',
        receipt_handle
    ]

    result = run(command, stdout=PIPE, stderr=PIPE, text=True, shell=True)

    if result.returncode != 0:
        print(f"Failed to delete message. Error: {result.stderr}")


# Usage for local testing
if __name__ == "__main__":

    # Example usage
    queue_url = 'http://localhost:4566/000000000000/login-queue'  
    # Adjust the queue name based on your LocalStack configuration

    # Read from SQS queue
    messages = read_from_sqs_queue(queue_url)

    # Start connection to Postgres database
    load_dotenv("postgres_user.env")
    print("Starting connection to postgres")

    if len(messages) != 0:
        # Establish connection to local PostgreSQL
        conn = psycopg2.connect(
        host='localhost',
        port='5432',
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        database=os.getenv('POSTGRES_DATABASE')
        )

        # Create the table if not exists
        create_user_logins_table(conn)

        for data, receipt_handle in messages:
            # Write to PostgreSQL
            write_to_postgres(data, conn)
            print("Record successfully written to PostgreSQL.")

        # Close the database connection when done
        print("Write finished to user_logins")
        conn.close()