from pyfiles import app
from flask import Flask, flash, request, redirect, url_for,render_template
import os
from werkzeug.utils import secure_filename
from pyfiles import compressed, rul
import pandas as pd

UPLOAD_FOLDER = 'file_upload'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# from flask_sqlalchemy import SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///holes.db'
# db=SQLAlchemy(app)


# class Item(db.Model):
#     id=db.Column(db.Integer, primary_key=True)
#     name=db.Column(db.String, nullable=False)
#     data=db.Column(db.LargeBinary)
#     cluster=db.Column(db.Integer)
#     rul=db.column(db.Numeric)


def execute(cs,rs):
    # If filename is valid
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/clear',methods=["POST"])
    def clear():
        cs.clear()
        rs.clear()
        return redirect(url_for('upload_file',cs=cs,rs=rs))
    
    #Upload file
    @app.route('/', methods=['GET','POST'])
    def upload_file():
        if request.method == 'POST':
            print(request.files)
            if 'myfile' not in request.files:
                print("No file part")
                return redirect(request.url)
            file = request.files['myfile']
            if file.filename == '':
                print("No selected file")
                return redirect(request.url)
            if file and allowed_file(file.filename):
                print("Correct")
                filename = secure_filename(file.filename)
                (data_comp,final_cluster) = compressed.calcClusters(file)
                pred_rul=rul.calcRUL(data_comp,final_cluster)
                r=float("{:.2f}".format(pred_rul))
                cs.append(final_cluster)
                rs.append(r)
                return render_template('upload.html',cs=cs,rs=rs)
        print("CLUSTERS HERE:")
        return render_template('upload.html',cs=cs,rs=rs)

 
    @app.route('/home/upload')
    def upload():
        return render_template('upload.html')
