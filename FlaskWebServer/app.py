#Web server items
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
# Database items
from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Measurements, Message

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
        weatherUrlJson = request.url + "/JSON"
        measurements = session.query(Measurements).order_by(asc(Measurements.created_date)).all()
        data = jsonify(measurements=[m.serialize for m in measurements])
        from sense_hat import SenseHat
        sense = SenseHat()
        humidity = sense.get_humidity()
        pressure = sense.get_pressure()
        temp = sense.get_temperature()
        return render_template('weather.html',
                               data = data,
                               humidity=humidity,
                               pressure=pressure,
                               temp=temp)

@app.route('/weather/JSON')
def weatherJSON():
    measurements = session.query(Measurements).order_by(asc(Measurements.created_date)).all()
    return jsonify(measurements=[m.serialize for m in measurements])

def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    # value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

@app.route('/writeSensehat', methods=['GET', 'POST'])
def writeSensehat():
    if request.method == 'GET':
        messages = session.query(Message).order_by(desc(Message.created_date)).limit(5).all()
        return render_template('writeSensehat.html', messages=messages)

    if request.method == 'POST':
        optionsValue = ""
        if 'options' in request.form:
            optionsValue = request.form['options']
        textValue = request.form['textValue']
        if True:
            from sense_hat import SenseHat
            sense = SenseHat()
            formMessage = textValue + " " + optionsValue
            textColour = hex_to_rgb(request.form['textColour'])
            backColour = hex_to_rgb(request.form['backColour'])
            sense.show_message(formMessage, text_colour=textColour, back_colour=backColour)
            sense.clear()
            myMessage = Message(message=formMessage)
            session.add(myMessage)
            session.commit()
            return "<a href='/writeSensehat'>Write another message </a> &nbsp <a href='/'>Home</a>"
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
 
