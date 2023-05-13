"""
-----------------------------------------------------------------------
classify.py
-----------------------------------------------------------------------

A small flask app that allows you to paste in a job description and picks
out the skills for you.
"""
from flask import Flask, render_template, request, redirect, url_for
from utils import parse_sentences, preprocessing
import pickle

app = Flask(__name__, template_folder="assets/classify/template", static_folder="assets/classify/static")

with open("models/vectoriser.pkl", "rb") as v:
    vec = pickle.load(v)
with open("models/model.pkl", "rb") as m:
    model = pickle.load(m)

@app.route("/", methods=["GET", "POST"])
def classify():
    if request.method == "GET":
        return render_template("index.html")
    
    if request.method == "POST":
        data = request.form["job-box"]
        if data:
            data_sentences = parse_sentences(data)

            # transform the job description into a digestable format for the model
            skills_section = []
            for sentence in data_sentences:
                cleaned_sentence = preprocessing(sentence)
                vectorised = vec.transform([cleaned_sentence])
                label = model.predict(vectorised)
                if label[0] == '1':
                    skills_section.append(sentence)
            skills_section = "\n".join(skills_section)

        return redirect(url_for("classified", data=data, segment=skills_section))

@app.route("/results", methods=["GET"])
def classified():
    return render_template("results.html", 
                           data=request.args["data"],
                           segment=request.args["segment"])


if __name__ == "__main__":
    app.run(port="8000")