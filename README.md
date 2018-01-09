# Super-Reminder---Microsoft-Azure
python flask app deployed on Azure cloud
A Python Flask-based web app which allows the user to save text files or pictures which serve as a list of things to do or a personal diary. Each file or a picture has a priority level which is the level of importance to each item. Handles scaling based on the number of users, scaling validated by using Apache JMeter for stress testing. Built using Python Flask, SQL and deployed on Microsoft Azure

code.py
    + Upload the food pair data (anywhere on Azure) and then create a web page that shows part 6 and the pictures.
      Please show NAMES of pictures below each picture.
      You may do this manually or through a web interface.
    + There is no "user" concept, no login, all people using this service are "users".
    + Create a web interface that allows a (any) user to see the web page. Show the time and the time it takes to respond 
      to the load request.
    + allow a user to query for all foods weighing between two values which we will supply,
      (for example, show pictures and names of all foods between 100 and 500 grams)
    + We wish to guarantee a QoS of at most 2 seconds from site/page request until that page is displayed. 
      Show how we can determine if that goal is met. (You do NOT need to meet that goal, just show whether you do or don't)
      show the performance of your application.
    + Give one method (explain or give code) where you allow a login and only allow those users to upload their own foods.
    + allow a user to query for all foods with a specified ingredient. Show matching entries (pictures).
    + show top 5 requested ingredients.
    + show how a SQL injection would occur in your code, or explain why it could not.
    + show how one can find a "snack" (or other genre/type) with less than a specified number of calories.
