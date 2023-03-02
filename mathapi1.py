import wolframalpha
from pylatexenc.latex2text import LatexNodes2Text
import requests 
from flask import Flask, request


API_KEY = "P4GQGJ-RGG8K2W9EV"
client = wolframalpha.Client(API_KEY)

app = Flask(__name__)
@app.route('/solve', methods = ['POST', 'GET'])
def math():
    eq = LatexNodes2Text().latex_to_text(request.form['equation'])
    res = client.query(eq, params=(("format", "image,plaintext"),("podstate", "Result__Step-by-step%20solution"),))
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
    
    d = requests.get('http://api.wolframalpha.com/v2/query?podstate=Result__Step-by-step+solution&input=' + eq + '&format=plaintext&appid=' + API_KEY ).text
    if "<subpod title='Possible intermediate steps'>" in d:
        d = d.split("<subpod title='Possible intermediate steps'>")
        data["steps"] = d[1].split("plaintext")[1][1:-2]
    json_object = json.dumps(data, indent = 4, ensure_ascii=False) 
    return json_object


    
# math( LatexNodes2Text().latex_to_text("5*7x^2+x=-4x+32"))

# math( LatexNodes2Text().latex_to_text("solve 3x -7=11"))

# math( LatexNodes2Text().latex_to_text("x+5x*7x=32-4x"))

# math(LatexNodes2Text().latex_to_text("87/5 as a mixed number"))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')
