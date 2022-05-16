import csv
import os
from os.path import dirname, join, realpath

from flask import Flask, redirect, render_template, request, url_for

# from search import search_leads

app = Flask(__name__)

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = "static/files"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Root URL
@app.route("/")
def index():
    # Set The upload HTML template '\templates\index.html'
    return render_template("index.html")


# Get the uploaded files
@app.route("/", methods=["POST"])
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files["file"]
    if uploaded_file.filename != "":
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename)  # set the file path
        uploaded_file.save(file_path)  # save the file

    with open(file_path) as input:
        reader = csv.reader(input)
        for word in reader:
            print(word[0])
            # search_rankings(word[0]) #検索順位を表示する
            # search_leads(word[0])
    print("csv file has exported")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(port=5000)
