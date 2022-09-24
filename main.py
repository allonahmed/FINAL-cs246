import os
import sys
sys.path.insert(0, '/Users/allon/myProjects/Personal-File-Server/services/')
from flask import Flask, request, Response, jsonify, render_template
from dotenv import load_dotenv
import route_func
import boto3
import json

app = Flask(__name__)

load_dotenv()

# BUCKET = 'file-server-ahmed'
AWSclient = boto3.client( #s3 kkey id and access key
    's3',
    aws_access_key_id=os.getenv('PUBLIC_KEY'),
    aws_secret_access_key=os.getenv('SECRET_KEY'),
)  

app.add_url_rule('/', view_func = route_func.home)
app.add_url_rule('/register/<apikey>', view_func = route_func.register)
app.add_url_rule('/upload/<filename>', view_func = route_func.upload)
app.add_url_rule('/files', view_func = route_func.files)
app.add_url_rule('/files/<filename>', view_func = route_func.getfile)
app.add_url_rule('/delete/<filename>', view_func = route_func.deletefile)
app.add_url_rule('/removeuser/<key>', view_func = route_func.remove)
app.add_url_rule('/deleteAll', view_func = route_func.delAllFiles)

if __name__ == "__main__":
    app.run(host = '0.0.0.0',port=8080, debug=True)

