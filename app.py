from flask import Flask, request, render_template, url_for

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

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

class StudentForm(FlaskForm):
    id = StringField(validators=[DataRequired()])
    name = StringField(validators=[DataRequired()])
    preference = StringField(validators=[DataRequired()])
    status = StringField(validators=[DataRequired()])

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
    return render_template('match_student.html',
        student_list=student_list)

@flaskApp.route('/Prepare_Email')
def prepare_email():
    return render_template('prepare_email.html')

@flaskApp.route('/Settings')
def settings():
    return render_template('settings.html')

if __name__ == "__main__":
    flaskApp.run(debug=True, host='0.0.0.0', port=5221)