from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
from pytesseract import image_to_string
from uuid import uuid4
import os
import re
from commonregex import CommonRegex


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
    # return f.filename
    img1=Image.open(f)
    # folder_name = str(uuid4())
    # os.makedirs("FlaskFiles")
    # with open('./{fn}/output.txt'.format(fn=folder_name),'wb') as f:
    #   f.write(image_to_string(img1))
    ocrOutput = image_to_string(img1).lower()
    # monthsShort= 'jan|feb|mar|apr|jun|jul|aug|sep|nov|dec'
    # monthsLong= 'january|february|march|april|june|july|august|september|november|december'
    # monthInteger =  '[0-9]{2}'
    # months= '(' + monthsShort + '|' + monthsLong + '|' + monthInteger + ')'
    # separators = '[/-]'
    # days = '[0-9]{2}'
    # years = '[0-9]{4}'
    dateRegex = "\d{2,4}[/.-](?:jan|feb|mar|apr|jun|jul|aug|sep|nov|dec|january|february|march|april|june|july|august|september|november|december|\d{2})[/.-]\d{2,4}"
    timeRegex = "\d{1,2}[:]\d{1,2}[:]{0,1}\d{0,2}\s{0,1}[am|pm]{0,2}"
    
    totalAmountRegex = ".*total.*[0-9]*"
    netAmountRegex = ".*net\samount.*[0-9]*"
    total = re.findall(totalAmountRegex + "|" + netAmountRegex, ocrOutput)
    maxTotal = 0
    for string in total:
      number = re.findall('\d+', string)
      # print(number[0], string)
      if(number):
        number = number[0]
        number = int(number)
        if(number>maxTotal):
          maxTotal=number

    invoiceRegex = "inv.*\t{0,1}[:-=]{0,1}\t{0,1}[0-9a-z]+"
    billIdRegex = "bill.*\t{0,1}[:-=]{0,1}\t{0,1}[0-9a-z]+"
    receiptRegex = "receipt.*\t{0,1}[:-=]{0,1}\t{0,1}[0-9a-z]+"
    invoiceNo = re.findall(invoiceRegex + "|" + billIdRegex + "|" + receiptRegex, ocrOutput)
    for invoiceDetail in invoiceNo:
      if(re.findall("[a-z]*\t{0,1}[a-z]*[\.#=:\\t]",invoiceDetail)):
        print(invoiceDetail)
      # print(splittedInvoice)

    # regex2 = "\d{2}[/-](?:jan|feb|mar|apr|jun|jul|aug|sep|nov|dec|january|february|march|april|june|july|august|september|november|december|\d{2})[/-]\d{2,4}"
    
    # dateRegex = re.compile(dateRegex)
    # regex2 = re.compile(regex2)
    #print(dateRegex)

    # commonRegexOutput = CommonRegex(ocrOutput)
    # colonSeperatedValues = re.findall(".*:.*", ocrOutput)

    # totalRegexes = [
    #   ".*total.*[0-9]*",
    #   ".*net\samount.*[0-9]*"
    # ]

    # total = re.findall("(" + ")|(".join(totalRegexes) + ")", ocrOutput)
    date = re.findall(dateRegex, ocrOutput)
    if date:
      date = date[0]
    times = re.findall(timeRegex, ocrOutput)
    print(times)
    time = []
    if times:
      for time1 in times:
        if('am' in time1 or 'pm' in time1):
          time = time1
          break
        else:
          splittedList = time1.split(":")
          count = 0
          for element in splittedList:
            # if(element in)
            element = int(element)
            if((0<=element<60)):
              count+=1
          if(count==len(splittedList)):
            time = time1
            break


      # time = time[0]
    # if date[0]:
    #   date = date[0]
    # if commonRegexOutput.times:
    #   time = commonRegexOutput.times[0]
    # time = ""
    # total1 = re.findall(regex2, ocrOutput)
    # if total:
    #   total = total.group()
    # if total1:
    #   total1 = total1.group() 

    # print(total)
    # print(total1)
    # for string in total:
    #   if string.contains:
    return "{}\n{}\n{}\n{}\n{}".format(date,time,invoiceNo,maxTotal, ocrOutput)
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
    app.run(host='localhost', port=5000, debug=True)