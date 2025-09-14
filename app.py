# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from bson import ObjectId
import certifi

app = Flask(__name__)
app.config["SECRET_KEY"] = '\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'
app.config["MONGO_URI"] = "mongodb+srv://pritamtung03_db_user:WLIFVuRwEev7APoP@cluster0.4ysopge.mongodb.net/Study_game"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


# Replace with your actual connection string
uri = "mongodb+srv://pritamtung03_db_user:WLIFVuRwEev7APoP@cluster0.4ysopge.mongodb.net/Study_game"

mongo = MongoClient(
    app.config["MONGO_URI"],
    tls=True,  # Explicitly enable TLS
    tlsCAFile=certifi.where(),  # Use the CA bundle from the 'certifi' package
    serverSelectionTimeoutMS=20000  # Set a timeout for server selection
)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    payments = list(mongo.db.payments.find().sort('date', -1))
    return render_template('index.html', payments=payments)

@app.route('/submit', methods=['POST'])
def submit_payment():
    name = request.form.get('name')
    email = request.form.get('email')
    payment_type = request.form.get('paymentType')
    date_str = request.form.get('date')
    
    # Convert date string to datetime object
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except:
        flash('Invalid date format')
        return redirect(url_for('index'))
    
    # Handle file upload
    screenshot = None
    if payment_type == 'online' and 'screenshot' in request.files:
        file = request.files['screenshot']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Create unique filename
            unique_filename = f"{datetime.now().timestamp()}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            screenshot = unique_filename
    
    # Insert into database
    payment_data = {
        'name': name,
        'email': email,
        'payment_type': payment_type,
        'date': date,
        'screenshot': screenshot,
        'submitted_at': datetime.now()
    }
    
    mongo.db.payments.insert_one(payment_data)
    flash('Payment submitted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=False)