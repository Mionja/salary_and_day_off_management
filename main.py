import os

from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from functools import wraps

from werkzeug.utils import secure_filename
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from datetime import datetime

app = Flask(__name__)

#Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#init MYSQL
mysql = MySQL(app)


#-----------------------------------------For any user----------------------------------------
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        #Create cursor
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO notifications(name, email,subject, message) "
                    "VALUES(%s, %s, %s,%s)", (name, email, subject, message))

        #commit to db
        mysql.connection.commit()

        #close the connection
        cur.close()

        flash("Thank you for contacting us, your message has been received", 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Get FORM fields
        login = request.form['login']
        password_user = request.form['pswd']

        #Create cursor
        cur = mysql.connection.cursor()

        #Get user by EMAIL(login)
        result = cur.execute("SELECT * FROM employee WHERE email=%s", [login])

        # Data admin
        email_admin = 'mionja@gmail.com'
        pass_admin = '123'

        if result > 0:
            #get stored hash
            data = cur.fetchone()
            password = data['password']

            #compare Passwords
            if sha256_crypt.verify(password_user, password):
                session.clear()
                #can log in
                session['logged_in'] = True
                session['id'] = data['id']

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'invalid password'
                return render_template('login.html', error=error)

        elif login == email_admin:
            # compare Passwords
            if password_user == pass_admin:
                session.clear()
                # can log in
                session['admin_logged'] = True

                flash('You are now logged in', 'success')
                return redirect(url_for('d'))
            else:
                error = 'invalid password'
                return render_template('login.html', error=error)
        else:
            error = 'No email found'
            return render_template('login.html', error=error)
        cur.close()
    return render_template('login.html')


#-----------------------------------------For employees only----------------------------------------
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized, Please login", 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/dashboard', methods=['GET'])
@is_logged_in
def dashboard():
    # Create cursor
    cur = mysql.connection.cursor()

    employee_data = cur.execute("""SELECT e.*, s.name AS s_name, s.salary AS s_salary, s.day_off AS s_day_off, s.cnaps,
                                      s.osti, s.irsa 
                                      FROM employee e 
                                      JOIN status s 
                                      ON e.id_status = s.id
                                      WHERE e.id = %s""", [session['id']])
    employee = cur.fetchone()

    day_off_data = cur.execute("SELECT d.* "
                               "FROM day_off d "
                               "JOIN employee e "
                               "ON d.id_employee = e.id WHERE e.id = %s", [session['id']])
    leaves = cur.fetchall()

    links = cur.execute("SELECT * FROM links WHERE id_employee=%s", [session['id']])
    links = cur.fetchone()

    t=0
    for leave in leaves:
        t += ((leave['end']-leave['start']).days)

    return render_template('employee/dashboard.html', employee=employee, leaves=leaves, n_leave=t, links=links)
    #close connection
    cur.close()


@app.route('/advance', methods=['GET', 'POST'])
@is_logged_in
def advance():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT e.*, s.* FROM employee e JOIN status s ON e.id_status = s.id WHERE e.id = %s;""",[session['id']])
    employee = cur.fetchone()

    if request.method == 'POST':
        advance = request.form['advance']
        if employee['advance']:
            _advance = employee['advance']
        else:
            _advance = 0

        if int(advance) < 0:
            flash('You cannot take an amount below 0', 'danger')
        elif int(advance) <= employee['salary'] - _advance:
            cur.execute("""UPDATE employee SET advance =advance + %s WHERE id = %s""", (advance, [session['id']]))
            # Commit to db
            mysql.connection.commit()

            # close connection
            cur.close()
            flash('Alright, {}$ will be shared to your account'.format(advance), 'success')
        else:
            flash('You cannot take an amount above your sold', 'danger')

    return render_template('employee/advance.html')


@app.route('/leave', methods=['GET', 'POST'])
@is_logged_in
def leave():
    if request.method == 'POST':
        #get curent time
        today = datetime.now()
        month = today.month
        year = today.year
        day = today.day

        #get form field
        start = request.form['start']
        end = request.form['end']
        reason = request.form['reason']

        if reason == "other":
            reason = request.form['o_reason']
            if reason == '':
                error = "Please fill the other reason field"
                return render_template('employee/leave_form.html', error=error)

        if end > start:
            input_year = int(start[0]+start[1]+start[2]+start[3])
            input_month = int(start[5]+start[6])
            input_day = int(start[8] + start[9])

            if input_year < year or input_month < month or input_day <= day:
                error = "Please insert a valid date"
                return render_template('employee/leave_form.html', error=error)

            # Create cursor
            cur = mysql.connection.cursor()

            id_employee = cur.execute("SELECT id_employee FROM day_off "
                                      " WHERE MONTH(start) LIKE MONTH(%s) AND YEAR(start) LIKE YEAR(%s) "
                                      " AND MONTH(end) LIKE MONTH(%s) AND YEAR(end) LIKE YEAR(%s) ",
                                      [start, start, end, end])
            start_end = cur.execute("SELECT * FROM day_off "
                                      " WHERE MONTH(start) LIKE MONTH(%s) AND YEAR(start) LIKE YEAR(%s) "
                                      " AND MONTH(end) LIKE MONTH(%s) AND YEAR(end) LIKE YEAR(%s) ",
                                      [start, start, end, end])
            if start_end['start'] == start and start_end['id_employee']==session['id']:
                error = "You've already taken that leave"
                return render_template('employee/leave_form.html', error=error)
            if id_employee < 6:
                #Add everything in the table day_off
                cur.execute("INSERT INTO day_off(start, end, reason, id_employee) "
                            "VALUES(%s, %s, %s, %s)", (start, end, reason, session['id']))

                # commit to db
                mysql.connection.commit()

                # close the connection
                cur.close()
                flash('From {} to {}, you will be taking your leave'.format(start, end), 'success')
                return redirect(url_for('accept'))
            else:
                return render_template('employee/decline.html')
        else:
            error = "The start date can't be greater than the end date"
            return render_template('employee/leave_form.html', error=error)
    return render_template('employee/leave_form.html')


@app.route('/accept', methods=['GET', 'POST'])
@is_logged_in
def accept():
    return render_template('employee/accept.html')


class LinkForm(Form):
    website = StringField('Website', [validators.Length(min=5)])
    github = StringField('github', [validators.Length(min=5)])
    twitter = StringField('twitter', [validators.Length(min=5)])
    facebook = StringField('facebook', [validators.Length(min=5)])


@app.route('/edit_links', methods=['GET', 'POST'])
@is_logged_in
def edit_links():
    #Create cursor
    cur = mysql.connection.cursor()

    #get employee by id
    result = cur.execute("SELECT * FROM links WHERE id_employee = %s", [session['id']])

    employee = cur.fetchone()

    #get form
    form = LinkForm(request.form)

    #populate employee from field
    if employee:
        form.website.data = employee['website']
        form.github.data = employee['github']
        form.twitter.data = employee['twitter']
        form.facebook.data = employee['facebook']
    else:
        pass

    if request.method == 'POST' and form.validate():
        website = request.form['website']
        github = request.form['github']
        twitter = request.form['twitter']
        facebook = request.form['facebook']

        #Create cursor
        cur = mysql.connection.cursor()

        #execute
        if employee:
            cur.execute("UPDATE links SET website=%s, github=%s, twitter=%s, facebook=%s "
                         "WHERE id_employee=%s", (website, github, twitter, facebook, session['id']))
        else:
            cur.execute("INSERT INTO links(website,github, twitter, facebook, id_employee)"
                        "VALUES (%s,%s,%s,%s,%s)",
                        (website, github, twitter, facebook, session['id']))
        #Commit to db
        mysql.connection.commit()

        #close connection
        cur.close()

        flash('Peronnal links edited', 'success')
        return redirect(url_for('dashboard'))
    return render_template('employee/edit_links.html', form=form)


@app.route('/edit_photo', methods=['GET', 'POST'])
@is_logged_in
def edit_photo():
    #Create cursor
    cur = mysql.connection.cursor()
    # get employee by id
    result = cur.execute("SELECT * FROM employee WHERE id = %s", [session['id']])

    employee = cur.fetchone()

    if request.method == 'POST':
        file = request.files["photo"]
        if file:
            photo = secure_filename(file.filename)
            file.save('static/uploads/' + photo)
            # execute
            try:
                os.remove('static/uploads/{}'.format(employee['photo']))
            except:
                pass
            cur.execute("UPDATE employee "
                        "SET photo=%s "
                        "WHERE id=%s", (photo, session['id']))
        #Commit to db
        mysql.connection.commit()

        #close connection
        cur.close()

        flash('Photo edited', 'success')
        return redirect(url_for('dashboard'))
    return render_template('employee/edit_photo.html', employee=employee)


class InfoForm(Form):
    name = StringField('Name', [validators.Length(min=3, max=50)])
    email = StringField('Email', [validators.Length(min=5, max=50)])
    address = StringField('Address', [validators.Length(min=10, max=150)])
    phone = StringField('Phone', [validators.Length(min=10, max=20)])


@app.route('/edit_info', methods=['GET', 'POST'])
@is_logged_in
def edit_info():
    #Create cursor
    cur = mysql.connection.cursor()

    #get employee by id
    result = cur.execute("SELECT * FROM employee WHERE id = %s", [session['id']])

    employee = cur.fetchone()

    #get form
    form = InfoForm(request.form)

    #populate employee from field
    form.name.data = employee['name']
    form.email.data = employee['email']
    form.address.data = employee['address']
    form.phone.data = employee['phone']

    if request.method == 'POST' and form.validate():
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        phone = request.form['phone']
        #Create cursor
        cur = mysql.connection.cursor()

        #execute
        cur.execute("UPDATE employee "
                    "SET name=%s, email=%s, address=%s, phone=%s "
                    "WHERE id=%s", (name, email, address, phone, session['id']))

        #Commit to db
        mysql.connection.commit()

        #close connection
        cur.close()

        flash('Peronnal information edited', 'success')
        return redirect(url_for('dashboard'))
    return render_template('employee/edit_info.html', form=form)


@app.route('/logout', methods=['GET'])
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


#-----------------------------------------For admin only----------------------------------------
def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged' in session:
            return f(*args, **kwargs)
        else:
            flash("Only the admin can access to the requested page, Please login", 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/admin/dashboard', methods=['GET'])
@is_admin
def d():
    return render_template('admin/dashboard.html')


@app.route('/admin/list_employee', methods=['GET'])
@is_admin
def get_list_employee():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get employee by id
    cur.execute("SELECT e.*,s.name AS st_name  "
                "FROM employee e JOIN status s ON e.id_status=s.id ")
    employees = cur.fetchall()

    return render_template('admin/list_employee.html', employees=employees)
    cur.close()


@app.route('/admin/detail_employee', methods= ['POST'])
@is_admin
def get_detail_employee():
    #get hidden input id
    id = request.form['id']

    # Create cursor
    cur = mysql.connection.cursor()

    # Get employee by id
    employee_data = cur.execute("""SELECT e.*, s.name AS s_name, s.salary AS s_salary, s.day_off AS s_day_off, s.cnaps,
                                          s.osti, s.irsa 
                                          FROM employee e 
                                          JOIN status s 
                                          ON e.id_status = s.id
                                          WHERE e.id = %s""", [id])
    employee = cur.fetchone()

    day_off_data = cur.execute("SELECT d.* "
                               "FROM day_off d "
                               "JOIN employee e "
                               "ON d.id_employee = e.id "
                               "WHERE e.id = %s", [id])
    leaves = cur.fetchall()

    t = 0
    for leave in leaves:
        t += ((leave['end'] - leave['start']).days)

    return render_template('admin/detail_employee.html', employee=employee, leaves=leaves, n_leave=t)
    # close connection
    cur.close()


@app.route('/admin/list_leave', methods=['GET', 'POST'])
@is_admin
def get_list_leave_appliances():
    # Create cursor
    cur = mysql.connection.cursor()

    Months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    if request.method == 'POST':
        searched_month = request.form['month']

        if searched_month != 'all' and searched_month != '':
            # Get employees and their leave appliances  of a given month
            cur.execute("SELECT e.name, d.* "
                        "FROM employee e JOIN day_off d ON e.id = d.id_employee "
                        "WHERE MONTH(d.start)=%s AND YEAR(d.start) LIKE YEAR(NOW()) "
                        "AND MONTH(d.end)=%s AND YEAR(d.end) LIKE YEAR(NOW()) ",
                        [searched_month, searched_month])
            employees = cur.fetchall()
            month = Months[int(searched_month) -1]
        else:
            cur.execute("SELECT e.name, d.* "
                        "FROM employee e JOIN day_off d ON e.id = d.id_employee "
                        "WHERE YEAR(d.start) LIKE YEAR(NOW()) "
                        "AND YEAR(d.end) LIKE YEAR(NOW()) ")
            employees = cur.fetchall()
            month = 'all in 2022'
    else:
        # Get employees and their leave appliances of the current month by id
        cur.execute("SELECT e.name AS name, d.* "
                    "FROM employee e JOIN day_off d ON e.id = d.id_employee "
                    "WHERE MONTH(d.start) LIKE MONTH(NOW()) AND YEAR(d.start) LIKE YEAR(NOW()) "
                    "AND MONTH(d.end) LIKE MONTH(NOW()) AND YEAR(d.end) LIKE YEAR(NOW()) ")
        employees = cur.fetchall()
        month = 'this month'

    return render_template('admin/list_leave_appliance.html', employees=employees, month=month)
    cur.close()


@app.route('/admin/notifications', methods=['GET', 'POST'])
@is_admin
def get_notifications():
    # Create cursor
    cur = mysql.connection.cursor()

    # if request.method == 'POST':
    #     #from search field
    #     email = request.form['email']
    #
    #     cur.execute("SELECT * FROM notifications WHERE email LIKE %%s% ", email)
    #     notifications = cur.fetchall()
    # else:
    # Get employee by id
    cur.execute("SELECT * FROM notifications ")
    notifications = cur.fetchall()

    return render_template('admin/notif.html', notifications=notifications)
    cur.close()


class AddForm(Form):
    name = StringField('Name', [validators.Length(min=3, max=100)])
    email = StringField('Email', [validators.Length(min=5, max=50)])
    address = StringField('Address', [validators.Length(min=10, max=150)])
    phone = StringField('Phone', [validators.Length(min=10, max=20)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/admin/add_employee', methods=['GET', 'POST'])
@is_admin
def add_employee():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get employee by id
    cur.execute("SELECT id, name FROM status")
    status = cur.fetchall()

    form = AddForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        address = form.address.data
        phone = form.phone.data
        id_status = request.form['id_status']
        password = sha256_crypt.encrypt(str(form.password.data))

        #Create cursor
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO employee(name, email,address, phone, password, id_status) "
                    "VALUES(%s, %s, %s,%s,%s, %s)", (name, email, address, phone, password, id_status))

        #commit to db
        mysql.connection.commit()

        #close the connection
        cur.close()

        flash("An employee was added and can log in", 'success')
        return redirect(url_for('get_list_employee'))
    return render_template('admin/add.html', form=form, status=status)


@app.route('/admin/logout', methods=['GET'])
@is_admin
def logout_admin():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


app.secret_key = 'mionja123'
app.run(debug=True)
