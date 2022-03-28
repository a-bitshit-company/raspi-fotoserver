from flask import Flask, jsonify, render_template
from flask_restful import Resource
from sqlalchemy import Column, Integer, Text, DateTime, Sequence
from sqlalchemy import create_engine,  or_
from sqlalchemy.event import api
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func
import base64
import os
from flask import Flask, request,jsonify, send_from_directory
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

import werkzeug.utils

FOLDER = '/home/user/fotoserver'

Base = declarative_base()
metadata = Base.metadata
engine = create_engine('sqlite:///sqlite/fotoserver.sqlite3')
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
Base.query = db_session.query_property() #Dadurch hat jedes Base - Objekt (also auch ein Millionaire) ein Attribut query für Abfragen
app = Flask(__name__)
api = Api(app)

def encode_base64(file):
    binary_file_data = file.read()
    base64_encoded_data = base64.b64encode(binary_file_data)
    return base64_encoded_data.decode('utf-8')

class Image(Base):
    __tablename__ = 'images'  # Abbildung auf diese Tabelle

    id = Column(Integer, Sequence('seq_reg_id', start=1, increment=1),primary_key=True)
    name = Column(Text)
    img_base64 = Column(Text)
    date = Column(DateTime)

    def serialize(self):
        return {'id' : self.id,
                'name':  self.name,
                'date': str(self.date),
                'img_base64' : self.img_base64
                }

class RImage(Resource):
    def get(self, id):
        img = Image.query.get(id)
        return img.serialize()

    def put(self, id):
        d = request.get_json(force=True)
        temp = Image(name=d['name'], img_base64=d['image'], date=d['date'])
        db_session.add(temp)
        db_session.flush()
        return temp.serialize()

    def delete(self, id):
        temp = Image.query.get(id)
        if temp is None:
            return jsonify({'message': 'object with id %d does not exist' % id})
        db_session.delete(temp)
        db_session.flush()
        return jsonify({'message': '%d deleted' % id})

#api.add_resource(RImage, '/image/<int:id>')
api.add_resource(RImage, '/image')

@app.route('/')
def index():
    str = '<!DOCTYPE html>\n<html>\n<head>\n<title>Fotoserver</title>\n</head>\n<body>'
    str += '<h1> Images </h1>\n'
    str +='<div id="images">\n'

    for img in db_session.query(Image):
        str += '<img src="data:image/png;base64,'
        str += img.img_base64
        str += '" />\n'

    str += '</div>'
    str += '</body>\n</html>'

    return str

@app.teardown_appcontext
def shutdown_session(exception=None):
    print("Shutdown Session")
    db_session.remove()

def init_db(): # this function is not called from script, execute from python shell to reset sqlite file
    img = Image(id=0, name="htl_logo.png", img_base64=encode_base64(open("static/htl_logo.png", 'rb')), date=func.now())
    db_session.begin()
    db_session.add(img)
    db_session.commit()

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    app.run()
