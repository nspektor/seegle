import urllib2
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
@app.route("/home", methods=["GET","POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")
    else:
        q = request.form.get('query')
        return redirect(url_for("results",query=q))

@app.route("/results",  methods=["GET","POST"])
@app.route("/results/<query>",  methods=["GET","POST"])
def results(query):
    """
    gets query that the user entered in the home page and displays the answer
    """
    try:
        result = conchshell.find_results(query)
        return render_template("results.html", question=query, answer=result, error=False)
    except:
        return render_template("results.html", question=query, answer="nope", error=["your question is wrong"])

if __name__=="__main__":
    app.debug = True
    app.run(host='0.0.0.0',port=8000)
