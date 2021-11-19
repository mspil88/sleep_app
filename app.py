
from datetime import datetime
from flask import Flask, render_template, request, redirect, session, flash, make_response, url_for
from flask_session import Session
from flask_jsglue import JSGlue
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from sql_utils import SleepDatabase, create_db_key, USER_TABLE, TIME_TO_SLEEP, TIME_IN_BED_TABLE, NUMBER_OF_GAPS, \
    GAP_LENGTHS, SLEEP_MOODS, SLEPT_WELL, WEEK_COMMENCING, week_commencing_data
from helpers import login_required, process_diary_data, df_to_dict, get_previous_wcs, df_for_diary, \
    generate_diary_inputs, create_moods_chart, this_week_last_week_sef

import json
import os
import pandas as pd

app = Flask(__name__, template_folder='templates')

'''TODOS: 
        (1) CACHE background image
        (2) Fix login messages
        (3) DIARY TABLE, ORDER the WC filter2
        (4) ADD MOOD TABLE TO DIARY        
        (5) Implement actual email validation

'''


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["expires"] = 0
    response.headers["Prgama"] = "no-cache"
    return response


app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

jsglue = JSGlue()
jsglue.init_app(app)
Session(app)

sleep_db = SleepDatabase('database/sleep.db')
sleep_db.table_rendering(USER_TABLE, TIME_IN_BED_TABLE, TIME_TO_SLEEP, NUMBER_OF_GAPS, GAP_LENGTHS, SLEEP_MOODS,
                         SLEPT_WELL, WEEK_COMMENCING)


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user_id = session['user_id']


    if request.method == "GET":
        return render_template('index.html')
    else:
        sleep_times = {}
        data = request.get_json()
        sleep_times['inbed'] = data['inbed']
        sleep_times['outbed'] = data['outbed']
        created_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        created_date = created_on[0:10]
        user_key = create_db_key(user_id, created_date)

        sleep_db.update("INSERT or REPLACE INTO time_in_bed (user_key, user_id, in_bed, out_bed, created_on, created_date) VALUES (?, ?, ?, ?, ?, ?)",
                        (user_key, user_id, sleep_times['inbed'], sleep_times['outbed'], created_on, created_date))
        print(sleep_times)

        return render_template('index.html')


@app.route("/time_taken", methods=["GET", "POST"])
@login_required
def time_taken():
    user_id = session['user_id']

    if request.method == "GET":
        return render_template('time_taken.html')
    else:
        time_to = {}
        data = request.get_json()
        time_to['time_to_sleep'] = data['time_to_sleep']
        time_to['time_get_out'] = data['time_get_out']
        created_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        created_date = created_on[0:10]
        user_key = create_db_key(user_id, created_date)

        sleep_db.update("INSERT or REPLACE INTO time_to_sleep (user_key, user_id, time_to_fall_asleep, time_to_get_out_bed, created_on, created_date) VALUES (?, ?, ?, ?, ?, ?)",
                        (user_key, user_id, time_to['time_to_sleep'], time_to['time_get_out'], created_on, created_date))

        print(time_to)

        return render_template('time_taken.html')


@app.route("/slept_well", methods=["GET", "POST"])
#@login_required
def slept_well():
    user_id = session['user_id']
    if request.method == "GET":
        return render_template('slept_well.html')
    else:
        slept_well = {}
        data = request.get_json()
        slept_well['slept_well'] = data['slept_well']
        created_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        created_date = created_on[0:10]
        user_key = create_db_key(user_id, created_date)

        sleep_db.update(
            "INSERT or REPLACE INTO slept_well (user_key, user_id, slept_well, created_on, created_date) VALUES (?, ?, ?, ?, ?)",
            (user_key, user_id, slept_well['slept_well'], created_on, created_date))

        print(slept_well)

        return render_template('slept_well.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    session.clear()
    error = None
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        rows = sleep_db.select("SELECT * FROM users where email_address = ?", (username,))

        #fix messages
        if not username or not password:
            flash("Invalid username or password")
            return render_template("login.html")
        elif len(rows) == 0:
            flash("Account does not exist")
            return render_template("login.html")
        elif not check_password_hash(rows[0]['password'], password):
            flash("Incorrect password")
            return render_template("login.html")
        else:
            session['user_id'] = rows[0]['id']
            return redirect("/")


#redesign buttons into row/ column grid
@app.route("/feel", methods=["GET", "POST"])
#@login_required
def feel():
    user_id = session['user_id']
    if request.method == "GET":
        default_moods = ['tired', 'frustrated', 'irritable', 'refreshed', 'alert', 'groggy', 'add']
        max_date = sleep_db.select("SELECT max(created_date) as max_date from sleep_moods where user_id = ?", (user_id,))[0]['max_date']
        moods = sleep_db.select("SELECT selected_moods FROM sleep_moods where user_id = ? and created_date = ?", (user_id, max_date,))[0]['selected_moods'].split(",")
        moods = moods + ['add']

        if not moods:
            moods = default_moods

        return render_template('feel.html', moods=moods)
    else:
        print("posting")
        created_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        created_date = created_on[0:10]
        user_key = create_db_key(user_id, created_date)

        data = request.get_json()
        user_moods = [i for i in data['selected_moods'] if i != '']
        user_moods_str = ','.join([i for i in user_moods])
        selected_moods = data['tracked_moods']
        selected_moods_str = ','.join([i for i in selected_moods if i != 'add'])
        sleep_db.update(
            "INSERT  or REPLACE INTO sleep_moods (user_key, user_id, user_moods, selected_moods, created_on, created_date) VALUES (?, ?, ?, ?, ?, ?)",
            (user_key, user_id, user_moods_str, selected_moods_str, created_on, created_date))
        print(user_moods_str)
        print(selected_moods_str)
        return render_template('feel.html')


@app.route("/gaps", methods=["GET", "POST"])
@login_required
def gaps():
    user_id = session['user_id']
    if request.method == "GET":

        return render_template('gaps.html')
    else:
        data = request.get_json()
        print(data)
        created_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        created_date = created_on[0:10]
        user_key = create_db_key(user_id, created_date)

        sleep_db.update(
            "INSERT  or REPLACE INTO sleep_gaps (user_key, user_id, gaps,  created_on, created_date) VALUES (?, ?, ?, ?, ?)",
            (user_key, user_id, data, created_on, created_date))

        return render_template('gaps.html')


@app.route("/add_gaps", methods=["GET", "POST"])
# @login_required
def add_gaps():
    user_id = session['user_id']
    created_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_date = created_on[0:10]
    user_key = create_db_key(user_id, created_date)
    num_gaps = sleep_db.select("select gaps from sleep_gaps where user_key = ?", (user_key, ))[0]['gaps']
    print(num_gaps)
    #if gaps zero then do not serve
    if request.method == "GET":

        return render_template('add_gaps.html', gaps=num_gaps)
    else:
        data = request.get_json()
        print(data)
        data_str = ','.join([i for i in data])
        sleep_db.update(
            "INSERT or REPLACE INTO gap_lengths (user_key, user_id, gap_lengths, created_on, created_date) VALUES (?, ?, ?, ?, ?)",
            (user_key, user_id, data_str, created_on, created_date))

        print(data_str)

        #adjust this
        return render_template('add_gaps.html', gaps=num_gaps)


def validate_register_inputs(username, password, confirmation):

    error = False
    if not username:
        flash("Invalid username")
        error = True
    elif not password:
        flash("Invalid password")
        error = True
    elif password != confirmation:
        flash("Invalid confirmation")
        error = True
    return error

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirm")
        now = datetime.now()
        check = sleep_db.select("select * from users where email_address = ?", (username,))

        error = validate_register_inputs(username, password, confirmation)

        if error:
            return render_template("register.html")
        elif check:
            flash("Account already exists")
            return render_template("register.html")
        else:
            pw = generate_password_hash(password)
            sleep_db.update("INSERT INTO users (email_address, password, created_on) VALUES (?, ?, ?)", (username,
                                                                                                          pw,
                                                                                                          now))
            return redirect("/login")

    else:
        return render_template("register.html")

@app.route("/dashboard", methods=["GET", "POST"])
#@login_required
def dashboard():
    if request.method == "POST":
        return NotImplementedError
    else:
        return render_template("dashboard.html")


@app.route("/diary2", methods=["GET"])
@login_required
def diary():
    user_id = session["user_id"]

    diary_table = sleep_db.select("SELECT DISTINCT a.user_id, a.created_date, a.in_bed, a.out_bed,"
                           "b.time_to_fall_asleep, b.time_to_get_out_bed, c.slept_well, "
                           "d.gaps, e.gap_lengths, g.selected_moods, f.wc "
                           "FROM time_in_bed a "
                           "left join time_to_sleep b "
                           "on a.user_id = b.user_id "
                           "and a.created_date = b.created_date "
                           "left join slept_well c "
                           "on a.user_id = c.user_id "
                           "and a.created_date = c.created_date "
                           "left join sleep_gaps as d "
                           "on a.user_id = d.user_id "
                           "and a.created_date = d.created_date "
                           "left join gap_lengths as e "
                           "on a.user_id = e.user_id "
                           "and a.created_date = e.created_date "
                           "left join sleep_moods as g "
                           "on a.user_id = g.user_id "
                           "and a.created_date = g.created_date "
                           "inner join week_commencing_ref as f "
                           "on a.created_date = f.created_date "                                                    
                           "where a.user_id = ?", (user_id,))

    try:
        sleep_data, hours_data, efficiency_data, ordered_week_commencing, mood_data, \
        this_week_sef, last_week_sef = generate_diary_inputs(diary_table)
    except KeyError:
        print("WARNING: Data not found")

    #mood_chart_json = create_moods_chart(mood_data)
    print(sleep_data)
    try:
        return render_template("diary2.html", sleep_data=sleep_data, wc=ordered_week_commencing, hours_data=hours_data,
                               efficiency_data=efficiency_data, mood_data=mood_data, sef_last=last_week_sef,
                               sef_this=this_week_sef)
    except Exception:
        return render_template("diary_warn.html")



@app.route("/add_gaps_2", methods=["GET", "POST"])

def add_gaps_2():
    gaps = 3
    if request.method == "GET":

        return render_template("add_gaps_2.html", gaps=gaps)
    else:
        data = request.get_json(force=True)
        print(data)
        return render_template("add_gaps_2.html", gaps=gaps)


@app.route("/diary2", methods=["GET"])
def diary2():
    if request.method == "GET":
        last_week_sef = 50.0
        this_week_sef = 62.0
        return render_template("diary2.html", sef_last=last_week_sef,
                               sef_this=this_week_sef)
    else:
        return render_template("diary2.html")

