from flask import Flask, request, render_template, url_for, send_file

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

from email.message import EmailMessage

flaskApp = Flask(__name__)

##### Database Code #####
flaskApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
flaskApp.config['SECRET_KEY'] = "secret key"
db = SQLAlchemy(flaskApp)

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

class CompanyForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    role = StringField(validators=[DataRequired()])
    contact = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])

class EmailForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    preference = StringField(validators=[DataRequired()])
    company_name = StringField(validators=[DataRequired()])
    company_role = StringField(validators=[DataRequired()])
    company_email = StringField(validators=[DataRequired()])
    submit = SubmitField("Submit")

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

@flaskApp.route('/Prepare_Email', methods=['GET', 'POST'])
def prepare_email():
    form = EmailForm()
    student_list = Student.query.filter(Student.company_id.isnot(None)).order_by(Student.id)
    company_list = Company.query.order_by(Company.name)

    if request.method == "POST":
        # Get data from row "form"
        name = request.form.get("name")
        preference = request.form.get("preference")
        company_name = request.form.get("company_name")
        company_role = request.form.get("company_role")
        company_email = request.form.get("company_email")

        email_msg = EmailMessage()
        email_msg.set_content("To HR Representative from " + company_name + ": \n\n" + name + " is interested in taking an internship at " + company_name + "for the role of " + company_role)
        email_msg['Subject'] = "Student Internship"
        email_msg['From'] = "sender@example.com"
        email_msg['To'] = company_email
        with open("email.msg", "wb") as f:
            f.write(email_msg.as_bytes())
        return send_file("email.msg", as_attachment=True)

    return render_template('prepare_email.html',
        form=form,
        student_list=student_list,
        company_list=company_list)

@flaskApp.route('/Settings')
def settings():
    return render_template('settings.html')

if __name__ == "__main__":
    flaskApp.run(debug=True, host='0.0.0.0', port=5221)