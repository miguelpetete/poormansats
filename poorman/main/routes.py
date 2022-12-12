import pika, sys, json
from flask import render_template, request, Blueprint, flash, redirect, url_for
from poorman.candidates.forms import ApplicationForm
from poorman.models import Candidate
from poorman import db
from datetime import datetime

main = Blueprint('main', __name__)

def create_dictionary(candidate):
    dictionary = {
        'name': candidate.name,
        'first_surname': candidate.first_surname,
        'second_surname': candidate.second_surname,
        'email': candidate.email,
        'job_code': 'BE03-345',
        'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    }
    return dictionary

def send_candidate(candidate):
    connection_parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.queue_declare(queue='letterbox')
    message = create_dictionary(candidate)
    channel.basic_publish(exchange='', routing_key='letterbox', body=json.dumps(message))
    print(f"sent candidate: {candidate.name}")
    connection.close()


@main.route("/")
@main.route("/home", methods=['GET'])
def home():
    form = ApplicationForm()
    return render_template("form.html", form=form)

@main.route("/apply", methods=['POST'])
def apply():
    form = ApplicationForm()
    if form.validate_on_submit():
        candidate = Candidate(name=form.name.data, first_surname=form.first_surname.data, 
                              second_surname=form.second_surname.data, email=form.email.data)
        send_candidate(candidate)
        db.session.add(candidate)
        db.session.commit()
        flash('Your application has been submited. You will receive information soon.')
        return redirect(url_for('main.home'))
    return render_template("form.html", form=form)
