"""
    This program sends three different messages to three different queues on the RabbitMQ server. 
    Each message contains a temperature reading from the smart-smoker represented by the smoker-temps.csv. 

    Author: Wade Bryson
    Date: September 24, 2023

"""

import pika
import sys
import webbrowser
import csv
import time


# Configure logging
from util_logger import setup_logger
logger, logname = setup_logger(__file__)

Show_Offer = True

def offer_rabbitmq_admin_site():
    """Offer to open the RabbitMQ Admin website"""
    ans = input("Would you like to monitor RabbitMQ queues? y or n ")
    print()
    if ans.lower() == "y":
        webbrowser.open_new("http://localhost:15672/#/queues")
        print()

def send_message(host: str, queue1_name: str, queue2_name: str, queue3_name: str, input_file: str):
    """
    Creates and sends a message to the queue each execution.
    This process runs and finishes.

    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue1_name (str): the name of the first queue
        queue2_name (str): the name of the second queue
        queue3_name (str): the name of the third queue
        input_file (str): the CSV file to be read
    """

    try:
        # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # use the connection to create a communication channel
        ch = conn.channel()
        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        ch.queue_declare(queue=queue1_name, durable=True)
        ch.queue_declare(queue=queue2_name, durable=True)
        ch.queue_declare(queue=queue3_name, durable=True)

        # read CSV
        with open(input_file, 'r') as file:
            reader = csv.reader(file)
            # skip header row
            header = next(reader)
            for row in reader:
                # separate row into variables
                timestamp, temp_of_smoker, temp_food1, temp_food2 = row
                # Making sure all temperature readings are valid
                if temp_of_smoker == '':
                    temp_of_smoker = 'No Temperature'
                if temp_food1 == '':
                    temp_food1 = 'No Temperature'
                if temp_food2 == '':
                    temp_food2 = 'No Temperature'
                # define messages
                message1 = timestamp, temp_of_smoker
                message2 = timestamp, temp_food1
                message3 = timestamp, temp_food2
                # joining the messages
                message1_join = ",".join(message1).encode()
                message2_join = ",".join(message2).encode()
                message3_join = ",".join(message3).encode()
                # use the channel to publish first message to first queue
                # every message passes through an exchange
                ch.basic_publish(exchange="", routing_key=queue1_name, body=message1_join)
                logger.info(f" [x] Sent {message1} to {queue1_name}")
                # publish second message to second queue
                ch.basic_publish(exchange="", routing_key=queue2_name, body=message2_join)
                logger.info(f"[x] Sent {message2} to {queue2_name}")
                # publish third message to third queue
                ch.basic_publish(exchange="", routing_key=queue3_name, body=message3_join)
                logger.info(f"[x] Sent {message3} to {queue3_name}")
                # wait 30 seconds before sending the next message to the queue
                time.sleep(2)

    except pika.exceptions.AMQPConnectionError as e:
        logger.info(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # close the connection to the server
        conn.close()

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":  
    # ask the user if they'd like to open the RabbitMQ Admin site
    if Show_Offer == True:
        offer_rabbitmq_admin_site()
   
    # send the message to the queue
    send_message("localhost","Smoker_Temp_Queue","Temp_Food1_Queue", "Temp_Food2_Queue", "smoker-temps.csv")

