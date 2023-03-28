from flask import Flask, render_template, request, redirect
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2


app = Flask(__name__)

app.config["Images"]= "/Users/sahithijarugula/question2/static/Images"

image_list= []
filenames = []
labels = []
seg1 = []
seg2 = []
index = 0


#code to get first set of uploaded images
@app.route("/home", methods=["POST","GET"])
def upload_image():
  if request.method == "POST":

    image = request.files["file"]
    basedir = os.path.abspath(os.path.dirname(__file__))
    filename = image.filename
    path = os.path.join(basedir, app.config["Images"], filename)
    image.save(path)  
    image_list.append(path)
    filenames.append(filename)
    text_value = request.form["text_box"]
    labels.append(text_value)
    return render_template("main.html")

  return render_template("main.html")

#After user has finished uploaded the first set this takes user to page that asks 
#for segmentation images
@app.route("/seg", methods=["POST","GET"])
def done():
  if request.method == "POST":
    return render_template("seg.html", filename = filenames[index])

#Gets first set of segmentation images saves them in seg1 and then
#adds gaussian noise and displays those images then asks for a 
#second set of segmentation images and saves them in seg2
@app.route("/home2", methods=["POST", "GET"])
def get_segs():
  global index
  if request.method == "POST":
    image = request.files["file"]
    basedir = os.path.abspath(os.path.dirname(__file__))
    filename = image.filename
    path = os.path.join(basedir, app.config["Images"], filename)
    image.save(path)
    length = len(image_list)
    if(index < length):
      seg1.append(path)
      img = add_noise(path)
      filename2 = "2"+ filename
      directory = os.path.join(basedir, app.config["Images"])
      os.chdir(directory)
      cv2.imwrite(filename2, img)
      filenames.append(filename2)
    else:
      seg2.append(path)

    index = index + 1
    if(index < (length*2)):
      return render_template("seg.html", filename = filenames[index])
    else:
      append_csv()
      return render_template("main.html")
  
#adds gaussian noise
def add_noise(path):
  img=cv2.imread(path,0)

  gauss_noise=np.zeros(img.shape,dtype=np.uint8)
  cv2.randn(gauss_noise,128,20)
  gauss_noise=(gauss_noise*0.5).astype(np.uint8)
  gn_img=cv2.add(img,gauss_noise)
  return  gn_img

#adds all paths to images and their text labels to a csv
def append_csv():
  df_list = list(zip(image_list, seg1, seg2, labels))
 
  df = pd.DataFrame(df_list, columns=["Images", "Segmentation1", "Segmentation2", "Labels"])
  
  basedir = os.path.abspath(os.path.dirname(__file__))
  app.config["question2"]= "/Users/sahithijarugula/question2"
  path = os.path.join(basedir, app.config["question2"], "image_info.csv")
  df.to_csv(path, mode="a", index=False, header=False)

@app.route("/display/<filename>")
def display_image(filename):
  return redirect(url_for("static", filename = "/Images/"+filename))

app.run(port=5000) 

