from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

data_store2 = []

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class DataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/api/message', methods=['GET'])
def get_message():
    return jsonify({"message": "Backend is up"})

@app.route('/api/data', methods=['POST'])
def post_data():
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({"error": "No data provided"}), 400
    data_store.append(data)

    new_data = DataModel(content=data['content'])
    db.session.add(new_data)
    db.session.commit()

    all_data = DataModel.query.all()
    data_store = [{"id": d.id, "content": d.content} for d in all_data]

    return jsonify({"status": "Data added", "data": data_store, "data2": data_store2}), 201

if __name__ == '__main__':
    app.run(debug=True)
