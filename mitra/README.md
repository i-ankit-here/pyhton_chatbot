# Title: Chatbot for website 
## Description: It allows users to easily find things up on the institute website

# How to install?
## run the following command in windows powershell to install required libraries:
###    pip install -r requirements.txt

# 1. Scraping website
## We have used "scrapy" framework of python for scraping NIT Jalandhar website. We have used a spider for crawling through the website to get all anchor tags their href attribute and text. We have used another spider to scrape out paragraph content from the anchor tags scraped out previously. This has been stored in a json file which contains text as title, href as url and paragraph as content.

# 2. Creating the Bot
## a. Data Preprocessing: Used NLP preprocessing techniques such as tokenization, lowercasing, punctuation removal, stop word removal, and lemmatization to clean and normalize textual data extracted from the JSON file containing the information.
## b. Intent Classification: Trained a machine learning model, Support Vector Machine (SVM), using TF-IDF vectorization, to classify user queries into predefined intents based on the content in the json file. The parameters supplied to the pipeline were processed using NLTK processing first.
## c. Response Generation: Created a logic to generate response from the chatbot based on the user input. A dictionary was created to store different domains and subdomains of queries user can choose from. The user input is passed to the pipeline created before to predict intent. On basis of the user input and the intent predicted a response is generated which would be given by the bot.

# 3. Serving the bot
## We have used Flask framework for integrating our bot with the server.