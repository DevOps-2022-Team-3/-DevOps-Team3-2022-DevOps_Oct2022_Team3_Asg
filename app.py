import os
from os.path import join, dirname, realpath
from flask import Flask, request, render_template, url_for, flash, redirect


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
import requests


import pandas as pd

flaskApp = Flask(__name__)

webhook_url = "https://www.workato.com/webhooks/rest/a30675cf-588c-41c6-992c-d83810677fd7/changesets"

##### Database Code #####
flaskApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
flaskApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'
flaskApp.config['SECRET_KEY'] = "secret key"
db = SQLAlchemy(flaskApp)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_dir = db.Column(db.String(200))  #store raw data
    email_dir = db.Column(db.String(200))
    internship_period = db.Column(db.String(120))

    def __init__(self, resume_dir, email_dir, internship_period, methods=['GET','POST']):
        self.resume_dir = resume_dir
        self.email_dir = email_dir
        self.internship_period = internship_period


class Student(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    preference = db.Column(db.String(200), nullable=False)
    company_id = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<ID %r>' % self.id

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200), nullable=False)
    contact = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

class StudentForm(FlaskForm):
    id = StringField(validators=[DataRequired()])
    name = StringField(validators=[DataRequired()])
    preference = StringField(validators=[DataRequired()])
    status = SelectField('Status', choices = [('unassigned', 'Unassigned'),('pending_confirmation', 'Pending confirmation'),('confirmed','Confirmed')], validators=[DataRequired()])
    submit = SubmitField("Submit")

##### Company Form (Unused) #####
##class CompanyForm(FlaskForm):
##    name = StringField(validators=[DataRequired()])
##    role = StringField(validators=[DataRequired()])
##    contact = StringField(validators=[DataRequired()])
##    email = StringField(validators=[DataRequired()])

with flaskApp.app_context():
    db.create_all()
########################################

@flaskApp.route('/')



@flaskApp.route('/Main')
def main():
    return render_template('main.html')

##### Data Upload Code #####
@flaskApp.route('/Upload_Data')
def upload_data():
    return render_template('upload_data.html')

# Upload folder
UPLOAD_FOLDER = 'static/files'
flaskApp.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

# File upload for student data
@flaskApp.route('/student_uploader', methods = ['GET', 'POST'])
def upload_student_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            student_col = ['id', 'name', 'preference']
            studentData = pd.read_excel(uploaded_file, names=student_col, header=None)
            for i, row in studentData.iterrows():
                id = str(row[0])
                name = str(row[1])
                preference = str(row[2])
                status = 'unassigned'
                student = Student(id=id,
                                name=name,
                                preference=preference,
                                status=status)
                db.session.add(student)
                db.session.commit()
        return redirect('Upload_Data')

# File upload for company data
@flaskApp.route('/company_uploader', methods = ['GET', 'POST'])
def upload_company_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            company_col = ['name', 'role', 'contact', 'email']
            companyData = pd.read_excel(uploaded_file, names=company_col, header=None)
            for i, row in companyData.iterrows():
                name = str(row[0])
                role = str(row[1])
                contact = str(row[2])
                email = 'unassigned'
                company = Student(name=name,
                                role=role,
                                contact=contact,
                                email=email)
                db.session.add(company)
                db.session.commit()
        return redirect('Upload_Data')
########################################

@flaskApp.route('/Match_Student', methods=['GET', 'POST'])
def match_student():
    form = StudentForm()
    student_list = Student.query.order_by(Student.id)
    company_list = Company.query.order_by(Company.name)
    
    if request.method == "POST":
        # Get data from row "form"
        id = request.form.get("id")
        status = request.form.get("status")
        companyInfo = request.form.get("companyInfo")

        if companyInfo == "None":
            companyInfo = None
        
        student_to_update = Student.query.filter_by(id=id).first()
        student_to_update.status = status
        student_to_update.company_id = companyInfo

        db.session.commit()

    return render_template('match_student.html',
        form=form,
        student_list=student_list,
        company_list=company_list)
        
    

@flaskApp.route('/Prepare_Email')
def prepare_email():
    return render_template('prepare_email.html')



#data validation for resume and email
ALLOWED_EXTENSIONS = set(['csv', 'pdf'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@flaskApp.route('/Settings', methods=['GET','POST'])
def settings():
    if request.method == 'POST':
        resume_dir = request.files.get('resume_dir') 
        email_dir = request.files.get('email_dir')
        internship_period = request.form['Internship_Period']

        #automation
        payload = {"internship_period": internship_period}

        response = requests.post(webhook_url, json=payload)

        print(response.status_code)

        #checks the file extension before reading the file

        if not resume_dir or not allowed_file(resume_dir.filename):
            return render_template("settings.html", error_message="Invalid resume file type. Only CSV and PDF files are allowed.")
        if not email_dir or not allowed_file(email_dir.filename):
            return render_template("settings.html", error_message="Invalid email file type. Only CSV and PDF files are allowed.")
        
        # Store the path of the file in the database instead of the actual file
        file = File(resume_dir=resume_dir.filename, email_dir=email_dir.filename, internship_period=internship_period)
        db.session.add(file)
        db.session.commit()
    return render_template('settings.html')


    

if __name__ == "__main__":
    flaskApp.run(debug=True, host='0.0.0.0', port=5221)