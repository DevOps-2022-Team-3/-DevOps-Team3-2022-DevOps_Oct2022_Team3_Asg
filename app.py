import os
from os.path import join, dirname, realpath
from flask import Flask, request, render_template, url_for, flash, redirect

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

import pandas as pd

flaskApp = Flask(__name__)

##### Database Code #####
flaskApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
flaskApp.config['SECRET_KEY'] = "secret key"
db = SQLAlchemy(flaskApp)

class Student(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    preference = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<ID %r>' % self.id

class Company(db.Model):
    name = db.Column(db.String(200), primary_key=True)
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

class CompanyForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    role = StringField(validators=[DataRequired()])
    contact = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])

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
    print("test12")
    print(request.form.get("status"))
    print("test134")
    if form.validate_on_submit():
        student = Student.query.filter_by(id=form.id.data).first()
        student.status = Student(status=form.status.data)
        db.session.commit()
    return render_template('match_student.html',
        form=form,
        student_list=student_list,
        company_list=company_list)

@flaskApp.route('/Prepare_Email')
def prepare_email():
    return render_template('prepare_email.html')

@flaskApp.route('/Settings')
def settings():
    return render_template('settings.html')

if __name__ == "__main__":
    flaskApp.run(debug=True, host='0.0.0.0', port=5221)