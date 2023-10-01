"""
    This program listens for work messages contiously. 
    Start multiple versions to add more workers.  

    Author: Wade Bryson
    Date: October 1st, 2023

"""

import pika
import sys
from collections import deque

# Configure logging
from util_logger import setup_logger
logger, logname = setup_logger(__file__)

# BBQ_Temp_Listener Deque Length
# Max Length = 5  (2.5 min * 1 reading every 30 seconds)
BBQ_Temp_Deque = deque(maxlen=5)

# define a callback function to be called when a message is received
def bbq_temp_callback(ch, method, properties, body):
    """ Define behavior on getting a message.
    Receive the temperature from RabbitMQ. Alerts the user if the temp decreases by more than 
    15 degrees in a 2.5 minute window."""
    # decode the binary message body to a string
    logger.info(f" [x] Received {body.decode()}")

    try:
        # Splitting the time stamp and temperature
        smoker_info = body.decode().split(",")
        # Making sure the temperature is valid before we add to the deque
        if smoker_info[1] != "No Temperature":
            smoker_temperature = float(smoker_info[1])
            smoker_timestamp = smoker_info[0]
            BBQ_Temp_Deque.append(smoker_temperature)

            # Temperature Alert Calculations
            if len(BBQ_Temp_Deque) > 1:
                temperature_difference = [BBQ_Temp_Deque[i]-BBQ_Temp_Deque[-1]
                                          for i in range(0, (len(BBQ_Temp_Deque)-1),1)]
                if any(value > 15 for value in temperature_difference):
                    alert_needed = True

                    if alert_needed:
                        logger.info("SMOKER ALERT: At {smoker_timestamp} your temperature dropped more than 15 degrees.")
    except Exception as e:
        logger.error("ERROR: There was an error processing the temperature.")
   
    # when done with task, tell the user
    logger.info(" [x] Receieved Smoker Temp.")
    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)


# define a main function to run the program
def main(hn: str = "localhost", qn: str = "Smoker_Temp_Queue"):
    """ Continuously listen for task messages on a named queue."""

    # when a statement can go wrong, use a try-except block
    try:
        # try this code, if it works, keep going
        # create a blocking connection to the RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))

    # except, if there's an error, do this
    except Exception as e:
        logger.error("ERROR: connection to RabbitMQ server failed.")
        logger.error(f"Verify the server is running on host={hn}.")
        logger.error(f"The error says: {e}")
        sys.exit(1)

    try:
        # use the connection to create a communication channel
        channel = connection.channel()

        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        channel.queue_declare(queue=qn, durable=True)

        # The QoS level controls the # of messages
        # that can be in-flight (unacknowledged by the consumer)
        # at any given time.
        # Set the prefetch count to one to limit the number of messages
        # being consumed and processed concurrently.
        # This helps prevent a worker from becoming overwhelmed
        # and improve the overall system performance. 
        # prefetch_count = Per consumer limit of unaknowledged messages      
        channel.basic_qos(prefetch_count=1) 

        # configure the channel to listen on a specific queue,  
        # use the callback function named callback,
        # and do not auto-acknowledge the message (let the callback handle it)
        channel.basic_consume( queue=qn, on_message_callback=bbq_temp_callback)

        # print a message to the console for the user
        logger.info(" [*] Ready for work. To exit press CTRL+C")

        # start consuming messages via the communication channel
        channel.start_consuming()

    # except, in the event of an error OR user stops the process, do this
    except Exception as e:
        logger.error("ERROR: something went wrong.")
        logger.error(f"The error says: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info(" User interrupted continuous listening process.")
        sys.exit(0)
    finally:
        logger.info("\nClosing connection. See you later.\n")
        connection.close()


# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # call the main function with the information needed
    main("localhost", "Smoker_Temp_Queue")