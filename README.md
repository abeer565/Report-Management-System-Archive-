
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
    - terminal (cms in macbook)
    - Pycharm CE
    
    some needed libraries 
    - Starting by pip install flask-sqlalchemy in terminal
    - Successfully installed flask-sqlalchemy-2.5.1
    - depndecie needed to be installed pip3 install Flask-WTF
    - pip install sqlalchemy-utils
    - pip install PyMySQL
    
## CRUD system
    Strted by programing the CRUD system with the needed functionality
        - Contents of the Home page
            - Managing Reports table 
                the table show the report's id and name   
            - Main function in the RSMA sysetem 
                - Add new Report
                - Delete report 
                - View report content 

## Database
    - Started by downloading the needed app and libraries to establish the Postgre ,SQLAlchemy dtatbase 
    - The Database has been created in terminal becouse ,I used Postgresql
    - the needed seeting has been added to the fasl files to access the created database and tables. 
    - The Database has been named rsma 
        - inside the db two tables have been created called reports ,users 
            - reports table 
                - the colomns are :  
                        - id 
                        - report_name
                        - report_content
                        - report_group
                        - report_editor_uploader
                        - report_tag
                        - rreport_related_files
            - Users table 
                - the colomns are :  
                        - user_id 
                        - user_name
                        - user_password
                        - user_email
                        - user_role
                        - user_group
                        - is_admin
## Search
    -Search using different criteria.
           - you have the choice to search by report name or report_content or  report_tag or report_group or report_editor_uploader.
     - the search result will display in the reportresult.html  
           - a "Go Back" button has been added to the page ,once you press it will direct you to the home page of the system. 
       
## Flask login 
       - Instaling flask-login
       - User table has been created in postgre database using terminl
       - signup page has been established (as an extra) ,you need to signup to enter: 
                            - user_name
                            - user_password
                            - user_email
                            - user_role (Admin or regular user)
                            - user_group
       - login page has been established and you need to login to enter : 
                            - user_name
                            - user_password
        ### Note/ a login functioality has been established that mean you have to be login to access the system. 
        - logout page has been added. 
        - for the  the home page and the table users page ,it have been protedcted that means the user need to login inorder to enter theses pages. 
                       
# Flask Admin
   - Instal flask-admin
   - In flask you can import flask admin to help us with the managing the user. 
   - So flask admin has been imported and I linked to the user table then the CRUD ability for managing the users by the admin has been established. 

# authnitication and roles 
    - if the user is not logged-in ,the user will not be allowd to enter the system.
    - same for the admin dashboared , if the the user not logged-in the system it will not access it.
