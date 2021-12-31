# Spring Revolutionaries Hub
A website for supporting Myanmar people financially and spiritually during their revolution

# Purpose 
When I considered about the idea for the final project, I desired that my project would have a real-world impact rather than being just for the submission. With that premise, I, as a Burmese, couldn't see the idea other than the one that can contribute in Myanmar's Spring Revolution. This is the reason why I was determined to implement this idea despite the project being concerned with politics.

# Overview
## Features
This website comprises mainly of two features, named ***Donations Hub*** and ***Stay Connected***, both of which are designed to help Myanmar People in resisting against the inhumane terrorism to some extent. Besides, links to other websites or organisations that can be of great helps to revolution in different means are also recommanded. 

### Donations Hub
Even though links leading to donation recipients are prevalent in social media, they are essentially not centralised, resulting in links being scattered. ***Donations Hub*** will hopefully mitigate this subtle inconvenience by compiling as many links as possible somewhat as a **centralised source**, and ficilitate searching for appropriate locations to donate with **category** and **ordering system**.

![Donations Hub Demo](springrevolution/static/springrevolution/images/donations_hub.gif)


### Stay Conneccted
**Stay Connected** is the feature that users can optionally subscribe to receive our service of **sending emails to their Gmail inbox** on the time interval they've set. Inside these emails are heartwarming, motivational, encouraing, comforting messages, which will hopefully help users have a sense of being connected and encouraged during this hard time.

![Stay Connected Demo](springrevolution/static/springrevolution/images/stay_connected.gif)

## Authentication System
This website follows real-world authentication procedures. Submitting the registration form, users will receive **confirmation email** in their Gmail inbox first. Only after the confirmation will they be added to the database. 

Should users happen to **forget** their **passwords**, they can also reset theirs via the link sent with the email.

> Login is required only for using ***Stay Connected*** feature.
***
# How Features Work

Data of this website, specifically <strong>links of donations</strong> and <strong>messages</strong>, is compiled with the help of users. Users can suggest links and leave messages via the forms under respective tabs. However, the data submitted will be sent to us first, from which whether or not the submitted data should be approved will be decided, which means that the submitted data will not be directly added to the database.

In order to be able to send emails on the time interval users have set for ***Stay Connected*** feature, there is a button under profile dropdown menu on navigation bar, which is only available to admin user. Every day, he has to manually click that _Start Mail_ button to send emails to all the users whose receiving dates are the same as that day. Then, their receiving dates will be incremented differently according to their subscription.

# Distinctiveness & Complexity
The nature of this website is conspicuously different from that of e-commerce and social networking web apps as can be inferred from the fact that it is concerned with neither shopping nor social interaction (The type of iteraction between users in ***Stay Connected*** feature is in fact inherently distinct to that of social media). Although it is true that some concepts from each earlier project have come into play in this website, it does not neccessarily mean resemblance to earlier projects in terms of features. 

The website also has extra code complexity, which predominantly lies upon dealing with automated emails. Moreover, it was indeed a time-consuming and brain-storming task to make single-page website available in efficient design especially due to handling not only tabs but also sub-tabs. 
While working on this project, I've indeed acquired substantial new coding knowledge.

# About Files & Folders
* HTML files inside _templates_ folder can be essentailly categorised into a layout file, display files, and email files.
* Inside _static_ folder are a CSS file for styling, a Javascript file for user interactions and API calls, and _images_ folder.
* _util .py_ contains two helper functions for _views. py_.
* _Procfile_ is created to be able to deploy the website on heroku web server. It tells Heroku the commands to run on the initialization of the app.
* Packages in _requirements.txt_ were automatically specified by running `pip freeze > requirements.txt`.
* _.gitignore_ is created to hinder environment variables specified in _.env_ file.

# Usage
This website is deployed on the internet using heroku server. 

URL - https://springrevolutionarieshub.herokuapp.com/index

# Architecture

This website is a single-paged web application (except for login and registration pages) built with Django framework. Google SMTP server is used to send emails to users and the developer for particular features. 

### Languages
* Frontend
    * HTML
    * CSS
    * JavaScript

* Backend
    * Python

* Database
    * SQlite

### Frameworks
* Django
* Bootstrap

# Acknowledgement
Icons made by [Freepik](https://www.freepik.com) from [Flaticon](https://www.flaticon.com/).

Credits for images are given to respective media companies and photographers.