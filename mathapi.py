import wolframalpha
import json
from pylatexenc.latex2text import LatexNodes2Text
import requests 
from flask import Flask, request


API_KEY = "P4GQGJ-RGG8K2W9EV"
client = wolframalpha.Client(API_KEY)

app = Flask(__name__)
@app.route('/solve', methods = ['POST', 'GET'])
def math():
    p = (("format", "image,plaintext"),("podstate", "Step-by-step solution"),)
    eq = LatexNodes2Text().latex_to_text(request.form['equation'])
    res = client.query(eq, params=p)
    data = {}
    for p in res.pods:
        for s in p.subpods:
            if s["plaintext"] == None:
                if p["@title"] in data:
                    data[p["@title"]].append(s.img.src)
                else:
                    data[p["@title"]] = [s.img.src]
            else:
                if p["@title"] in data:
                    data[p["@title"]].append(s.plaintext)
                else:
                    data[p["@title"]] = [s.plaintext]
    
    json_object = json.dumps(data, indent = 4, ensure_ascii=False) 
    return json_object

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5001')
