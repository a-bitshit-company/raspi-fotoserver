from flask import Flask, jsonify, render_template
from sqlalchemy import Column, Integer, Text, DateTime, Sequence
from sqlalchemy import create_engine,  or_
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func
import base64

Base = declarative_base()
metadata = Base.metadata
engine = create_engine('sqlite:///sqlite/fotoserver.sqlite3')
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
Base.query = db_session.query_property() #Dadurch hat jedes Base - Objekt (also auch ein Millionaire) ein Attribut query für Abfragen
app = Flask(__name__)

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
                'img_base64' : self.img_base64,
                'date' : self.date}

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
    db_session.commit() #

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    app.run()
