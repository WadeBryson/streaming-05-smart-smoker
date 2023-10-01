# Streaming-05-Smart-Smoker

## Prerequisites

1. Git
1. Python 3.7+ (3.11+ preferred)
1. VS Code Editor
1. VS Code Extension: Python (by Microsoft)
1. RabbitMQ Server installed and running locally

## Description
1. somker-temps.csv contains readings from a smart-smoker. Every 30 seconds it is reading the timestamp, smoker temp, food1 temp, and food2 temp.
1. BBQ_Temp_Producer creates a producer that passes three different messages to three different queues.
     - Message 1 - Time of Day, Smoker Temp
     - Message 2 - Time of Day, Food 1 Temp
     - Message 3 - Time of Day, Food 2 Temp
1. BBQ_Temp_Listener creates a consumer that reads the smoker temperature from the Smoker_Temp_Queue. It will alert the user if their smoker temperature decreases by more than 15 degrees in 2.5 minutes.
1. Temp_Food1_Listener creates a consumer that reads the Food1 temperature from the Temp_Food1_Queue. It will alert the user if their Food temperature does not increase by at least 1 degree in a 10 minute window.
1. Temp_Food2_Listener creates a consumer that reads the Food2 temperature from the Temp_Food2_Queue. It will alert the user if their Food temperature does not increase by at least 1 degree in a 10 minute window.

## Screenshot

See a running example with at least 3 concurrent process windows here:

<img align="center" width="921" height="483" src="BBQ Producer.png">
<img align="center" width="921" height="483" src="Smoker Listener.png">
<img align="center" width="921" height="483" src="Food 1 Listener.png">
<img align="center" width="921" height="483" src="Food 2 Listener.png">
<img align="center" width="921" height="483" src="RabbitMQ Screen Shot.png">
