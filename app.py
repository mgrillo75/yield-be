import os
from flask import Flask, jsonify, request, make_response
from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin

port = int(os.environ.get("PORT", 5000))

app = Flask(__name__)

cors = CORS(app)

#app.config['CORS_HEADERS'] = 'application/json'
#app.config['CORS_RESOURCES'] = {r"/get*": {"origins": "*"}}


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Mos0451234561477@localhost/mgrillo_defiart_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text())
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, title, body, deposit):
        self.title = title
        self.body = body
        self.deposit = deposit


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'date', 'deposit')


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


@app.route('/', methods=["GET"])
@cross_origin()
def index():
    return("hello NFT YIELDS")


@app.route('/get', methods=['GET', 'OPTIONS'])
@cross_origin()
def get_articles():
    all_articles = Articles.query.all()
    results = articles_schema.jsonify(all_articles)
    #results.headers.add("Access-Control-Allow-Origin", "*")
    return (results)


@app.route('/get/<id>/', methods=['GET'])
def post_details(id):
    article = Articles.query.get(id)
    return article_schema.jsonify(article)


@app.route('/add', methods=['POST'])
def add_article():
    title = request.json['title']
    body = request.json['body']
    deposit = request.json['deposit']

    articles = Articles(title, body, deposit)
    db.session.add(articles)
    db.session.commit()
    return article_schema.jsonify(articles)


@app.route('/update/<id>/', methods=['PUT'])
def get_article(id):
    article = Articles.query.get(id)

    title = request.json['title']
    body = request.json['body']
    deposit = request.json['deposit']

    article.title = title
    article.body = body
    article.deposit = deposit

    db.session.commit()
    return article_schema.jsonify(article)


if __name__ == "__main__":
    # app.run(debug=True)
    # app.run(host='0.0.0.0',port=5000,debug=True)
    app.run(host='0.0.0.0', port=port, debug=True)
