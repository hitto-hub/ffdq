from datetime import datetime
from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy
from zoneinfo import ZoneInfo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# データベースのテーブルを作成
class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    timestamp = db.Column(db.String, nullable=False)
    question = db.Column(db.String, nullable=False)
    def __repr__(self):
        return '<Data %r>' % self.question

with app.app_context():
    db.create_all()

#delete all data
@app.route('/api', methods=['DELETE'])
def delete_all():
    try:
        Data.query.delete()
        db.session.commit()
        return 'delete all data\n'
    except:
        return 'delete all data failed\n'

@app.route('/api', methods=['GET'])
def get_question():
    try:
        quetion = Data.query.all()
        return {
            "status": "success",
            "num_results": f"{len(question)}",
            "data": [
                {
                    "id": v.id,
                    "timestamp": v.timestamp,
                    "question": v.question
                }
                for v in question
            ]
        }
    except:
        return {
            "status": "failed"
        }
    
    
@app.route('/api', methods=['POST'])
def post_question():
    try:
        data = request.json["question"] #POSTメソッド のデータを取得
        timestamp = datetime.now(ZoneInfo("Asia/Tokyo"))
        timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        cre = Data(question = data, timestamp = timestamp_str)
        db.session.add(cre)
        db.session.commit()
        return {
            "status": "success",
            "data": {
                "id": cre.id,
                "timestamp": cre.timestamp,
                "question": cre.question
            }
        }
    except:
        return {
            "status": "failed"
        }

@app.route('/api/count', methods=['GET'])
def get_count():
    try:
        question = Data.query.all()
        return {
            "status": "success",
            "num_results": f"{len(question)}",
        }
    except:
        return {
            "status": "failed"
        }

if __name__ == '__main__':
    app.run()
