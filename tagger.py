"""
-----------------------------------------------------------------------
tagger.py
-----------------------------------------------------------------------

A helper app that allows copy-and-paste of a job description into a 
submit box for faster tagging.

Currently designed for tagging of jobs skills section.
"""
from flask import Flask 
from flask import render_template, request, session, redirect, url_for
import glob
from random import randint
import json
from utils import parse_sentences

app = Flask(__name__, template_folder="assets/tagger/template", static_folder="assets/tagger/static")
app.secret_key = "classifier"

@app.route("/", methods=["GET", "POST"])
def tagger():
    # get previously tagged document indexes
    if not session.get("tagged"):
        i_s = [int(file.replace("out\\", "").replace(".json", "")) for file in glob.glob("out/*")]
        session["tagged"] = i_s

    # find new random document to tag
    if not session.get("i") or session.get("i") in session.get("tagged"):
        files = glob.glob("files/*")
        selection = [i for i in range(0, len(files)) if i not in session["tagged"]]
        if len(selection) == 0:
            return redirect(url_for("done"))
        session["i"] = selection[randint(0, len(selection) - 1)]

    # read in job file
    i = session["i"]
    try:
        with open(f"files/{i}.txt", "r", encoding="utf-8") as file:
            job = file.read()
    # TODO: Some files don't actually exist, improve randomiser
    except FileNotFoundError as _:
        session["tagged"] += [i]
        return redirect(url_for("tagger"))
    
    if request.method == "GET":
        return render_template("index.html", job=job)
    
    # Submitted the segment containing job skills information
    # Pair parsed sentences (all) and tagged (segment) together in json
    if request.method == "POST":
        i = session["i"]
        if request.form["submit-button"] == "add":

            data = {}
            rows = request.form["submit-box"]
            data["sentences"] = parse_sentences(job)
            data["segment"] = parse_sentences(rows)

            out_file = open(f"out/{i}.json", "w+")
            json.dump(data, out_file)
            out_file.close()

            session["tagged"] += [i]
            return redirect(url_for("tagger"))
    return render_template("index.html", job=job)

@app.route("/done")
def done():
    return "<h1>Done!</h1>"    

if __name__ == "__main__":
    app.run(port=8000)