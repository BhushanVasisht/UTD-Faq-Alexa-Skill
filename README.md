Build an Alexa UTD skill for frequently asked question.

## Team Member

###Arihant Chhajed 
###Bhushan Vasisht 
###Parva Shah    

## Concepts
This lambda function is created for hackutd hackathon. This function shows how you can pass alexa query and pass to external web service which performs all the NLP part,which find matches the query with its existing dataset and answers if match found

## Setup
To run this example skill you need to do three things. 

### The first is to deploy the example code in lambda

### The second is to configure the Alexa skill to use Lambda.

### You will also require to setup our faq nlp engine which finds the semantic similarity between the input query and existing query using which it reply with the correct answer with some confidense score.

####PLease Note: We have created a web crawler which crawls the utd web pages to generate the dataset

## Example Conversation

###User: Alexa, Open Comet Guide

###Alexa: Welcome to Comet Guide! Ask something to hear about the university of texas at dallas and its services... Currently I can answer you housing, alumni, counseling related queries... So... which option would you like to go for?

###User: First // Here "Housing,2nd,etc -- anything will work. We are storing this information in context memory of alexa

###Alexa: Ok... Thank you for your response... Now you can ask me your queries with hot keyword... 'tell me'

### Tell me, What are the dates of my housing agreement
### Alexa:- All housing agreements are for the complete 2018-19 academic year.
