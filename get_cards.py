from flask import Flask
from flask import request
from flask import send_file
from flask.json import load
from gen_slides import load_cards, load_head
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def upload_file():
    if request.method == 'GET':
        f = request.json
        os.system("rm giz_class.tex")
        slide_pdf = "giz_class.pdf"
        slide_file = open("giz_class.tex","w")
        doc = ""
        doc = load_head(doc)
        doc = load_cards(doc, f['cards'])
        slide_file.write(doc)
        slide_file.close()
        os.system("pdflatex giz_class.tex")
        return send_file(slide_pdf, mimetype='application/pdf')

if __name__ == "__main__":
    app.run()