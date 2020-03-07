from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
import argparse
from pytesseract import image_to_string
from uuid import uuid4
import os
import cv2
import numpy as np
import re
import shutil
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
    f.save(f.filename)
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--preprocess", type=str, default="thresh",
      help="type of preprocessing to be done")
    args = vars(ap.parse_args())
    image = cv2.imread(f.filename)
    # scale_percent = 40 # percent of original size
    # width = int(image.shape[1] * scale_percent / 100)
    # height = int(image.shape[0] * scale_percent / 100)
    # dim = (height, width)
    # resize image
    #image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    #cv2.imshow("Blur", image)
    # convert the image to grayscale and flip the foreground
    # and background to ensure foreground is now "white" and
    # the background is "black"
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    thresh = cv2.threshold(gray, 0, 240,
      cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # grab the (x, y) coordinates of all pixel values that
    # are greater than zero, then use these coordinates to
    # compute a rotated bounding box that contains all
    # coordinates
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    # the `cv2.minAreaRect` function returns values in the
    # range [-90, 0); as the rectangle rotates clockwise the
    # returned angle trends to 0 -- in this special case we
    # need to add 90 degrees to the angle
    if angle < -45:
      angle = -(90 + angle)
    # otherwise, just take the inverse of the angle to make
    # it positive
    else:
      angle = -angle
    # rotate the image to deskew it
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
      flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    # draw the correction angle on the image so we can validate it
    cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),
      (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    # show the output image
    if h<w:
        angle=-90
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h),
          flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        # draw the correction angle on the image so we can validate it
        cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),
          (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        # width = int(image.shape[0])
        # height = int(image.shape[1])
        #dim = (w, h)
        # resize image
        #image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

        
    #print("[INFO] angle: {:.3f}".format(angle))
    #cv2.imshow("Input", image)
    #cv2.imshow("Rotated", rotated)
    #cv2.waitKey(0)
    # dim=(512,512)
    # image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    
    # load the example image and convert it to grayscale
    #image = cv2.imread(args["image"])
    gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
    
    #cv2.imshow("Image", gray)
    
    # check to see if we should apply thresholding to preprocess the
    # image
    if args["preprocess"] == "thresh":
      gray = cv2.threshold(gray, 0, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    # make a check to see if median blurring should be done to remove
    # noise
    elif args["preprocess"] == "blur":
      gray = cv2.medianBlur(gray, 3)
    # ret,gray = cv2.threshold(gray, 0, 255,cv2.THRESH_OTSU|cv2.THRESH_BINARY_INV)
    
    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.jpg".format(os.getpid())
    cv2.imwrite(filename, gray)
    
    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    ocrOutput = pytesseract.image_to_string(Image.open(filename)).lower()
    os.remove(filename)
    os.remove(f.filename)
    # os.remove(filename)
    # #print(text)
    # temp=r"C:\Users\aakas\Desktop\AIDL\New"
    # fullpath=os.path.join(temp, filename1)
    # # show the output images
    # #cv2.imshow("Image", image)
    # cv2.imwrite(fullpath ,image)
    # #cv2.imshow("Output", gray)
    # cv2.waitKey(0)
    # return f.filename
    # img1=Image.open(f)
    # folder_name = str(uuid4())
    # os.makedirs("FlaskFiles")
    # with open('./{fn}/output.txt'.format(fn=folder_name),'wb') as f:
    #   f.write(image_to_string(img1))
    # ocrOutput = image_to_string(img1).lower()
    # monthsShort= 'jan|feb|mar|apr|jun|jul|aug|sep|nov|dec'
    # monthsLong= 'january|february|march|april|june|july|august|september|november|december'
    # monthInteger =  '[0-9]{2}'
    # months= '(' + monthsShort + '|' + monthsLong + '|' + monthInteger + ')'
    # separators = '[/-]'
    # days = '[0-9]{2}'
    # years = '[0-9]{4}'
    dateFirstOrYearFirst = "\d{1,4}[\/.\-\s](?:jan|feb|mar|apr|jun|jul|aug|sep|nov|dec|january|february|march|april|june|july|august|september|november|december|\d{1,2})[\/.\-\s]\d{1,4}";
    monthFirst = "(jan|feb|mar|apr|jun|jul|aug|sep|nov|dec|january|february|march|april|june|july|august|september|november|december|\d{1,2})[\/.\-\s]\d{1,2}[\/.\-\s,]\s*\d{1,4}";
    # dateLastRegex = "\d{1,4}[/.-](?:jan|feb|mar|apr|jun|jul|aug|sep|nov|dec|january|february|march|april|june|july|august|september|november|december|\d{1,2})[/.-]\d{1,2}";
    dateRegex = dateFirstOrYearFirst;
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
    invoiceNoFinal = []
    for invoiceDetail in invoiceNo:
      if(re.findall("[a-z]*[.]{0,1}\s{0,1}[a-z]*[\.#=:\s]",invoiceDetail)):
        r = re.compile(r"[a-z]*[.]{0,1}\s{0,1}[a-z]*[\.#=:\s]")
        newInvoiceNo = r.sub(' ', invoiceDetail)
        # newInvoiceNo = re.findall("[a-z]*[.]{0,1}\s{0,1}[a-z]*[\.#=:\s](.+?)", invoiceDetail)
        if newInvoiceNo:
          print(newInvoiceNo)
          newInvoiceNo = newInvoiceNo.strip().split(" ")
          print(newInvoiceNo[0])
          invoiceNoFinal = newInvoiceNo[0]
          break
          
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
          # print(splittedList)
          count = 0
          for index in range(len(splittedList)):
            # if(element in)
            splittedList[index] = int(splittedList[index])
            if index==0:
              if(0<=splittedList[index]<24):
                count+=1;
                continue
              else:
                break
            if((0<=splittedList[index]<60)):
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
    return "Date:{}\nTime: {}\nInvoice No: {}\nBill Amount:  {}\nInvoice List: {}\nOCR Conversion: {}".format(date,time,invoiceNoFinal, maxTotal, invoiceNo, ocrOutput)
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