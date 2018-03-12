<h1> ** SI 364 Midterm Winter 2018 ** </h1>
<h2> ** Name: ** Sanika Babtiwale </h2>

<h3> ** Project Description: ** This application utilizes an API called Weather Underground (https://www.wunderground.com/weather/api/) to find weather information for U.S. cities. It provides a 3-day forecast, allows a user to search for cities they have saved under a particular state, and view a general list of all the cities they have entered in the database so far. </h3> 

<h4> ** List of Existing Routes with Template Names ** </h4>

* http://localhost:5000/ -> base.html 
* http://localhost:5000/city -> index.html 
* http://localhost:5000/city -> forecastresults.html 
* http://localhost:5000/cities -> all_cities.html
* http://localhost:5000/state_search -> state.html
* http://localhost:5000/state_result -> stateresults.html
* http://localhost:5000/404 -> 404error.html



<h4> ** Code Requirements ** </h4>

<h6> ** Ensure that the SI364midterm.py file has all the setup (app.config values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on http://localhost:5000 (and the other routes you set up) ** </h6>
<h6> ** Add navigation in base.html with links (using a href tags) that lead to every other viewable page in the application. (e.g. in the lecture examples from the Feb 9 lecture, like this ) ** </h6>
<h6> ** Ensure that all templates in the application inherit (using template inheritance, with extends) from base.html and include at least one additional block. ** </h6>
 <h6> ** Include at least 2 additional template .html files we did not provide. ** </h6>
<h6> ** At least one additional template with a Jinja template for loop and at least one additional template with a Jinja template conditional.
These could be in the same template, and could be 1 of the 2 additional template files. ** </h6>
<h6> ** At least one errorhandler for a 404 error and a corresponding template. ** </h6>
<h6> ** At least one request to a REST API that is based on data submitted in a WTForm. ** </h6>
<h6> ** At least one additional (not provided) WTForm that sends data with a GET request to a new page. ** </h6>
<h6> ** At least one additional (not provided) WTForm that sends data with a POST request to the same page. ** </h6>
<h6> ** At least one custom validator for a field in a WTForm. ** </h6>
<h6> ** At least 2 additional model classes. ** </h6>
<h6> ** Have a one:many relationship that works properly built between 2 of your models. ** </h6>
<h6> ** Successfully save data to each table. ** </h6>
<h6> ** Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for). ** </h6>
<h6> ** Query data using an .all() method in at least one view function and send the results of that query to a template. ** </h6>
<h6> ** Include at least one use of redirect. (HINT: This should probably happen in the view function where data is posted...) ** </h6>
<h6> ** Include at least one use of url_for. (HINT: This could happen where you render a form...) ** </h6>
<h6> ** Have at least 3 view functions that are not included with the code we have provided. (But you may have more! Make sure you include ALL view functions in the app in the documentation and ALL pages in the app in the navigation links of base.html.) ** </h6>

<h4> ** Additional Requirements ** </h4>

<h6> (100 points) Include an additional model class (to make at least 4 total in the application) with at least 3 columns. Save data to it AND query data from it; use the data you query in a view-function, and as a result of querying that data, something should show up in a view. (The data itself should show up, OR the result of a request made with the data should show up.) <h6>
<h6> ** (100 points) Write code in your Python file that will allow a user to submit duplicate data to a form, but will not save duplicate data (like the same user should not be able to submit the exact same tweet text for HW3). ** </h6>
