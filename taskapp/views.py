from flask import flash, render_template, request, session, url_for, redirect
from mongoengine import connect
from taskapp import app
from taskapp.models import Users, Tasks


connect('notesapp', host='localhost', port=27017)

Users.drop_collection()
Tasks.drop_collection()

admin_user = Users(user_name="admin", user_password="admin").save()
guest_user = Users(user_name="esteban", user_password="qwerty").save()

admin_task1 = Tasks(task_text="Install System Updates", task_status=False, user_id=admin_user.id).save()
admin_task2 = Tasks(task_text="Call mom", task_status=True, user_id=admin_user.id).save()

guest_task1 = Tasks(task_text="Buy a Coffescript Book", task_status=True, user_id=guest_user.id).save()
guest_task2 = Tasks(task_text="Start DLC Legend of Zelda BoTW", task_status=False, user_id=guest_user.id).save()
guest_task3 = Tasks(task_text="Learn Flask", task_status=True, user_id=guest_user.id).save()


@app.route('/')
def index():   
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return load_user_task()


@app.route('/login', methods=['POST'])
def login():
    _user_name = request.form["inputName"]
    _user_password = request.form["inputPassword"]
    try:
        _user_cursor = Users.objects(user_name=_user_name, user_password=_user_password)
        for user in _user_cursor:
            user_id = str(user.id)
            user_name = user.user_name
        if user_id is not "" and user_name is not "":
            session['logged_in'] = True
            session['user_id'] = user_id
            session['user_name'] = user_name
    except:
        flash('wrong password!')
    return index()


@app.route('/create_note', methods=['POST'])
def create_note():
    _task_text = request.form['inputTask']
    _user_id = request.form['inputUserId']
    Tasks(task_text=_task_text, task_status=False, user_id=_user_id).save()
    return redirect(url_for('index'))


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()


def load_user_task():
    user_name = session['user_name']
    user_id = session['user_id']
    user_task_list = Tasks.get_task_object(user_id)
    return render_template('list.html', user_name=user_name, user_id=user_id, user_task_list=user_task_list)


@app.route('/delete_user_task', methods=['POST'])
def delete_user_task():
    _task_id = request.json['task_id']
    Tasks.objects(id=_task_id).delete()
    return "Success"


@app.route('/check_task', methods=['POST'])
def check_task():
    _task_id = request.json['task_id']
    _task_status = request.json['task_status']
    Tasks.objects(id=_task_id).update(task_status=_task_status)
    return "Success"


@app.route('/create_user', methods=['POST'])
def create_user():
    _user_name = request.form['userName']
    _user_password = request.form['userPassword']
    Users(user_name=_user_name, user_password=_user_password).save()
    return redirect(url_for('index'))