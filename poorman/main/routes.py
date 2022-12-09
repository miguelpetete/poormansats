from flask import render_template, request, Blueprint

@main.route("/")
@main.route("/home")
def home():
    return render_template("test.html")