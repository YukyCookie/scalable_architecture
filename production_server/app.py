from workerA import get_accuracy

from flask import (
   Flask,
   request,
   jsonify,
   Markup,
   render_template 
)

# app = Flask(__name__, template_folder='./templates',static_folder='./static')
app = Flask(__name__)

@app.route("/")
def index():
    return '<h1>Welcome to the Group13 project.</h1>'

@app.route("/accuracy", methods=['GET'])
def accuracy():
    r = get_accuracy.delay()
    a = r.get()
    return '<h1>Model {} r2 score: {}</h1>'.format(a["model"], a["result"])

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5100,debug=True)
