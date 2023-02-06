from flask import Flask, request, render_template, url_for, redirect

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired



flaskApp = Flask(__name__)

##### Database Code #####
flaskApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
flaskApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'
flaskApp.config['SECRET_KEY'] = "secret key"
db = SQLAlchemy(flaskApp)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_dir = db.Column(db.LargeBinary)  #store raw data
    email_dir = db.Column(db.LargeBinary)
    internship_period = db.Column(db.String(120))

    def __init__(self, resume_dir, email_dir, internship_period, methods=['GET','POST']):
        self.resume_dir = resume_dir
        self.email_dir = email_dir
        self.internship_period = internship_period


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
##### Database Code #####

@flaskApp.route('/')

@flaskApp.route('/Main')
def main():
    return render_template('main.html')

@flaskApp.route('/Upload_Data')
def upload_data():
    return render_template('upload_data.html')

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

@flaskApp.route('/Settings', methods=['GET','POST'])
def settings():
    if request.method == 'POST':
        resume_dir = request.files['resume_dir'].read() 
        email_dir = request.files['email_dir'].read()
        internship_period = request.form['Internship_Period']

        # Store the values in the database
        file = File(resume_dir, email_dir, internship_period)
        db.session.add(file)
        db.session.commit()
    return render_template('settings.html')


    

if __name__ == "__main__":
    flaskApp.run(debug=True, host='0.0.0.0', port=5221)