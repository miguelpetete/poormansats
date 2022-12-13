from flask import redirect, url_for, Blueprint, render_template
from poorman.candidates.forms import ApplicationForm
from poorman import db
from poorman.models import Candidate

candidates = Blueprint('candidates', __name__)

@candidates.route("/appliance", methods=['GET', 'POST'])
def apply():
    form = ApplicationForm()
    if form.validate_on_submit():
        candidate = Candidate(name=form.name.data, first_surname=form.first_surname.data, 
                              second_surname=form.second_surname.data, email=form.email.data)
        db.session.add(candidate)
        db.session.commit()
        flash('Your application has been submited. You will receive information soon.')
        return render_template('apply.html')
    return render_template('apply.html')