###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
import requests
import json 
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required, Length # Here, too
from flask_sqlalchemy import SQLAlchemy
import weather_api

## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True

## All app.config values
app.config["SECRET_KEY"] = "stringhardtoguess"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/SBABTIWA364midterm"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
## Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)


######################################
######## HELPER FXNS (If any) ########
######################################
def get_or_create_city(db_session, city, state):
    city_obj = db_session.query(City).filter_by(cityname=city, citystate=state).first()
    if city_obj:
        return city_obj
    else:
        city_obj = City(cityname=city, citystate=state)
        db_session.add(city_obj)
        db_session.commit()
        return city_obj


def create_or_update_forecast(db_session, cityid, date, high_temp, low_temp):
    forecast = db_session.query(Forecast).filter_by(city_id = cityid, forecast_date = date).all()
    print (forecast)
    if forecast:
        row_count = db_session.query(Forecast).filter_by(city_id = cityid).filter_by(forecast_date = date).delete()
        db_session.commit()
        print ("Forecast rows deleted " + str(row_count))

    new_forecast = Forecast(forecast_date = date, 
                            forecast_high_temperature = high_temp,
                            forecast_low_temperature = low_temp,
                            city_id = cityid)
    db_session.add(new_forecast)
    db_session.commit()
    print ("Forecast row added for " + str(cityid) + " Date " + str(date))


##################
##### MODELS #####
##################


class City(db.Model): 
    __tablename__ = "cities"
    cityid = db.Column(db.Integer, primary_key = True)
    cityname = db.Column(db.String())
    citystate = db.Column(db.String())
    city_forecast = db.relationship('Forecast', backref = 'cities', lazy = True)

class Forecast(db.Model): 
    __tablename__ = "forecast"
    forecastid = db.Column(db.Integer, primary_key = True)
    forecast_date = db.Column(db.String()) 
    forecast_high_temperature = db.Column(db.Float())
    forecast_low_temperature = db.Column(db.Float())
    city_id = db.Column(db.Integer, db.ForeignKey('cities.cityid'))


###################
###### FORMS ######
###################


class CityForm(FlaskForm):
    city = StringField("Please enter name of the US city : ",validators=[Required()])
    state = StringField("State (abbreviated - MI, NY, etc.) : ",validators =[Required()])
    submit = SubmitField()
    
    def validate_state(form,field):
        if len(field.data) > 2:
            raise ValidationError("The state name must be abbreviated to two letters (MI = Michigan, for example). Please try again.")


class StateForm(FlaskForm):
    enter_state= StringField("Please enter the abbreviation of a state (CA,IL,etc.) to see its saved cities : ",validators = [Required()])
    submit = SubmitField()



#######################
###### VIEW FXNS ######
#######################

@app.errorhandler(404)
def not_found(e):
    return render_template('404error.html'), 404

@app.route('/')
def home(): 
    return render_template("base.html")

@app.route('/city')
def city_form_display():
    cityform = CityForm()
    return render_template('index.html', form = cityform )

@app.route('/cities')
def all_cities():
    all_cities_entered = City.query.all()
    return render_template('all_cities.html',cities=all_cities_entered)

@app.route("/city", methods = ['GET', 'POST'])

def city_result():

    forecast_list = []
    city_response = CityForm(request.form)
    city_name = ""
    if request.method == "POST" and city_response.validate_on_submit():
        city_name = city_response.city.data
        city_words = city_name.split()
        print(city_name)
        num_of_words = len(city_name.split())
        concat_city_name = ""

        if len(city_words) == 2:
            concat_city_name = city_words[0] + "_" + city_words[1]
        else:
            concat_city_name = city_words[0]
        
        state_name = city_response.state.data

        print (concat_city_name + " " + state_name)

        city_request = requests.get("http://api.wunderground.com/api/{}/forecast/q/{}/{}.json".format(weather_api.api_key,state_name,concat_city_name))

        print(city_request)
        json_text = json.loads(city_request.text)

        print(json_text)
        
        try:
            forecast = json_text["forecast"]
        except KeyError:
            flash("FORM SUBMISSION ERROR - " + "Invalid Input")
            return render_template("forecastresults.html")

        for each_forecast in json_text["forecast"]["simpleforecast"]["forecastday"]:
            forecast_results = (each_forecast["date"]["weekday"],each_forecast["high"]["fahrenheit"], each_forecast["low"]["fahrenheit"])
            forecast_list.append(forecast_results)
            cityid = get_or_create_city(db.session, city_name, state_name).cityid

            current_forecasts = db.session.query(Forecast).filter_by(city_id = cityid).all()
            print (current_forecasts)
            create_or_update_forecast(  db.session, 
                                        cityid, 
                                        each_forecast["date"]["weekday"],
                                        each_forecast["high"]["fahrenheit"],
                                        each_forecast["low"]["fahrenheit"])


        print(forecast_list)

    errors = [e for e in city_response.errors.values()]
    if len(errors) > 0:
        flash("FORM SUBMISSION ERROR - " + str(errors))
    return render_template("forecastresults.html", cityname = city_name, forecast = forecast_list)


@app.route('/state_search')
def state_form():
    state_form = StateForm()
    return render_template('state.html', form=state_form)

@app.route("/state_result", methods = ['GET','POST'])
def state_results():
    state_response = StateForm()

    # print ("POST enter_state = " + str(request.form.get("enter_state")))
    # print ("GET enter_state = " + str(request.args.get("enter_state")))
    # print ("VAUES enter_state = " + str(request.values.get("enter_state")))

    if request.args:

        state_name = str(request.args.get("enter_state"))
        if len(state_name) > 2:
             flash("FORM SUBMISSION ERROR - Invalid Input")
             return redirect(url_for('state_form'))

        cities_list = City.query.filter_by(citystate = state_name).all()
        print(cities_list)
    
        return render_template('stateresults.html', state_name = state_name, cities = cities_list)

    
    return redirect(url_for('state_form'))



## Code to run the application...

# Put the code to do so here!
if __name__ == '__main__':
    db.create_all() 
    app.run(use_reloader=True,debug=True)

# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
