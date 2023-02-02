from flask import Flask, request, render_template

appFlask = Flask(__name__)
@appFlask.route('/Main')

def main_page():
    return render_template('Main.html')

if __name__ == "__main__":
    appFlask.run(host='0.0.0.0', port=5221)