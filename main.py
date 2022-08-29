from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from functools import wraps
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

#Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#init MYSQL
mysql = MySQL(app)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET'])
def contact():
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

        if result > 0:
            #get stored hash
            data = cur.fetchone()
            password = data['password']

            #compare Passwords
            if sha256_crypt.verify(password_user, password):
                #can log in
                session['logged_in'] = True
                session['id'] = data['id']

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'invalid password'
                return render_template('login.html', error=error)
                cur.close()
        else:
            error = 'No email found'
            return render_template('login.html', error=error)

    return render_template('login.html')


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

    #Get employee by id
    employee_data = cur.execute("SELECT * FROM employee WHERE id = %s", [session['id']])
    employee = cur.fetchone()
    status_data = cur.execute("SELECT * FROM status JOIN employee ON employee.id_status = status.id WHERE employee.id = %s", [session['id']])
    status = cur.fetchone()

    return render_template('dashboard.html', employee=employee, status=status)
    #close connection
    cur.close()

@app.route('/calendar', methods=['GET'])
@is_logged_in
def calendar():
    return render_template('calendar.html')


@app.route('/logout', methods=['GET'])
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


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
        cur.execute("UPDATE employee SET name=%s, email=%s, address=%s, phone=%s WHERE id=%s", (name, email, address, phone, session['id']))

        #Commit to db
        mysql.connection.commit()

        #close connection
        cur.close()

        flash('Peronnal information edited', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_info.html', form=form)


@app.route('/leave', methods=['GET', 'POST'])
@is_logged_in
def leave():
    return render_template('leave_form.html')

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
    result = cur.execute("SELECT * FROM employee WHERE id = %s", [session['id']])

    employee = cur.fetchone()

    #get form
    form = LinkForm(request.form)

    #populate employee from field
    form.website.data = employee['website']
    form.github.data = employee['github']
    form.twitter.data = employee['twitter']
    form.facebook.data = employee['facebook']

    if request.method == 'POST' and form.validate():
        website = request.form['website']
        github = request.form['github']
        twitter = request.form['twitter']
        facebook = request.form['facebook']

        #Create cursor
        cur = mysql.connection.cursor()

        #execute
        cur.execute("UPDATE employee SET website=%s, github=%s, twitter=%s, facebook=%s WHERE id=%s", (website, github, twitter, facebook, session['id']))

        #Commit to db
        mysql.connection.commit()

        #close connection
        cur.close()

        flash('Peronnal links edited', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_links.html', form=form)


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


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        address = form.address.data
        phone = form.phone.data
        password = sha256_crypt.encrypt(str(form.password.data))

        #Create cursor
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO employee(name, email,address, phone, password, id_status) VALUES(%s, %s, %s,%s,%s, 2)", (name, email, address, phone, password))

        #commit to db
        mysql.connection.commit()

        #close the connection
        cur.close()

        flash("An employee with status was added and can log in", 'success')
        return redirect(url_for('add'))
    return render_template('add.html', form=form)


app.secret_key = 'mionja123'
app.run(debug=True)
