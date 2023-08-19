from flask import Flask, request,  jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from datetime import datetime
import pytz
from user_agents import parse 
from ipstack import GeoLookup

app = Flask(__name__)
CORS(app)





#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
'''
# Base de datos simulada (reemplaza con una base de datos real)
feedbacks_list = []
'''

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:pDDp4ycIxTN9iHFfToWW@containers-us-west-198.railway.app:5459/railway')
db = SQLAlchemy(app)


#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

class Downloadcv(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)

class Clickdev(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(100), nullable=False)
    referer_url  = db.Column(db.String(1000), nullable=False)
    data_inf  = db.Column(db.String(1000), nullable=False)


#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/feedbacks', methods=['GET'])
def get_feedbacks():
    feedbacks = Feedback.query.all()
    feedbacks_list = [{'id': f.id, 'name': f.name, 'description': f.description} for f in feedbacks]
    return jsonify(feedbacks_list)


@app.route('/api/feedbacks', methods=['POST'])
def add_feedbacks():
    name = request.json.get('name')
    description = request.json.get('description')
    new_feedback = Feedback(name=name, description=description)
    db.session.add(new_feedback)
    db.session.commit()
    return jsonify({'id': new_feedback.id, 'name': new_feedback.name, 'description': new_feedback.description}), 201





@app.route('/api/downloadcv', methods=['POST'])
def download_cv():
    date = request.json.get('date')
    new_feedback = Downloadcv(date=date)
    db.session.add(new_feedback)
    db.session.commit()
    return jsonify({'id': new_feedback.id, 'date': new_feedback.date }), 201


@app.route('/api/clickdev', methods=['POST'])
def click_dev():
    '''
    date = request.json.get('date')
    '''
    bogota_tz = pytz.timezone('America/Bogota')
    bogota_time = datetime.now(bogota_tz)
    visitor_ip = request.remote_addr
    referer_url = request.headers.get('Referer')


    user_agent = request.headers.get('User-Agent')
    browser, os = get_browser_and_os(user_agent)
    geolocation = get_geolocation(visitor_ip)
    print(browser, os)
    print(geolocation)

    data_inf = "[{},{}]  [{}]".format(browser, os, geolocation)
    new_information = Clickdev(date=bogota_time, ip_address=visitor_ip, referer_url=referer_url, data_inf=data_inf)
    db.session.add(new_information)
    db.session.commit()

    return jsonify({
        'id': new_information.id,
        'date': new_information.date,
        'ip_address': new_information.ip_address,
        'referer_url': new_information.referer_url,
        'data_inf':new_information.data_inf
    }), 201









@app.route('/api/feedbacks/<int:feedback_id>', methods=['GET'])
def get_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    return jsonify({'id': feedback.id, 'name': feedback.name, 'description': feedback.description})

@app.route('/api/feedbacks/<int:feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    return '', 204



#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))



def get_browser_and_os(user_agent):
    user_agent_data = parse(user_agent)
    browser = user_agent_data.browser.family
    os = user_agent_data.os.family
    return browser, os




geo_lookup = GeoLookup("dae96249832155cb240097ae081ae102")

def get_geolocation(ip_address):  

    location = geo_lookup.get_location(ip_address)

    '''
    {'ip': '127.0.0.1', 'type': 'ipv4', 'continent_code': None, 'continent_name': None, 'country_code': None, 'country_name': None, 'region_code': None, 'region_name': None, 'city': None, 'zip': None, 'latitude': 0.0, 'longitude': 0.0, 'location': {'geoname_id': None, 'capital': None, 'languages': None, 'country_flag': None, 'country_flag_emoji': None, 'country_flag_emoji_unicode': None, 'calling_code': None, 'is_eu': None}} <class 'dict'>
    '''

    city= location["city"]
    region_name= location["region_name"]
    country_name=location["country_name"]
    continent_name= location["continent_name"]
    latitude = location["latitude"]
    longitude = location["longitude"]
    
    print("Ciudad:", city)
    print("Región:", region_name)
    print("País:", country_name)
    print("Continente:", continent_name)
    print("Latitud:", latitude)
    print("Longitude:", longitude)

    text_data = "Ciudad:{};Región:{};País:{};Continente:{};Latitud:{};longitude:{};".format(city, region_name, country_name, continent_name, latitude, longitude)
    return text_data
