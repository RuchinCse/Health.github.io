
import flask
import pickle
import pandas as pd
import numpy as np
import cv2
import keras
from keras.preprocessing.image import img_to_array
from werkzeug import secure_filename


app = flask.Flask(__name__, template_folder='templates', static_url_path='/static')
@app.route('/',methods=['GET' ,'POST'])
def main():
	if flask.request.method == 'GET':
		return(flask.render_template('index.html'))
	if flask.request.method == 'POST':
		with open (f'model/food.pkl','rb') as f:
			model= pickle.load(f)
		#f = flask.request.files['file']
		
		#f.save(secure_filename(f.filename))
		#read image file string data
		f = flask.request.files['file'].read()
		print(type(f))
		
		
		#npimg = np.asarray(npimg)
		# convert numpy array to image
		#img = cv2.imdecode(npimg, cv2.CV_LOAD_IMAGE_UNCHANGED)
		npimg = np.fromstring(f, np.uint8)
		npimg = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
		npimg = cv2.resize(npimg,(224,224))
		npimg = cv2.cvtColor(npimg,cv2.COLOR_BGR2RGB)
		print(type(npimg))
		#npimg = img_to_array(npimg) 
		npimg = npimg.reshape(1,224,224,3)
		#im = cv2.imread("model/Beach.jpg",mode='RGB')
		prediction = model.predict(npimg)
		
		ans= np.max(prediction)
		for i in range(10):
			if(prediction[0,i] == ans):
				index=i	
		with open("Mydict.txt", "rb") as myFile:
			Dict = pickle.load(myFile)
		label=Dict[index]
		#calorie from csv file
		data = pd.read_csv("nu.csv")
		df= pd.DataFrame(data)
		df = df.set_index("item_name", drop = True)
		df =df.loc[label,:]
		c= df[0]
		f=df[1]
		carb=df[2]
		prot=df[3]
		vita=df[4]
		vitc=df[5]
		calc=df[6]
		iron=df[7]




		return flask.render_template('result.html',original_input = {'calories': c,'fat':f,'carbohydrates':carb,'protien':prot,'vitaminA':vita,'vitaminc':vitc,'calcium':calc,'iron':iron},result= label)
if __name__ == '__main__':
	app.run()

