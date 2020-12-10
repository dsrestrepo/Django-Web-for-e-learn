1. Description: My project is named e-Learn, this is a project where I want to help people to find information about some topics like data science or computer science, but I also wanted to help people to contact with others that works or likes the same topics, so each one has a profile, can comment each course, and can even send direct messages to other users.
 
2. What the project does?:The project have two options
    
    2.1. See the content as not logged in: 
    -you can see the login page if you hava an acount and you want to login you can do it here with username and password
    -you can see the reggister page, if you want to create an account you can do it here with email, username and password
    -you can see the main page where you will have a preview of what you will find in each course 
    -you can see the content of each course and the comments
    As not logged in you can't:
    -you can't don any comment
    -You can't visit the profiles of other users or send messages to other users
    -You can't do the test
    -You don't have a profile
    
    2.2. See the content as logged in:
    -you can see the main page where you will have a preview of what you will find in each course
    -you can see each couse by clicking in the name but first you need to fill a small sirvey, in the course you can see the course's content, the comments, write comments and click to visit the profiles of each user, finally you can do the final test of each course.
    -you can visit your profile, in you profile you can see your personal information, you have also your courses, the results of your courses, your comments, you can edit your profile, send messages and see messages, (the messages you've not seen are in a different color than the messages that you've seen)
    -you can see other user's profile, in other user's profile you can see the same that you saw in your profile, except you can't edit the profile, see the messages, and see the resoults, but you can see the comments, the courses and send a message to the other user.
    -finally you can logout

NOTE: ALL THE FUNCTIONS CAN BE USED IN ANY SCREEN SIZE OVER 300px PERFECT FOR THE 320px OF THE iPhoneSE OR LARGER SCREENS

I think that this project meets the given requirements, because it has nothing to do with the previous projects, because is part of a idea that I had from time ago, although if it takes up some of what was learned in each one, it makes some models, javascript functions to modify the DOM, fetch functions, APIS, security, html and css, django's own functions such as pagination, login, logout, it is reponsive, among other things

3. what you'll find in the project files?:
The project've been created with django in backend and javascript in frontend, in the main directory you'll find:

-README.md
-manage.py
-a folder with the project name: webFinalDavid
-a folder with the app name: finalProject

    3.1 In webFinalDavid -> urls.py we add the app path ->  path("", include("finalProject.urls"))
        In webFinalDavid -> settings.py we add the app (finalProject) and the django auth for the user model

    3.2 In the app folder finalProject you'll find:
        
        3.2.1 models.py: As we saw this is like a courses's social network, so we neet the profile information, like personal data, but also some information about the course like answers or comments, and also some social data, like messages, so we use the models:
            
            -User: To save the user info of the dgango default user as password, email, username, name, lastname, but also we have the career, country or profession. Except password, email and username the values could be blank. 
            
            -Course: this model saves the info of the course (users, description, course_name) The users field have a many to many relation with Course so a User can have many Courses and a Course can have many users, the course also have a course name, and a description (the one that wee see in the index)
            
            -Test: This model saves the info of the presented test (test_version, user, course, result); where the test version could be the first test, second test or final test; the user is a foreign key with User(The one who did the test); the course has a foreing key with Course (the course where the test was done), finally the result is how many answers were done well in the test.
            
            -TestData: This model saves the most specific data of each test (test, question1, ..., question6), the test is a foreing key with Test (wich test are those anwsers from), and from question1 to question6 are the answers, the test are multiple options, so the answers are from 1 to 6.  
            
            -Comment: The Comment have the info of the comments (user, content, timestamp, course), the user is a foreing key with User(the one who did the comment); the content is the comment done by the user, the timestamp is the datetime the commend were done, and finally, the course is a foreing key with Course, this tell us the course where the comment were done
            
            -Message: The Message this have the infor of the direct messages (sender, content, timestam, user), the sender is a Foreing key with User, this is the user who've the message, the content is the message, the timestamp is when the message were done, and the user is too a Foreing key with User, but this is the user who recive the message.
            
            All those models have a funtion to serialize the data, and a __str__ to give a description.


        3.2.2 admin.py: The admin.py have the data the admin will see in the interface, so uses all those models we saw befor, and also each model has an Admin version, with this classes the admin can see in his interface a table of the data that each model have, also the CourseAdmin class have a get_users functions for the many to many field to display all the users in one line.


        3.2.3 urls.py: Here we have the routes of the app, we have each route related with a function in views.py and a name used in many parts of the django template to relate beteween pages. we have two types of route 
        
        routes that return a template:
            "" related with views.index
            "login" related with views.login_view
            "logout" related with views.logout_view
            "register" related with views.register
            "course/<str:cname>" related with views.course
            "make_test" related with views.make_test
            "profile/<str:username>" related with views.profile
        
        Routes of the API
            "test" related with views.test
            "newPost" related with views.newPost
            "newMessage" related with views.newMessage
            "read" related with views.read
            "editUser" related with views.editUser


        3.2.4 views.py: Here we will find the functions of each route or the urls.py so we have the functions (all the funtions need the request, if the function needs extra info will be in perentesis):
        
        return a template:

            -index: This function just returns a template with the index
            
            -login_view: This function takes a POST with the username and password to compare with the database, if the user exist do the login and returns the index viwe if not exist send an error message saying password or email invalid.
            
            -logout_view: This is a view that juss work if the user is logged, just logout the sesion and returns the main
            
            -register: This view is used to create a new user, takes a POST request with username, password ans email to create the object in the user database, if there are not problems like the email or username alredy exist this function returns the main view with a logged user, else this view returns the error message.
            
            -course(cname):This view show the course, uses the variable cname that represents the course name to display different changes in the template deppending of each course, this function returns the course template, this templete changes if the user is logged in, or not (things like the comment box, or the final test), if the user is logged this function also verify if the couse exist in database, if it doesn´t exist create the course, if it exist, but the user is not in the course returns a survey to register in the course, if the user is in the course returns the course information and the final test, except if the user've alredy done the final test, then display the resoult and the course data 
            
            -make_test: This is the function for the first survey to register the user in the course, takes a POST request with the version of the test(in this case the first), the course of the test and the answers of the 6 questions, saves this information in the database in the Test table, and the TestData table, and then send the user to the course view that displays the course info and the final test.
            
            -profile(username): this function renders the profile uses the username of the profile to display to do it, this function also compares this username with the user of the request to see if is the own profile of the user or not in this function, this funtion also captures the comments of the user, the courses of the user, the messages of the user, the resoults of the tests, and the profile information, but some of this data like messages or resoults is just used if the profile is of the own user.
        
        return a json respone: (all this functions needs a csrf token and a user logged)

            -test: This function does something similar to make_test, the difference is that make_test is done just for the first test, because is a survey so it uses a result as a default result of 5, also make_test renders all the course content and the test api is better for cases like the final test because we just need to render the result, this functions requires a POST, with the test data, like the version, the course and the answers, calculate the result and if all is ok send the message to the frontend in a json with the result of the test from 0 to 5
        
            -newPost: This function create the comment, requires a POST, with the data of the Comment like course, user and the content of the comment, if all is ok, creates the comment and returns a JSON with the message
        
            -newMessage: This functions create the direct Message in the database, requires a POST with the data of the Message like the message and user (the one who receives the message), if this user exist this function takes other user from the request to send the message, if the user sender is the same receiver then mark the message as read by default, else the message is not read, and then with this information creates the Message in the data base, if all is ok send the confirmation message in a JSON response, else send an error in the JSON response
        
            -read: This function uses a PUT method with the id of the message to edit, if the message exist it changes the status to read and if all is ok send a JSON response with a message, else send an error with the error
        
            -editUser: This funtion edits the user profile in the database, this function requires a PUT with the data of the user to edit, for example the email, the country, career, profession, or more, with this information we see if the user exist, and we can change the user information just if the user is the same user of the request, if all is ok this function returns a JSON response with the confirmation message else this function returns an error 


        3.2.6 templates/finalProject: Here we have 5 templates asociated with functions of views.py, and a layout, so the templates are:
            
            -layout.html: The layout is the main structure that the other templates uses, here we have things like:
                *the title
                *the styles: one is prism, this is a libray to display code in the page, bootstrap other styles library, and the other is styles.css (my custom styles)
                *the javascript libraries like, marthjax(for latex ecuations), chart.js(for charts), tensorflow(for some tensor operations)
                *the navbar with the main button, and:
                    -if user is not logged in: buttons of login and register
                    -if user logged in we have the profile and the logout button asociated with the logout_view in views.py  
            
            -Register.html: This is the template that have the register form, with the email, username, password and confirm password, this form is asociated with the register function in views.py

            -login.html: This template is the template that have the login form with the username and the password, this form is asociated with the login_view in views.py
        
            -index.html: This is the main page, here we have the courses, each course in a card where we'll find the image of the course, the link of the course's page in the title, the description of the course, and other button with the link of the course.

            -profile.html: This is the profile of the user, this layout is just for logged users, here we have
                *a header div with the information of the user like username, name, country, etc...
                *a toggle grup of buttons (Controled in a javascript function in profile.js) with the options  of the course, the options are:
                    -if is the own profile: Courses, Comments, Send message, Results, Edit Profile, See messages
                    -If is other user's profile: Courses, Comments and Send message
                *each button has a div with asociated with the content to display so we have the divs with:
                    -The courses the usser is doing and have done
                    -The test the user've done and the result of each test
                    -The edit profile with a form that has the filed of email, First name, Last name, Country, Porfession and Career, this is asociated with a javascript function in profile.js that does the changes and sends the request to editUser funtion in views.py
                    -The send a message, this have a form to send a message, to other user (also asiciated with a javascript function in profile.js that send the message to backend in newMessage in views.py)
                    -The Read messages, here the user can see his messages and mark as read, to mark a message as read the user just click the button and a javascript function in profile.js does the process to change the color and send the request to the read function in views.py
                    -Finally the Comments, in this div we display the comments done by the user, in cards with the comment, the course, the date, and the username, this div also have the paginator that displays 10 comments for page and show us which page we are and the option to go trough other pages.
            
            -course.html: This is the longest html, but the reazon is that each course is absolutley different, and each course have a different test, so here is a summary of what this html does:
                *This templete always display the comments of the course (at the end of the html)
                1.See if user is in course (if user is not logged in then is in course), here we have two options:
                    -if user is NOT in course we will display a form with the first survey, (this survey is allocated near the end of the html above the comments), this form is related with a POST to make_test function in views.py
                2. if user is in course (or not logged in) we have some if's for each course to see wich course we are searching then we display the course's content:
                    -each course have some buttons with the chapters if we click the buttons we can see the chapter, these buttons are controlled by a function in profile.js
                    Note: in the statistics course in linear regression we have a chart controled by linear_regression.js
                3. In course see if user is logged in, here he have two options:
                    -if user IS NOT logged in we don't display the final test, and the comment form
                    -if user IS logged in:
                        -we display the final test button that controls the final test helped by a functions in profile.js to display the final test div and to send the final test; If user've done the final test we display the result
                        -we display the form of the comments to let the user comment about the cpurse.

        3.2.7 static/finalProject: Here we'll find the static files as javascript files, images, or css, in this case we have:
            
            -.pgn files: this files are the page's logo, the logo of each couse, and some images used in some courses's content
            
            -styles.css: This is the file were we can find the stiles of the page, have the styles to center thigs, to make some things responsive, like the images or videos, change the color or size of some thing and finally we have some different styles in some screen size like under 800px, 600px or 400px

            -prism.css and prism.js: this is a library to dislay a block of code in html

            -profile.js: This is the javascript of the profile.html this controls the functions of:
                *loads the initial configuration of the profile.html
                *Control the toggle buttons that display the different profile options
                *edit Profile, this functions is activated when the form of edit profile is sumbited then this function captures the information in the form and sends these information in a fetch to the editUser funtion in views.py, with the result of this fetch we can display the changes in the profile changing the html.
                *Send New Message, this funtion is activated when the form of sumbit a message is submited, then this function captures the data and uses a fetch to send these data to newMessage in views.py if all is ok we display the message, if there are problems, show display the error.
                *read message: this is so simple, when the user click in a message, not read this function does the request in a fetch to the read function in views.py to change the status of the message, if all is ok the fetch gets a message, and this function changes the color of the message

            -linear_regression.js: This is used in the statistic course to display a linear regression's chart
            and to display the data used to do the chart, here we use the functions of tensorflow and chart.js

            -course.js: This is the javascript that control the course.html actions, have funtions for:
                *loads the initial configuration of the course.html
                *control the buttons that display course items and final test and does the action to display or hide these sections.
                *send final test if the user've done the final test and click in send this function gets the
                answers and send these data in a fetch to the test function in views.py, this function also get the response of the fetch to display the result
                *create a new post (or comment): this function captures the request of a new comment in the course.html and uses the data to send a fetch to the newPost function in views.py to write the new post. 
