
# Report Management System (Archive)

this is a project of CRUD system with users and admin role. 
## Inroduction 

    Frontend 
    - html 
    - css 
    - bootstrap

    bakckend
    - SQLAlchemy 
    - Postgresql (Postgres.app with PostgreSQL 14 (Universal))
    - flask 

    coding programs 
    - terminal (cmd in macbook pro)
    - Pycharm CE
    
    some needed libraries needed to be pip and install and the main were:
        - Starting by pip install flask-sqlalchemy in terminal
        - Successfully installed flask-sqlalchemy-2.5.1
        - depndecie needed to be installed pip3 install Flask-WTF
        - pip install sqlalchemy-utils
        - pip install PyMySQL
        - etc..
    
## CRUD system
    Strted by programing the CRUD system with the needed functionality
        - Contents of the Home page
            - Managing Reports table 
                the table show the report's id and name   
            - Main function in the RSMA sysetem 
                - Create new Report 
                - Add new Report
                - Delete report 
                - View report content 

## Database
    - Started by downloading the needed app and libraries to establish the Postgre ,SQLAlchemy dtatbase 
    - The Database has been created in terminal becouse ,I used Postgresql and also in the main file app.py
    - the needed seeting has been added to the fasl files to access the created database and tables. 
    - The Database has been named rsma 
        - inside the db four tables have been created called reports ,users , groups , (assosiation table (users_group))
            - reports table 
                - the colomns are :  
                        - id (PRIMARY KEY)
                        - report_name
                        - report_content
                        - report_editor_uploader
                        - report_tag
                        - rreport_related_files
                        - group_id (FOREIGN KEY)  REFERENCES the id in the groups tabel
            - Users table 
                - the colomns are :  
                        - id (PRIMARY KEY)
                        - user_name
                        - user_password
                        - user_email
                        - is_admin (the colomn has been created and boolean and by defualt=false)
                        - group_id (FOREIGN KEY)  REFERENCES the id in the groups tabel
      
            - groups table 
                - the colomns are :  
                        - id (PRIMARY KEY)
                        - title
                        
            - users_group (assosiation table) 
                - the colomns are :  
                        - id (PRIMARY KEY)
                        - user_id  (FOREIGN KEY)  REFERENCES the id in the Users tabel
                        - group_id (FOREIGN KEY)  REFERENCES the id in the groups tabel
                        
            - Realationships 
                        - Many-to-many 
                            - bettwen Users and Groups table 
                                - every user belongs to many groups and every groups have many users
                        - One to many 
                            - bettwen Groups and Reports table 
                                - One groups have  many reports 
                                - and report belongs to one group
                  
# system pages 
   -signup
   - login
   - home page for (the admin to display all the reports)
   - home page for (the user that is not an admin to display just the reports who have permissions on it)
   - admin dashboard (Users CRUD) (Just for admins)
   - Group Managment (Groups CRUD) (Just for admins)
   - search this is includs in the home page toolbar
   - reportresult 
   - user tble (jusr an extra)

## Search
    -Search using different criteria.
           - you have the choice to search by report name or report_content or  report_tag or report_group or 
             report_editor_uploader
     - the search result will display in the reportresult.html  
           - a "Go Back" button has been added to the page ,once you press it will direct you back. 
       
## Flask login 
       - Instaling flask-login
       
## Signup page has been established (as an extra) ,you need to signup to enter: 
                            - user_name
                            - user_password
                            - user_email
                            
## login page has been established and you need to login to enter : 
                            - user_name
                            - user_password
                            - Note/ if the user enter a wrong password or username the system wil alert the user.  
        ### Note: a login functioality has been established that mean you have to be login to access the system.
        ### Note: you need to be logined to use the system ,it has been protedcted that means the user need to login inorder to                       enter all the pages in the system. 
     
## logout page has been added. 
       ### after the user logout the system will direct him to login page. 
                       
# Flask Admin
   - Instal flask-admin
   - In flask you can import flask admin to help us with the managing the user. 
   - So flask admin has been imported and I linked to the user table then the CRUD ability for managing the users by the admin        has been established. 

# Authnitication and roles 
    - if the user is not logged-in ,the user will not be allowd to enter the system.
    - same for the admin dashboared , if the the admin user not logged-in to the system he will not access it.
    - Admin dashboard link
            - If you are an admin you will see an admin dashboard link in the left side of the home page that will direct you to               the admin page after press it. 
# Admin dashboard (CRUD) : 
    - display all the system users in a in the user list.  
    - Creat user
    - Edit user 
    - delete user
    - the admin can assign the users to any group.        
# Group Management (CRUD) 
     - If you are an admin you will see an Group Management link in the left side of the home page that will direct you to it. 
     - about the page: 
        - display all the system groups in a in the Group managment table.  
        - Creat group
        - Edit group 
        - delete group
# Go back button 
        - this button will direct the user to go back. 
