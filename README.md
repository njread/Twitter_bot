# Twitter bot
For this project we are going to make a twitter bot that checks to see if you have posted to git hub and if you have Tweet out the the repos that you updated for the day. 

## What was used
For this project I decided to use a web app `Heroku` to keep the code running so I didn't have to run the program every day. Other wise I would just tweet it out my self and I really don't need any more excuses to go on twitter everyday. To build the bot I used the Twitter api through `tweepy` and to pull the git hub commit history I used a great package `PyGithub`. Both are fairly user friendly and have good documentation to help you out. 

## Code

This is  a fairly easy code to create only about 20 lines or so. The logic for this project is as follows:
- Import the necessary libraries via `pip`  
- Go to twitter and sign up for a developer license 
- Generate your keys for the Twitter account
- Set the keys in the code (side note **DO NOT** put your keys in the actual code if you are going to publish it on any public site like git hub) 
- Link up your git hub username and password
- Standard control  flow of `while loop` , `for loop` and an `if statement`. The `for loop` to check each repos latest commit date the `if statement` checks the dates against the current date if they match posts a tweet and the `while loop` to keep everything running indefinitely. 
- Write a simple server to host the web app on Heroku 
- Use Heroku integrated with git to push your code up to a web app so that it can run independent of your machine. 
- Use the command `heroku run python "your file name"`to run your code. 
  

## conclusion 
This project is fantastic for anyone that is starting out with programing. It's very rewarding to see a tweet pop up that you made through the twitter API and its even more rewarding to do it through an automated process. There are a few ways to tackle this problem and although Heroku doest always play nice it is good practice in package management and making sure commits are in the right order. I would recommend this project to anyone who is interested in making web applications or fun and simple twitter bots.