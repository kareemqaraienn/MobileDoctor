from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import login_required, LoginManager, UserMixin, login_user, logout_user, current_user
from sqlalchemy.ext.automap import automap_base
from flask_sqlalchemy import SQLAlchemy
from main import predict_input, get_disease_info, dictionary_of_symptoms
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
import json
import pytz





app = Flask(__name__, static_folder='frontend', template_folder='frontend')


app.config['SECRET_KEY'] = 'mysecretkey' # Set a secret key here
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin123@mobiledoc.cy4cb9lerqy0.us-east-1.rds.amazonaws.com/main'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)



Base = automap_base()
with app.app_context():
    Base.prepare(db.engine, reflect=True)

# Check the mapped classes
# print("Mapped classes:", Base.classes.keys())

# Directly use the automapped class
User = Base.classes.User
UserInfo = Base.classes.UserInfo
Predictions = Base.classes.PredictionSessions
SymptomInPredictions = Base.classes.SymptomsInPredictions


#print each column name in each table
# for table in Base.classes:
#     print(table)
#     for column in table.__table__.columns:
#         print(column.name)

class UserWrapper(UserMixin):
    def __init__(self, user):
        self.user = user

    # Delegate the properties and methods to the underlying user object
    @property
    def id(self):
        # Use 'userId' as the primary key
        return self.user.userId

    # Implement get_id method
    def get_id(self):
        return str(self.id)



# User loader function
@login_manager.user_loader
def load_user(user_id):
    user = db.session.query(User).get(user_id)
    return UserWrapper(user) if user else None


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # check if user clicked on login or register
        if request.form['submit_button'] == 'Login':
            return redirect(url_for('login'))
        elif request.form['submit_button'] == 'Register':
            return redirect(url_for('register'))
    if current_user.is_authenticated:
        return render_template('dashboard.html', user=current_user)
    else:
        return render_template('homepage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # check if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        # get data from request
        data = request.get_json()
        
        # get email
        email = data.get('email')
        
        # get password
        password = data.get('password')
        
        # Use SQLAlchemy's querying API
        Session = sessionmaker(bind=db.engine)
        session = Session()

        # query the database to find user with matching email
        user = session.query(User).filter_by(email=email).first()

        # check if user exists and password is correct
        if user and check_password_hash(user.password, password):
            # log the user in
            login_user(UserWrapper(user), remember=True)
            # Optionally, you can create a session or token here.
            # For example:
            # session['user_id'] = user.userId
            return jsonify({'message': 'Login successful'})
        else:
            # return error message
            return jsonify({'message': 'Invalid credentials'})
    return render_template('login.html', user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # check if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('predict'))
    if request.method == 'POST':
        # get data from request
        data = request.get_json()
        print(data)
        
        # get user information
        email = data['email']
        password = data['password']
        password_confirmation = data['password_confirmation']
        first_name = data['first_name']
        last_name = data['last_name']
        age = data['age']

        # check if password and password confirmation match
        if password != password_confirmation:
            # return error message with status code
            return jsonify({'message': 'Passwords do not match'}), 400

        # check if user exists in db
        existing_user = db.session.query(User).filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'User already exists'}), 409
        

        # insert the new user into the user table
        new_user = User(email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.flush()

        # insert the user's additional info into the userInfo table
        new_user_info = UserInfo(
            userId=new_user.userId,
            firstName=first_name,
            lastName=last_name,
            age=age,
            createdOn=db.func.current_date()
        )
        db.session.add(new_user_info)
        
        # commit the changes
        db.session.commit()
        login_user(UserWrapper(new_user), remember=True)

        return jsonify({'message': 'Registration successful'}), 201
    return render_template('register.html', user=current_user)




@app.route('/predict', methods=['POST', 'GET'])
@login_required
def predict():
    if request.method == 'POST':
        return handle_prediction_request()
    else:
        return render_prediction_form()

@app.route('/predict/<predictId>/results')
@login_required
def display_results(predictId):
    prediction = db.session.query(Predictions).get(predictId)
    if prediction:
        info = get_prediction_info(prediction)
        print(int(prediction.probability))
        return render_template('Results.html', disease=prediction.predictedDisease, info=info, probability=prediction.probability/100, user=current_user)
    else:
        # Handle invalid predictId
        return render_template('error.html', message='Invalid prediction ID')
    
    
@app.route('/history/<user_id>')
@login_required
def history(user_id):
    if user_id != str(current_user.id):
        return redirect(url_for('history', user_id=current_user.id))
    Session = sessionmaker(bind=db.engine)
    session = Session()
    PredictionSessions = Base.classes.PredictionSessions
    SymptomsInPredictions = Base.classes.SymptomsInPredictions

    # Fetch predictions and their associated symptoms from the database
    predictions = (
        session.query(PredictionSessions, SymptomsInPredictions)
        .join(SymptomsInPredictions, PredictionSessions.predictionId == SymptomsInPredictions.predictionId)
        .filter(PredictionSessions.userId == user_id)
        .all()
    )

    # Create a list to hold the predictions and associated information
    history_data = []
    for prediction, symptom in predictions:
        prediction_id = prediction.predictionId
        disease_name = prediction.predictedDisease
        symptom_name = symptom.symptom.replace('_', ' ').capitalize()
        created_on = prediction.createdOn

        # Check if the disease entry already exists in history_data
        disease_entry = next((d for d in history_data if d['predictionId'] == prediction_id), None)
        if disease_entry:
            # Append the symptom to the existing disease's symptoms
            disease_entry['symptoms'].append(symptom_name)
        else:
            # Assume currentDate is the datetime in UTC
            # Make the currentDate timezone aware
            currentDate = pytz.utc.localize(created_on)

            # Convert to Eastern Time
            date = currentDate.astimezone(pytz.timezone('US/Eastern'))
            # Create a new disease entry
            disease_entry = {
                'predictionId': prediction_id,
                'name': disease_name,
                'symptoms': [symptom_name],
                'created_on': date
            }
            history_data.append(disease_entry)
    # sort the history data by created_on
    history_data.sort(key=lambda x: x['created_on'], reverse=True)
    # Render the history template and pass the history data to it
    return render_template('history.html', history_data=history_data)



@app.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user using Flask-Login
    return redirect(url_for('login'))

# Define the route to handle the API call for deleting a prediction
@app.route('/api/predictions/delete', methods=['POST'])
def delete_prediction():
    # Get the prediction name from the request body
    predictionId = request.json['predictionId']
    print(predictionId)
    # Delete the prediction from the database
    Session = sessionmaker(bind=db.engine)
    session = Session()
    session.query(SymptomInPredictions).filter(SymptomInPredictions.predictionId == predictionId).delete()

    session.query(Predictions).filter(Predictions.predictionId == predictionId).delete()
    session.commit()
    session.close()

    # Return a success response
    return jsonify({'success': True})

def handle_prediction_request():
    symptoms = request.form.getlist('symptoms[]')
    predicted_disease, probability = predict_input(symptoms)
    prediction = save_prediction_info(predicted_disease, probability)
    save_symptoms_in_prediction(symptoms, prediction)
    return redirect(url_for('display_results', predictId=prediction.predictionId))

def render_prediction_form():
    return render_template('MD.html', user=current_user, symptoms_dict=dictionary_of_symptoms)

def collect_symptoms(form_data):
    symptoms = []
    for key, value in form_data.items():
        if key.startswith('dropdown'):
            symptoms.append(value)
    return symptoms


def save_prediction_info(predicted_disease, probability):
    new_session = Predictions(userId=current_user.id, predictedDisease=predicted_disease, probability=probability)
    db.session.add(new_session)
    db.session.commit()
    return new_session

def save_symptoms_in_prediction(symptoms, prediction):
    for symptom in symptoms:
        new_symptom_in_prediction = SymptomInPredictions(predictionId=prediction.predictionId, symptom=symptom)
        db.session.add(new_symptom_in_prediction)
    db.session.commit()

def get_prediction_info(prediction):
    symptom_in_prediction = db.session.query(SymptomInPredictions).filter_by(predictionId=prediction.predictionId).all()
    symptoms = [symptom.symptom for symptom in symptom_in_prediction]
    info_json = get_disease_info(prediction.predictedDisease, symptoms)
    info = json.loads(info_json)

    # Modify and process info as needed
    for symptom, severity in info['symptom_severity'].items():
        severity_percentage = (severity / 7) * 100
        severity_color = get_severity_color(severity)
        style_string = f'width: {severity_percentage}%; background-color: {severity_color};'
        info['symptom_severity'][symptom] = {'severity': severity, 'percentage': severity_percentage, 'color': severity_color, 'style': style_string}

    info['symptom_severity'] = {k.replace('_', ' '): v for k, v in sorted(info['symptom_severity'].items(), key=lambda item: item[1]['percentage'], reverse=True)}

    return info


def get_severity_color(severity):
    if severity <= 3:
        return 'green'
    elif severity <= 5:
        return 'orange'
    else:
        return 'red'

    


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')



