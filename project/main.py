from flask import Flask, render_template, request, url_for, redirect, g, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import os
import project.database as db
import project.validation as vd
from project.classes import Dog, Report

app = Flask(__name__)
app.config.from_mapping(DATABASE = os.path.join(app.instance_path, 'schema.sql'))
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # Limits image upload size to 8MB (1024 * 1024 = 1MB)
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'dev'


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if request.form["login_button"] == "login":
            try:
                user = db.execute_query("SELECT userID, email, password FROM user WHERE email = ?", (email,))[0]
                # Tries to find a user with given email

                if check_password_hash(user[2], password): # Evaluates hashed given password against hashed stored password
                    session.clear() # Refreshes session and redirects to user profile
                    session['userID'] = user[0]
                    return redirect(url_for('dogList'))
                else:
                    flash("Incorrect password")
            except:
                flash(f"User with email {email} not found")

    return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":

        # Data collection
        email = request.form["email"]
        telephoneNo = request.form["telephoneNo"]
        password = request.form["password"]
        confirmPassword = request.form["confirmPassword"]

        error = None
        if request.form["register_button"] == "register":
            empty = False
            if not email:
                flash('Email required', 'empty') # Unfilled fields flashed as errors to user
                empty = True
            if not telephoneNo:
                flash('Telephone number required', 'empty')
                empty = True
            if not password:
                flash('Password required', 'empty')
                empty = True
            if not confirmPassword:
                flash('Re-enter password', 'empty')
                empty = True

            # Validation only occurs if fields are filled
            if not empty:
                if not vd.validateEmail(email):
                    error = 'Invalid email'
                elif not vd.validateTel(telephoneNo):
                    error = 'Invalid telephone number'
                elif not vd.validatePassword(password):
                    error = 'Invalid password - password must contain one capital letter, one digit, and be between 8-32 characters'
                elif not vd.matchPasswords(password, confirmPassword):
                    error = 'Passwords do not match'

                if error is None:
                    db.execute_query("INSERT INTO user VALUES (NULL, ?, ?, ?)", (email, generate_password_hash(password), telephoneNo))
                    return render_template('auth/login.html')
                else:
                    flash(error, 'error')

    return render_template('auth/register.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'userID' in session:

        if request.method == "GET":
            report_ids = db.execute_query(f'SELECT reportID, userID, dogID FROM report ORDER BY reportID DESC LIMIT 20')
            # Gets the IDs of the 20 latest reports

            reports = []
            for ids in report_ids:

                telephoneNo = db.execute_query(f'SELECT telephoneNo FROM user WHERE userID=?', (ids[1],), 'single')[0]

                dog = db.execute_query(f'SELECT name, last_report, location FROM dog WHERE dogID=?', (ids[2],))[0]

                data = [ids[0], ids[1], ids[2], dog[0], dog[1], dog[2], telephoneNo]
                '''
                List of data items to be added to the report
                ids[0] = Report ID
                ids[1] = User ID
                ids[2] = Dog ID
                dog[0] = Dog name
                dog[1] = Dog last report date
                dog[2] = Dog location
                telephoneNo = User telephone number
                '''
                reports.append(Report(*(data)))  # data list unpacked to be passed into Report object

    else:  # User not granted access if not authorised/in session
        return render_template('error_401.html')

    return render_template('feed/home.html', reports=reports)


@app.route('/dogs', methods=['GET', 'POST'])
def dogList():
    title = "My Dogs"

    if 'userID' in session:
        dogs = []
        names = []
        dogs_query = db.execute_query('SELECT * FROM dog WHERE dog.userID=?', (session['userID'],))
        for data in dogs_query:
            dogs.append(Dog(*data)) # *data unpacks the tuple and passes values as positional arguments
            names.append(data[2])


    else:
        return render_template('error_401.html')

    return render_template('dogs/list.html', dogs=dogs, names=names)


@app.route('/report/<string:id>', methods=['GET', 'POST'])  # Dog ID is passed into function as parameter
def report(id):
    dogID = id
    is_lost = db.execute_query(f'SELECT lost FROM dog WHERE dogID=?', (dogID,), 'single')[0]
    if is_lost == 0: # Create new report is dog is not lost (lost = 0)

        # DATE COMPARISON
        last_report = db.execute_query(f'SELECT last_report FROM dog WHERE dogID=?', (dogID,), 'single')[0]
        if last_report == 'No report':
            pass
        else:
            last_report_date = datetime.datetime.strptime(last_report, "%Y-%m-%d") # Converts last report into a comparable datetime object
            present = datetime.datetime.now()
            delta = present.date() - last_report_date.date() # Determines number of days between last report and present day
            if delta.days < 7:
                flash(f'You must wait {delta.days} days before reporting your dog as missing again')
                return redirect(url_for('dogList'))

        userID = session['userID']
        name, location = db.execute_query(f'SELECT name, location FROM dog WHERE dogID=?', (dogID,), 'multi')[0]
        date = datetime.date.today()
        db.execute_query(f'INSERT INTO report VALUES (NULL, ?, ?, ?, ?, ?)', (userID, dogID, name, date, location))
        db.execute_query(f'UPDATE dog SET lost = ?, last_report = ? WHERE dogID == ?', (1, date, dogID))

    else: # Revert changes if dog is lost (lost = 1)
        db.execute_query(f'UPDATE dog SET lost = ? WHERE dogID == ?', (0, dogID))
        db.execute_query(f'DELETE FROM report WHERE dogID=?', (dogID))

    return redirect(url_for('dogList'))


@app.route('/edit', methods=['GET', 'POST'])
def editDog():
    title = "Editing"

    if request.method == "GET":
        id = request.args.get('id')

        if 'userID' in session:
            userID = db.execute_query('SELECT userID FROM dog WHERE dog.dogID=?', (id,), 'single')[
                0]
            if userID != session['userID']:
                return render_template('error_401.html')

        else:
            return render_template('error_401.html')

        dog = db.execute_query('SELECT name, age, sex, breed, location FROM dog WHERE dogID=?', (id,))[0]
        # Query returns array so [0] gets item
        (name, age, sex, breed, location) = dog  # Retrieved values mapped to tuple

    if request.method == "POST":
        name = request.form['name_input']
        age = request.form['age_input']
        sex = request.form['sex_input']
        breed = request.form['breed_input']
        location = request.form['location_input']
        id = request.form['id_hidden']
        image = request.files['image_input']

        if request.form['button'] == 'delete':
            db.execute_query('DELETE FROM report WHERE dogID=?', (id,))
            # Deletes all reports for this dog - referential integrity

            db.execute_query('DELETE FROM dog WHERE dogID=?', (id,))
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{id}.png")  # Dog image removed
            os.remove(file_path)
            return redirect(url_for('dogList'))

        elif request.form['button'] == 'submit':
            error = None
            if not vd.validateName(name):
                error = 'Invalid name - must be between 1 and 20 characters'
                flash(error)
            if not vd.validateAge(age):
                error = 'Invalid age - please enter a number'
                flash(error)
            if not vd.validateBreed(breed):
                error = 'Invalid breed - must be between 1 and 50 characters'
                flash(error)

            if error is None:
                db.execute_query('UPDATE dog SET name=?, age=?, sex=?, breed=?, location=? WHERE dogID=?', (name, age, sex, breed, location, id))
                if image:
                    image.filename = id + '.png' # Renames uploaded file to be the ID of this dog
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))

                return redirect(url_for('dogList'))

    return render_template('dogs/edit.html', id=id, name=name, age=age, sex=sex, breed=breed, location=location)


@app.route('/create', methods=['GET', 'POST'])
def createDog():
    title = "Creating"

    if request.method == "POST":
        name = request.form['name_input']
        age = request.form['age_input']
        sex = request.form['sex_input']
        breed = request.form['breed_input']
        location = request.form['location_input']
        image = request.files['image_input']


        if request.form['submit_button'] == 'submit':
            error = None
            if not vd.validateName(name):
                error = 'Invalid name - must be between 1 and 20 characters'
                flash(error)
            if not vd.validateBreed(breed):
                error = 'Invalid breed - must be between 1 and 50 characters'
                flash(error)
            if not vd.validateAge(age):
                error = 'Invalid age - please enter a number'
                flash(error)
            if image.filename == '':
                error = 'You must upload an image of your dog of type PNG or JPG, no more than 8MB'
                flash(error)

            if error is None:
                db.execute_query('INSERT INTO dog VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)', (session['userID'], name, age, sex, breed, 0, 'No report', location))
                id = db.execute_query('SELECT dogID FROM dog ORDER BY dogID DESC LIMIT 1', None, 'single')[0]
                image.filename = str(id) + '.png'  # Renames uploaded file to be the ID of this dog
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
                return redirect(url_for('dogList'))

    return render_template('dogs/create.html')


if __name__ == '__main__':
    app.run(debug = True)