# Importing essential libraries
from flask import Flask, render_template, request,redirect,url_for,send_from_directory
from google_trans_new import google_translator
import os
import codecs

from werkzeug.utils import secure_filename


translator = google_translator()

app = Flask(__name__,template_folder='templates')

UPLOAD_FOLDER_1 = 'd:\home\site\wwwroot\templates'



@app.route('/')
def home():
	return render_template('frontend2.html')
@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        message = request.files['myfile']
        if message:  
            filename =secure_filename(message.filename)
            message_location =os.path.join(
                UPLOAD_FOLDER_1, message.filename
            )  
            
            message.save(message_location)
            message.seek(0)
            text =message.read()
            text =str(text,'cp1252')
            text_to_translate = translator.translate(text,'hi')
            text2 = text_to_translate
            with codecs.open(filename, 'w',encoding="utf-8") as f:
                f.write(str(text2))
                return redirect('/downloadfile/'+ filename) 
    return render_template('frontend2.html')
# Download API
@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    return render_template('download.html',value=filename)

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    return send_from_directory(UPLOAD_FOLDER_1, filename, as_attachment=True)


if __name__ == '__main__':
	app.run(debug=True)
