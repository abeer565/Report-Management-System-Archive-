from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
#from flask_migrate import Migrate , MigrateCommand
#from flask_script import Manager


from sqlalchemy.orm import relationship
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.config['Secret_Key'] = "me"
app.secret_key = "Secret Key"
DB_HOST ='localhost'
DB_NAME ='rsma'
DB_USER ='postgres'
DB_PASS=''
#conn = psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:''@localhost/rsma"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#migrate = Migrate(app, db)
#manager = Manager(app)
#manager.add_command('db',MigrateCommand)



admin = Admin(app, name='Control Panel')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'




###
@login_manager.user_loader
def load_user(id):
    curr_user = Users.qeury.get(int(id))
    return curr_user
###


#Create a form class
class NameForm(FlaskForm):
    name = StringField("What's Your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

#the relationship
# group has many reports ,so one to many
# the user belongs to many group
# the group has many users
###
users_group =db.Table('users_group',
            db.Column('user_id',db.Integer, db.ForeignKey('users.id'),primary_key=True),
            db.Column('group_id',db.Integer, db.ForeignKey('groups.id'),primary_key=True),
)
####
class groups(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    user = db.relationship('Users',secondary=users_group, backref=db.backref('userggroup'),lazy='dynamic')
    #Group Can have many reports
    report = db.relationship('reports', backref='report',lazy='select')

    def __init__(self,title):
            #self.id =id
            self.title = title
            #self.user = user
            #self.report = report

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), unique=True)
    user_password = db.Column(db.String(255))
    user_email = db.Column(db.String(255), unique=True)
    is_admin = db.Column(db.Boolean ,default=False)
    #group_id = db.Column(db.Integer, db.ForeignKey('groups.id')) #group id
    #g = db.relationship('groups',secondary=users_group, back_populates='user')

    def __init__(self, id, user_name, user_password, user_email ,is_admin):
        self.id = id
        self.user_name = user_name
        self.user_password = user_password
        self.user_email = user_email
        self.is_admin =is_admin
        #self.group_id = group_id
        #self.userggroup = userggroup



###
class reports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_name = db.Column(db.String(50), unique=True)
    report_content = db.Column(db.String(50))
    #report_group = db.Column(db.String(255),unique=True)
    report_editor_uploader = db.Column(db.String(255) ,unique=True)
    report_tag = db.Column(db.String(200))
    report_related_files = db.Column(db.String(200))
    # foreign key to link group
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))

    def __init__(self, report_name, report_content, report_editor_uploader,report_tag, report_related_files):
        self.report_name = report_name
        self.report_content = report_content
        #self.report_group = report_group
        self.report_editor_uploader = report_editor_uploader
        self.report_tag = report_tag
        self.report_related_files = report_related_files
        #self.group_id = group_id


####
#rolles and permissions
class Controller(ModelView):
     def is_accessible(self):
         if current_user.is_admin == True:
             return current_user.is_authenticated # this is if the user authenticated the user can acess the admin dashboard
         else:
             return abort(404) # this in flask i can abort error that will be shown if the user in not an admin
         #return current_user.is_authenticated
     def not_auth(self):
         return "you are not authorized to used the admin dashboard" # if the user not authoriced to enter the page this message will appear.
###


admin.add_view(Controller(Users,db.session)) ## admin page
#using to uniqe idinttey for each login user
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/creat_admin',methods=['GET','POST'])
def creat_admin():
    if request.method == 'POST':
        new_user = Users(user_name=request.form['user_name'],user_email=request.form['user_email'],user_password=request.form['user_password'],is_admin=True)
        db.session.add(new_user)
        db.session.commit()
        return "you have created an admin account Successfully !!"
    return render_template('admin_signup.html')


@app.route('/user_table')
@login_required  # this line has been added to protect the page.
def user_table():
    users = Users.query.all()
    return render_template('user_table.html',users=users)


@app.route('/home')
@login_required # the login is reqired to enter the system ,this means the user has to login to enter this page .
def Index():
        user_id= current_user.id
        print("current user id ")
        print(user_id)
        user = Users.query.filter_by(id=user_id).first()
        print("is admin ")
        # if the current user is admin ,all reports will be diplayes
        if user.is_admin == True:
            all_data = reports.query.all()
            return render_template("index.html",reports=all_data)
        elif user.is_admin == False:
            all_ = reports.query.all()
            gg = groups.query.all()
            users_group_list = db.session.query(users_group).filter_by(user_id=user_id)
            ggg = db.session.query(groups).filter_by(id=user_id)
            list1 = []
            results = reports.query.all()
            for i in users_group_list:
                #if (report_name in i.group_id) is True:
                list1.append(i.group_id)
            print(users_group_list.count())
            userr = db.session.query(Users).filter(Users.id == user_id).first
            group = groups.query.all()
            return render_template("not_admin_home_page.html" ,ggg=group,curr_user=user_id,gu=users_group_list,r=all_,g=gg,gl=list1)
        else:
            return "Not a user"

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_password = request.form['user_password']
        user_email = request.form['user_email']
        new_user = Users(user_name=user_name, user_password=user_password, user_email=user_email)
        db.session.add(new_user)
        db.session.commit()
        return "Welcome Sigh Up Copmete"
    return render_template("signup.html")

@app.route('/login', methods =['GET','POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_password = request.form['user_password']
        user = Users.query.filter_by(user_name=user_name).first()
        if user:
            if user.user_password == user_password:
                login_user(user)
                return redirect(url_for('Index'))
            else:
                flash("Invalid user name or password", 'error')
                return render_template("login.html")
    return render_template("login.html")


@app.route('/insert',methods=['POST'])
def insert():
    if request.method =='POST':
        report_name = request.form['report_name']
        report_content = request.form['report_content']
        report_editor_uploader = request.form['report_editor_uploader']
        report_tag = request.form['report_tag']
        report_related_files = request.form['report_related_files']
        #group_id = request.form['group_id']

        my_data = reports(report_name, report_content,  report_editor_uploader, report_tag, report_related_files)
        db.session.add(my_data)
        db.session.commit()

        flash("Report has been added Successfully !!")
        return redirect(url_for('Index'))

@app.route('/update',methods =['GET','POSt'])
def update():
    if request.method =='POST':
        my_data = reports.query.get(request.form.get('id'))
        my_data.report_name = request.form['report_name']
        my_data.report_content = request.form['report_content']
        #my_data.group_id = request.form['group_id']
        my_data.report_editor_uploader = request.form['report_editor_uploader']
        my_data.report_tag = request.form['report_tag']
        my_data.report_related_files = request.form['report_related_files']

        db.session.commit()
        flash("Report has been updated Successfully !!")

        return redirect(url_for('Index'))


@app.route('/delete/<id>/',methods =['GET','POSt'])
def delete(id):
    my_data = reports.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Report has been deleted Successfully !!")
    return redirect(url_for('Index'))

##search
@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/reportresult",methods=['POST'])
def reportresult():
    report_name = request.form.get("report_name")
    report_content = request.form.get("report_content")
    report_tag = request.form.get("report_tag")
    title = request.form.get("title")
    #title = request.form.get("title")
    report_editor_uploader = request.form.get("report_editor_uploader")
    #session = Session()
    #results = session.query(reports).all()
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    results = reports.query.all()
    for i in results:
        if (report_name == ''):
            print("report name is empoty")
        elif (report_name in i.report_name) is True:
            print("i am here in search first if")
            list1.append(i.report_name)
            list2.append(i.report_content)
            list3.append(i.report_tag)
            #get group titile
            group_id = i.group_id
            group = groups.query.filter_by(id=group_id).first()
            list4.append(group.title)
            list5.append(i.report_editor_uploader)
        if (report_content == ''):
            print("report_content is empty")
        elif (report_content in i.report_content) is True:
                print("i am here in search first if")
                list1.append(i.report_name)
                list2.append(i.report_content)
                list3.append(i.report_tag)
                group_id = i.group_id
                group = groups.query.filter_by(id=group_id).first()
                list4.append(group.title)
                list5.append(i.report_editor_uploader)
        if (report_tag == ''):
            print("report tag is empoty")
        elif (report_tag in i.report_tag) is True:
            print("i am here in search first if")
            list1.append(i.report_name)
            list2.append(i.report_content)
            list3.append(i.report_tag)
            group_id = i.group_id
            group = groups.query.filter_by(id=group_id).first()
            list4.append(group.title)
            list5.append(i.report_editor_uploader)
        if (report_editor_uploader == ''):
            print("report_editor_uploader is empoty")
        elif (report_editor_uploader in i.report_editor_uploader) is True:
            list1.append(i.report_name)
            list2.append(i.report_content)
            list3.append(i.report_tag)
            group_id = i.group_id
            group = groups.query.filter_by(id=group_id).first()
            list4.append(group.title)
            list5.append(i.report_editor_uploader)

        if  (title == ''):
            print("title is empoty")
        else:
            group = groups.query.filter_by(title=title).first()
            group_id = group.id
            if (str(group_id) in str(i.group_id)):
                list1.append(i.report_name)
                list2.append(i.report_content)
                list3.append(i.report_tag)
                group_id = i.group_id
                group = groups.query.filter_by(id=group_id).first()
                list4.append(group.title)
                list5.append(i.report_editor_uploader)

    return render_template("reportresult.html", count=len(list1), result1=list1, result2=list2, result3=list3, result4=list4, result5=list5)
    db.session.commit()

#GM page
@app.route('/group_managment')
@login_required # the login is reqired to enter the system ,this page will apear only for the admin
def group_managment():
    group = groups.query.first()
    user = Users.query.first()
    usergroup = group.user.all()
    users = Users.query.all()
    groupp = groups.query.all()
    reportss= reports.query.all()


    return render_template("group_managment.html",users=users,groupp=groupp ,reportss=reportss,usergroup=usergroup)



@app.route('/creat_group',methods=['GET','POST'])
def creat_group():
    users = Users.query.all()
    if request.method =='POST':
        title = request.form['title']
        report = request.form['report']
        print("the group  title")
        print(title)

        userggroup = request.form.getlist('userggroup')
        #userggroup = request.form['userggroup']
        print("hello users")
        print(userggroup)
        my_data = groups(title)
        db.session.add(my_data)
        db.session.commit()
        ##
        group_ = db.session.query(groups).filter_by(title=title).first() #group
        group_id = db.session.query(groups.id).filter_by(title=title).first()
        print("group id is ")
        print(group_id)
        # user list
        for x in userggroup:
            print("i am in the loop")
            print(x)
            new_user = db.session.query(Users).filter(Users.user_name == x)  # users
            group_.user.extend(new_user)
            db.session.add(group_)
            db.session.commit()
            ##
        # end for loop
        #update the group_id for the reports
        report = reports.query.filter_by(report_name=report).first()
        group_id = groups.query.filter_by(title=title).first()
        report.group_id = group_id.id
        db.session.commit()
        ####
        flash("Group has been Successfully Created !!")
    return redirect(url_for('group_managment'))
########
########



@app.route('/update_group',methods =['GET','POSt'])
def update_group():
    if request.method =='POST':
        my_data = groups.query.get(request.form.get('id'))
        group_id = my_data.id
        title = request.form['title']
        currnt_user = request.form.getlist('currnt_user')
        userggroup = request.form.getlist('userggroup')
        currnt_report = request.form.getlist('currnt_report')
        updated_report = request.form.getlist('updated_report')

        #update group titile
        my_data.title = request.form['title']
        db.session.commit()
        print("the cuurent report are")
        print(currnt_report)
        ##loop start here
        # remove current user list to updated with the new one
        countt = 0
        if len(currnt_user) > 0: # theis ststments check if theier is any current user
            for x in currnt_user:
                print("i am in the remove loop")
                print(x)
                user = currnt_user[countt]
                update_users = Users.query.filter_by(user_name=user).first()
                group = groups.query.filter_by(title=title).first()
                group.user.remove(update_users)
                countt += 1
                db.session.commit()
        # Updated user list
        count = 0
        for x in userggroup:
            print("i am in the new updated loop")
            print(x)
            user=userggroup[count]
            update_users = Users.query.filter_by(user_name=user).first()
            group = groups.query.filter_by(title=title).first()
            group.user.append(update_users)
            count += 1
            db.session.commit()

        countt=0
        if len(currnt_report) > 0:  # if their are
            # remove current report list
            for x in currnt_report:
                print("i am in the remove loop")
                print(x)
                curreport = currnt_report[countt]
                current_report = reports.query.filter_by(report_name=curreport).first()
                current_report.group_id = group_id
                countt += 1
                db.session.commit()
        # Updated report list
        count = 0
        for x in updated_report:
            print("i am in the new updated loop")
            print(x)
            report = updated_report[count]
            print("current report")
            print(report)
            update_report = reports.query.filter_by(report_name=report).first()
            print("group_id")
            print(group_id)
            update_report.group_id = group_id
            print(update_report.group_id)
            count += 1
            db.session.commit()
        flash("Group has been updated Successfully !!")
        return redirect(url_for('group_managment'))

@app.route("/logout")
def logout():
    logout_user()
    #return "You have logout see you soon !!  <a href='/home'> Click Here to go to the home page</a>"
    return render_template("login.html")
## end_search

##search

## end_create_user_group

@app.route('/delete_group/<id>/',methods =['GET','POSt'])
def delete_group(id):
    my_data = groups.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Group has been deleted Successfully !!")
    return redirect(url_for('group_managment'))


if __name__ == "__main__":
    app.run(debug=True)
