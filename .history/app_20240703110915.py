from flask import Flask, render_template,redirect,request,flash,url_for,Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from datetime import datetime
import csv
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
        # Save the contact message to the database
        contact_message = ContactMessage(name=name, email=email, mobile=mobile, message=message)
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


#this is csv downloader

@app.route('/download_contact_messages')
def download_contact_messages():
    contact_messages = ContactMessage.query.all()
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(['ID', 'Name', 'Email','Mobile', 'Message'])  # Adjust headers based on your model fields
    for message in contact_messages:
        writer.writerow([message.id, message.name, message.email, message.mobile, message.message])  # Adjust based on your model fields
        buffer.seek(0)
        response = Response(buffer, mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=contact_messages.csv'
    
    return response


@app.route('/delete_contact_message/<int:id>', methods=['POST'])
def delete_contact_message(id):
    contact_message = ContactMessage.query.get_or_404(id)
    db.session.delete(contact_message)
    db.session.commit()
    flash('Contact message deleted successfully!', 'success')
    return redirect(url_for('dashboard'))


# this is pdf converter

# @app.route('/download_contact_messages')
# def download_contact_messages():
#     contact_messages = ContactMessage.query.all()

#     buffer = io.BytesIO()
#     p = canvas.Canvas(buffer, pagesize=letter)
#     width, height = letter

#     # Title
#     p.setFont("Helvetica-Bold", 16)
#     p.drawString(100, height - 40, "Contact Messages")

#     p.setFont("Helvetica-Bold", 12)
#     p.drawString(50, height - 70, "ID")
#     p.drawString(100, height - 70, "Name")
#     p.drawString(250, height - 70, "Email")
#     p.drawString(400, height - 70, "Mobile")
#     p.drawString(500, height - 70, "Message")

#     p.setFont("Helvetica", 10)
#     y = height - 90
#     for message in contact_messages:
#         p.drawString(50, y, str(message.id))
#         p.drawString(100, y, message.name)
#         p.drawString(250, y, message.email)
#         p.drawString(400, y, message.mobile)
#         p.drawString(500, y, message.message)
#         y -= 20

#     p.showPage()
#     p.save()
    
#     buffer.seek(0)
#     response = Response(buffer, mimetype='application/pdf')
#     response.headers['Content-Disposition'] = 'attachment; filename=contact_messages.pdf'
    
#     return response

if __name__ == '__main__':
    app.run(debug=True)
