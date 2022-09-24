import os
import sys
sys.path.insert(0, '/Users/allon/myProjects/Personal-File-Server/services/')
from flask import Flask
from dotenv import load_dotenv
import route_func

app = Flask(__name__)

load_dotenv()

app.add_url_rule('/', view_func = route_func.home)
app.add_url_rule('/register/<apikey>', view_func = route_func.register)
app.add_url_rule('/upload/<filename>', methods=['POST'], view_func = route_func.upload)
app.add_url_rule('/files', view_func = route_func.files)
app.add_url_rule('/files/<filename>', view_func = route_func.getfile)
app.add_url_rule('/delete/<filename>', view_func = route_func.deletefile)
app.add_url_rule('/removeuser/<key>', view_func = route_func.remove)
app.add_url_rule('/deleteAll', view_func = route_func.delAllFiles)

if __name__ == "__main__":
    app.run(host = '0.0.0.0',port=8080, debug=True)

