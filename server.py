from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
from pytesseract import image_to_string
from uuid import uuid4
import os
import re


app = Flask(__name__)
CORS(app)
# root
@app.route("/")
def index():
    """
    this is a root dir of my server
    :return: str
    """
    return "This is root!!!!"

# GET
@app.route('/users/<user>')
def hello_user(user):
    """
    this serves as a demo purpose
    :param user:
    :return: str
    """
    string1 = "user"
    return "Hello %s!" % user

# POST
@app.route('/api/post_some_data', methods=['POST'])
def upload_file():
  if request.method == 'POST':
    f = request.files['file']
    img1=Image.open(f)
    # folder_name = str(uuid4())
    # os.makedirs("FlaskFiles")
    # with open('./{fn}/output.txt'.format(fn=folder_name),'wb') as f:
    #   f.write(image_to_string(img1))
    ocrOutput = image_to_string(img1)
    colonSeperatedValues = re.findall(".*:.*", ocrOutput)
    return "{}\n{}".format(colonSeperatedValues, ocrOutput)
    # f.save(secure_filename(f.filename))
# def get_text_prediction():
#     """
#     predicts requested text whether it is ham or spam
#     :return: json
#     """
#     # json = request.get_json()
#     # print(json)
#     # if len(json['text']) == 0:
#     #     return jsonify({'error': 'invalid input'})

#     return jsonify({'you sent this': json['text']})
    
# running web app in local machine
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)