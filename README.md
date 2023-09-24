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
