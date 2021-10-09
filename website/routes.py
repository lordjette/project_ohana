from flask import Blueprint, render_template, request, redirect, url_for
from .models import Task
from . import db

routes = Blueprint('routes', __name__)


@routes.route("/")
@routes.route("/home", methods=["GET", "POST"])
def home():
    selected_map = request.args.get('type')
    if selected_map == 'hospitals_and_clinics':
        ipmap = '/map_health'
    elif selected_map == 'schools':
        ipmap = '/map_educ'
    elif selected_map == 'stores':
        ipmap = '/map_grocery'
    elif selected_map == 'police':
        ipmap = '/map_security'
    elif selected_map == 'transpo':
        ipmap = '/map_transpo'
    elif selected_map == 'banks':
        ipmap = '/map_finance'
    else:
        ipmap = '/map'              
    return render_template("home.html", type=selected_map, ipmap=ipmap)

@routes.route("/list")
def list():
    list = Task.query.all()
    return render_template("list.html", list=list)


@routes.route("/new-task", methods=['GET', 'POST'])
def new_task():
    if request.method == 'POST':
        task = request.form.get('task')

        if len(task)==0:
            return redirect(url_for('routes.new_task'))
        else:
            new_task_add = Task(task=task)

            db.session.add(new_task_add)
            db.session.commit()
            return redirect(url_for('routes.list'))

    else:
        return render_template("new_task.html")


@routes.route("/edit-task/<id>", methods=["GET", "POST"])
def edit_task(id):
    current_task = Task.query.filter_by(id=id).first()

    if request.method == 'POST':
        new_task = request.form.get('task')
        if len(new_task) == 0:
            return redirect(url_for('routes.edit_task', id=id))
        else:
            current_task.task = new_task
            db.session.commit()
            return redirect(url_for('routes.list'))

    else:
        return render_template("new_task.html", current_task=current_task)


@routes.route("/delete-task/<id>", methods=["GET", "POST"])
def delete_task(id):
    current_task = Task.query.filter_by(id=id).first()
    db.session.delete(current_task)
    db.session.commit()
    return redirect(url_for('routes.list'))






@routes.route('/map')
def map():
    return render_template('map.html')

@routes.route('/map_grocery')
def map_grocery():
    return render_template('map_grocery.html')

@routes.route('/map_educ')
def map_educ():
    return render_template('map_educ.html')

@routes.route('/map_security')
def map_security():
    return render_template('map_security.html')

@routes.route('/map_finance')
def map_finance():
    return render_template('map_finance.html')

@routes.route('/map_transpo')
def map_transpo():
    return render_template('map_transpo.html')

@routes.route('/map_health')
def map_health():
    return render_template('map_health.html')

@routes.route('/map_single')
def map_single():
    return render_template('map_single.html')