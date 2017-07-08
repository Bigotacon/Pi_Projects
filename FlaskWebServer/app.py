from flask import Flask, render_template, request, redirect, jsonify, url_for, flash

# Database items
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Measurents, Message

engine = create_engine('sqlite:///flaskwebserver.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather')
def weather():
    if True:
        from sense_hat import SenseHat
        sense = SenseHat()
        humidity = sense.get_humidity()
        pressure = sense.get_pressure()
        temp = sense.get_temperature()
        return render_template('weather.html',
                               humidity=humidity,
                               pressure=pressure, 
                               temp=temp)

@app.route('/writeSensehat', methods=['GET', 'POST'])
def writeSensehat():
    if request.method == 'GET': 
        messages = session.query(Message).all()
        for message in messages:
            print (message.message)

        return render_template('writeSensehat.html', messages=messages)
    if request.method == 'POST':
        textBoxPath = request.form['projectFilepath']
        radioButtonPath = request.form['radioButtonPath']

        if True:
            from sense_hat import SenseHat
            sense = SenseHat()
            formMessage = textBoxPath + " " + radioButtonPath
            sense.show_message(formMessage)
            myMessage = Message(message=formMessage)
            session.add(myMessage)
            session.commit()

            return "<a href='/writeSensehat'>Write another message </a> &nbsp <a href='/'>Home</a>"
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
