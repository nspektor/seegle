import urllib2
from flask import Flask, request, render_template, redirect, url_for
from conchshell import find_results

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
        q = request.form["query"]
        if (not q or
            q.isspace()):
            
            return render_template("home.html")
        
        return redirect(url_for("results", query=q))

    
@app.route("/results/<query>",  methods=["GET","POST"])
def results(query):
    """Gets query that the user entered in the home page 
    and displays the answer
    
    Arguments:
     query: a string that is the user's query input

    Return:
     html page with answer to query
    """
  
    result = find_results(query)
    return render_template("results.html", question=query, answer=result)
   


if __name__=="__main__":
    app.debug = True
    app.run(host='0.0.0.0',port=8000)
