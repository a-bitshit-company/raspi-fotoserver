import base64

import datetime as datetime
import requests


PATH = '/home/matteo/Pictures/maimais/nazishit.png'

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


if __name__ == '__main__':

    data = {'name' : 'lappen', 'image': encode_base64(PATH), 'date' : str(datetime.datetime(2020,5,17))} #date aus exif auslesen?
    response = requests.put('http://localhost:5000/image/0', json=data)
    print(response)


    response = requests.get('http://localhost:5000/image/1y')
    res_json = response.json()
    print(res_json)
    #decode_Base64('/tmp/test', res_json['data'])