from flask import Flask, request, render_template, url_for

flaskApp = Flask(__name__)

@flaskApp.route('/')

@flaskApp.route('/Main')
def main():
    return render_template('main.html')

@flaskApp.route('/Upload_Data')
def upload_data():
    return render_template('upload_data.html')

@flaskApp.route('/Match_Student')
def match_student():
    return render_template('match_student.html')

@flaskApp.route('/Prepare_Email')
def prepare_email():
    return render_template('prepare_email.html')

@flaskApp.route('/Settings')
def settings():
    return render_template('settings.html')


if __name__ == "__main__":
    flaskApp.run(debug=True, host='0.0.0.0', port=5221)