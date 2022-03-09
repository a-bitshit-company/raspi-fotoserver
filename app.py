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

def encode_base64(fName):
    with open(fName, 'rb') as file:
        binary_file_data = file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        return base64_encoded_data.decode('utf-8')

def decode_Base64(fName, data):
    data_base64 = data.encode('utf-8')
    with open(fName, 'wb') as file:
        decoded_data = base64.decodebytes(data_base64)
        file.write(decoded_data)

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
    str = '<h1> test </h1>\n'
    str += '<img src="data:image/png;base64,'
    str += Image.query.get(0).img_base64
    str += '" />'
    return str

@app.teardown_appcontext
def shutdown_session(exception=None):
    print("Shutdown Session")
    db_session.remove()

def init_db(): # this function is not called from script, execute from python shell to reset sqlite file
    img = Image(id=0, name="htl_logo.png", img_base64=encode_base64("static/htl_logo.png"), date=func.now())
    db_session.begin()
    db_session.add(img)
    db_session.commit() #

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    app.run()
