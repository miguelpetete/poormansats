from flask import redirect, url_for, Blueprint, render_template
from poorman.candidates.forms import ApplicationForm
from poorman import db
from poorman.models import Candidate

candidates = Blueprint('candidates', __name__)
