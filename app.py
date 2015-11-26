import urllib2
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
@app.route("/home", methods=["GET","POST"])
def home():
    """ runs home page and from for query input
    
    Returns:
     Home page or result page if query is inputed
    
    """
    if request.method == "GET":
        return render_template("home.html")
    else:
        q = request.form.get('query')
        if(q==""):
            q="no question entered, try again"
        return redirect(url_for("results",query=q))
@app.route("/results",  methods=["GET","POST"])
@app.route("/results/<query>",  methods=["GET","POST"])
def results(query):
    """Gets query that the user entered in the home page 
    and displays the answer
    
    Arguments:
     query: a string that is the user's query input

    Return:
     html page with answer to query

    """

    try:
        result = conchshell.find_results(query)
        return render_template("results.html", question=query, answer=result, error=False)
    except:
        return render_template("results.html", question=query, answer="nope", error=["your question is wrong"])

if __name__=="__main__":
    app.debug = True
    app.run(host='0.0.0.0',port=8000)
