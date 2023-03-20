import re
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import jsonify
import requests
import pickle
import numpy as np
import sklearn
import doc_detail_extract as dde


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/pravin'
db = SQLAlchemy(app)
model = pickle.load(open('C:\\Users\\imswa\\OneDrive\\Desktop\\MentalHealthCompanion - Copy\\companion\\random_forest_regression_model.pkl', 'rb'))

class Contact(db.Model):
    '''sr, name, phone_num, email, msg, dt'''
    sr = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    dt = db.Column(db.String(12), nullable=False)



@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')



@app.route('/index.html', methods=['GET'])
def index():
    return render_template('index.html')



@app.route('/login.html')
def login():
    return render_template('login.html')



@app.route('/contact.html', methods = ['GET', 'POST'])
def contact():
    if (request.method=='POST'):
        '''add entry to the database'''
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        message = request.form.get('message')
        entry = Contact(name=name, phone_num=phone, email=email, msg=message)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')



@app.route('/signup.html')
def signup():
    return render_template('signup.html')


@app.route('/taketest.html',methods=['GET'])
def taketest():
    return render_template('taketest.html')



# standard_to = StandardScaler()
@app.route('/predict', methods=['POST'])


def predict():
    if request.method == 'POST':
        wind_down = float(request.form['wind_down'])
        dryness_mouth = int(request.form['dryness_mouth'])
        no_positive_feeling = int(request.form['no_positive_feeling'])
        breathing_difficulty = int(request.form['breathing_difficulty'])
        difficult_to_work = int(request.form['difficult_to_work'])
        over_react = int(request.form['over_react'])
        trembling = int(request.form['trembling'])
        use_nervous_energy = int(request.form['use_nervous_energy'])
        panic = int(request.form['panic'])
        nothing_look_forward = int(request.form['nothing_look_forward'])
        agitated = int(request.form['agitated'])
        difficult_relax = int(request.form['difficult_relax'])
        blue = int(request.form['blue'])
        intolerant = int(request.form['intolerant'])
        close_panic = int(request.form['close_panic'])
        unable_enthusiatic = int(request.form['unable_enthusiatic'])
        not_worth_person = int(request.form['not_worth_person'])
        touchy = int(request.form['touchy'])
        action_of_heart_abs = int(request.form['action_of_heart_abs'])
        scared_no_reason = int(request.form['scared_no_reason'])
        life_meaningless = int(request.form['life_meaningless'])

        prediction=model.predict([[wind_down, dryness_mouth, no_positive_feeling,breathing_difficulty,
        difficult_to_work, over_react, trembling,use_nervous_energy, panic, nothing_look_forward,
        agitated,difficult_relax, blue, intolerant, close_panic,unable_enthusiatic, not_worth_person,
        touchy,action_of_heart_abs, scared_no_reason, life_meaningless]])
        output=round(prediction[0])
        if output<=0:
            return render_template('verylow.html')#,prediction_text="you are Normal")
        else:
            return render_template('moderate.html',data=dde.doc_data_pd)#,prediction_text="you are Abnormal".format(output))
    else:
        return render_template('index.html')




if __name__ == "__main__":
    app.run(debug=True)
