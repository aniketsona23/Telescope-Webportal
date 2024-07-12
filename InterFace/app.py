from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from datetime import datetime, timedelta, timezone


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

# Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Define the form
class DataForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    exposure_time = StringField('Exposure Time', validators=[DataRequired()])
    obj = StringField('Object', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    exposure_time = db.Column(db.String(80), nullable=False)
    obj = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    request_date = db.Column(db.Date, nullable=False, default=datetime.now().date())
    request_time = db.Column(db.Time, nullable=False, default=datetime.now().time())

    def __repr__(self):
        return f'<Data {self.name} - {self.obj}>'

def arrange_data(data):
    result = {}
    for item in data:
        category = item.get('Category')
        obj = item.get('Object')
        image_link = item.get('Image link')

        if category not in result:
            result[category] = {}
        
        result[category][obj] = image_link
    
    return result

@app.route('/')
def home():
    url = 'https://opensheet.elk.sh/15x9oFZtisE5Bl3s3pc-pJvWzsIKkjzQnFPtz9gMTra4/Sheet1'
    response = requests.get(url)
    data = response.json()
    arranged_data = arrange_data(data)
    return render_template('index.html', arranged_data=arranged_data)

@app.route('/send/', methods=['POST'])
def send():
    name = request.form.get('name')
    exposure_time = request.form.get('exposure')
    obj = request.form.get('object')
    email = request.form.get('email')
    ist_offset = timedelta(hours=5, minutes=30)
    ist_timezone = timezone(ist_offset)
    current_datetime = datetime.now(ist_timezone)

    new_data = Data(name=name, exposure_time=exposure_time, obj=obj, email=email, request_date=current_datetime.date(), request_time=current_datetime.time())
    db.session.add(new_data)
    db.session.commit()

    return jsonify({'message': 'Data added successfully!'})



@app.route('/team/')
def team():
    return render_template('team.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

