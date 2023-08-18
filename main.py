from flask import Flask, request,  jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

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
    print("hola mundo")
    date = request.json.get('date')
    new_feedback = Clickdev(date=date)
    db.session.add(new_feedback)
    db.session.commit()
    return jsonify({'id': new_feedback.id, 'date': new_feedback.date }), 201






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
