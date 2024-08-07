from flask import Flask, render_template,redirect,request,flash,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from datetime import datetime


# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Add a secret key for session management

# Configure the SQLAlchemy part of the application instance
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Define the ContactMessage model
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return '<ContactMessage {}>'.format(self.name)

# Create the database and the db tables
# @app.before_first_request
# def create_tables():
#     db.create_all()

# Define the routes
@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        message = request.form['message']
        created=request.form['created']
        # Save the contact message to the database
        contact_message = ContactMessage(name=name, email=email, mobile=mobile, message=message,created=created)
        db.session.add(contact_message)
        db.session.commit()

        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/certified professional')
def certified_professional():
    return render_template('Certified Professional Coder.html')

@app.route('/CPC Exam')
def CPC_Exam():
    return render_template('CPC Exam New Guidelines.html')

@app.route('/Ed Facility')
def Ed_Facility():
    return render_template('ED FACILITY.html')

@app.route('/Ed Professional')
def Ed_Professional():
    return render_template('ED Professionals.html')

@app.route('/Evaluation and Management')
def Evaluation():
    return render_template('Evaluation and Management Coding.html')

@app.route('/Interventional Radiology')
def Interventional():
    return render_template('Interventional Radiology department coding (IVR).html')

@app.route('/dashboard')
def dashboard():
    contact_messages = ContactMessage.query.all()
    return render_template('dashboard.html', contact_messages=contact_messages)

if __name__ == '__main__':
    app.run(debug=True)
