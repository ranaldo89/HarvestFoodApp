from flask import Flask

from flask import Flask, render_template, request, flash, redirect, session, jsonify, url_for,send_from_directory
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Recipe, Plan, PlanRecipe
from forms import NewMeals
from model import Meals
from sqlalchemy import desc
import requests
import random
import ast,os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/search"



headers = {
    'x-rapidapi-key': "35de92b7f2msh28ee39b7a390ebbp1a6502jsnb110a480cfdc",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

mock_results = [{
        "id": 479101,
        "url": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
        "image": "https://spoonacular.com/recipeImages/thai-sweet-potato-veggie-burgers-with-spicy-peanut-sauce-262682.jpg?size=200",
        "title": "Thai Sweet Potato Veggie Burgers ",
        "readyInMinutes": 20,
        "nutrition": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]
    }, {
        "id": 479101,
        "url": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
        "image": "https://spoonacular.com/recipeImages/seared-chicken-with-avocado-196932.jpg?size=200",
        "title": "Seared Chicken with Avocado                      ",
        "readyInMinutes": 20,
        "nutrition": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]
    }, {
        "id": 479101,
        "url": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
        "image": "https://spoonacular.com/recipeImages/browned-butter-and-lemon-brussels-sprouts-707586.jpg?size=200",
        "title": "Southwestern Chicken Salad                      ",
        "readyInMinutes": 20,
        "nutrition": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]
    }, {
        "id": 212401,
        "url": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
        "image": "https://spoonacular.com/recipeImages/Butternut-squash-salad-212401.jpg?size=200",
        "title": "Butternut squash salad",
        "readyInMinutes": 65,
        "nutrition": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]
    }, {
        "id": 479101,
        "url": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
        "image": "https://spoonacular.com/recipeImages/california-quinoa-avocado-salad-958131.jpg?size=200",
        "title": "California quinoa & avocado salad",
        "readyInMinutes": 40,
        "nutrition": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]
    }, {
        "id": 479101,
        "url": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
        "image": "https://spoonacular.com/recipeImages/spinach-avocado-and-marinated-tofu-salad-905643.jpg?size=200",
        "title": "On the Job: Pan Roasted Cauliflower From Food52",
        "readyInMinutes": 125,
        "nutrition": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]
    }, {
        "id": 479101,
        "url": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
        "image": "https://spoonacular.com/recipeImages/southwestern-butternut-squash-salad-1141526.jpg?size=200",
        "title": "Southwestern Butternut Squash Salad",
        "readyInMinutes": 50,
        "nutrition": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]
    }, {
        "id": 479101,
        "url": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
        "image": "https://spoonacular.com/recipeImages/grilled_pork_tenderloin_with_chimichurri_and_summer_veggies-82069.jpg?size=200",
        "title": "Grill Pork Tenderloin With Chimichurri and Summer Veggies",
        "readyInMinutes": 20,
        "nutrition": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]
    }, {
        "id": 479101,
        "url": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
        "image": "https://spoonacular.com/recipeImages/easy-peanut-noodles-1575205.jpg?size=200",
        "title": "Easy Peanut Noodles",
        "readyInMinutes": 35,
        "nutrition": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]
    }, {
        "id": 479101,
        "url": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
        "image": "https://spoonacular.com/recipeImages/gluten-free-baked-feta-pasta-the-tiktok-sensation-1622281.jpg?size=200",
        "title": "Gluten Free Baked Feta Pasta – The TikTok Sensation",
        "readyInMinutes": 20,
        "nutrition": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]
    }, {
        "id": 479101,
        "url": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
        "image": "https://spoonacular.com/recipeImages/Herb-Crusted-Beef-Tenderloin-175785.jpg",
        "title": "Herb Crusted Beef Tenderloin",
        "readyInMinutes": 20,
        "nutrition": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]
    }, {
        "id": 479101,
        "url": "http://feedmephoebe.com/2013/11/job-food52s-pan-roasted-cauliflower/",
        "image": "https://spoonacular.com/recipeImages/Lamb-Shank-Stew-with-Root-Vegetables-247018.jpg?size=200",
        "title": "Lamb Shank Stew with Root Vegetables",
        "readyInMinutes": 60,
        "nutrition": [{0: "blah"}, {"title": "Fat", "percentOfDailyNeeds": 40.32}, {0: "blah"}, {"title": "Carbohydrates", "percentOfDailyNeeds": 8.78}, {0: "blah"}, {0: "blah"}, {0: "blah"}, {"title": "Protein", "percentOfDailyNeeds": 14.42}]
    }
    ]

define_status = {
    "created": 1,
    "processed": 35,
    "dispatched":65,
    "delivered":100
}

app = Flask(__name__)
app.secret_key = "A big secret"

@app.route('/')
def index():
    """Homepage."""

    # if session != {}:
    #     user = User.query.get(session["user_id"])

    return render_template("homepage.html")

@app.route('/new-account', methods=['POST'])
def new_user_profile():
    """Process account creation and display my meals page."""

    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    bday = request.form["bday"]
    gender = request.form["gender"]
    pw = request.form["pw"]
    confirm_pw = request.form["confirm_pw"]

    #hashed_pw = generate_password_hash(pw)

    new_user = User(fname, lname, email, pw, bday, gender)
    db.session.add(new_user)
    db.session.commit()

    flash('Registration successful!.', 'success')
    session["user_id"] = new_user.getuserid()
    return redirect("/mymeals")

@app.route('/emails-from-db')
def check_email_in_db():
    """Checks if email is in db."""

    email = request.args.get("email")

    if User.query.filter_by(email=email).first() is None:
        return jsonify(True)    # email not in db
    else:
        return jsonify(False)    # email is in db


@app.route('/signin', methods=['POST'])
def signin_process():
    """Process sign in form."""

    email = request.form["email"]

    user = User.query.filter_by(email=email).first()

    session["user_id"] = user.user_id

    return redirect("/mymeals")


@app.route('/check-credentials')
def check_credentials():
    """Checks if email is in db and if password is correct."""

    email = request.args.get("email")
    pw = request.args.get("pw")

    # returns None if user not in db
    user = User.query.filter_by(email=email).first()

    # returns False if user IS in db
    if not user:
        return jsonify(False)

    if user.pw != pw:
        return jsonify(False)

    return jsonify(True)

@app.route('/signout')
def signout():
    """Log out."""

    del session["user_id"]
    return redirect("/clear")

@app.route('/clear')
def clear_credentials():
    """Clears authorization credentials that are stored in the Flask session."""

    if 'credentials' in session:
        del session['credentials']
    return redirect("/")

@app.route("/mymeals")
def check_for_plans():
    """Checks if user has any saved meal plans."""

    user = User.query.get(session["user_id"])

    if (Plan.query.filter_by(user_id=user.user_id).first()) is not None:
        # order by plan_id and get highest number
        plan = Plan.query.filter_by(user_id=user.user_id).order_by(desc(Plan.plan_id)).first()
        return redirect("/mymeals-{}".format(plan.plan_id))
    else:
        return render_template("no_meals.html", fname=user.fname)

@app.route("/mymeals-<int:plan_id>")

#  SHOWS THE RECIEPES SELECTED


def show_saved_recipes(plan_id):
    """Displays a meal plan."""

    session["plan_id"] = plan_id

    user = User.query.get(session["user_id"])
    plan = Plan.query.filter_by(plan_id=plan_id).first()
    recipes = plan.recipes
    start = plan.start.strftime("%b %#d, %Y")
    # all past plans made by current user
    past_plans = Plan.query.filter_by(user_id=user.user_id).all()

    return render_template("my_meals.html", start=start, recipes=recipes, fname=user.fname, past_plans=past_plans)


@app.route('/results')
def process_search():

    # SHOWS ALL RECIEPES TO BE SELECTED
    """Process search form and display results."""

    user = User.query.get(session["user_id"])
    if "rec_id" in session:
        del session["rec_id"]
    session['rec_id'] = []

    start = request.args.get("start")
    # session['start'] = start

    meals = Meals.query.all()
    

    # request.args is a multidict, so need to use .getlist (not .get)
    cuisines = request.args.getlist("cuisine")
    exclude = request.args.get("exclude")
    intolerant = request.args.getlist("intolerant")

    # make intolerant list into comma-separated string
    intolerant_str = ""
    for word in intolerant:
        intolerant_str += word + ","



    return render_template("results.html",
                           start=start,
                           cuisines=cuisines,
                           exclude=exclude,
                           intolerant=intolerant,
                           meals=meals,
                           results=mock_results,
                           fname=user.fname)


@app.route("/save-recipes", methods=['POST'])
  
#    SAVE RECIEPES FROM THE API TO THE DATABASE

def save_recipe():
    """Stores a saved recipe into database."""

       # make a new record in the plan table
    start = request.form.get("start")
    plan = Plan(start=start,
                user_id=session['user_id'],
                order_status="created"
                )
    db.session.add(plan)
    db.session.commit()

    recipes = []
    plan.recipes = []
    for i in range(1, 6):
        recipes.append(ast.literal_eval(request.form.get("recipe-{}".format(i))))
        recipe = db.session.query(Recipe).filter_by(recipe_id=recipes[i-1]["id"]).first()
        if recipe is not None:
            recipe.num_saved += 1
        else:
            #print("THIS IS THE RESPONSE: {}".format(recipes))
            recipe = Recipe(recipe_id=recipes[i-1]["id"],
                            title=recipes[i-1]["title"],
                            url=recipes[i-1]["url"],
                            image=recipes[i-1]["image"],
                            prep_time=recipes[i-1]["prepTime"],
                            num_saved=1,
                            fat=recipes[i-1]["fat"],
                            carbohydrates=recipes[i-1]["carbs"],
                            protein=recipes[i-1]["protein"])
            db.session.add(recipe)

        plan.recipes.append(recipe)

    db.session.commit()

    return redirect("/mymeals")



@app.route("/fat-data.json")

    # SHOWS FAT CALC FOR EACH RECIEPE

def fat_data():
    """Return percentage of fat for the five saved recipes."""

    user = User.query.get(session["user_id"])
    # plan = Plan.query.filter_by(user_id=user.user_id).order_by(desc(Plan.plan_id)).first()
    plan = Plan.query.get(session["plan_id"])
    recipes = plan.recipes

    color = "#4A7E13"
    fat = 0

    for recipe in recipes:
        fat += recipe.fat

    fat = (fat*3)/5

    if fat > 100:
        fat = 100
        color = "#dd3c45"

    fat_dict = {
                "labels": [
                    "Fat",
                    "Remainder",
                ],
                "datasets": [
                    {
                        "data": [fat, 100-fat],
                        "backgroundColor": [
                            color,
                            "gray"
                        ],
                        "hoverBackgroundColor": [
                            color,
                            "gray"
                        ]
                    }]
            }

    return jsonify(fat_dict)


@app.route("/carbs-data.json")
def carbs_data():

     # SHOWS CARBS CALC FOR EACH RECIEPE
    """Return percentage of carbs for the five saved recipes."""

    user = User.query.get(session["user_id"])
    # plan = Plan.query.filter_by(user_id=user.user_id).order_by(desc(Plan.plan_id)).first()
    plan = Plan.query.get(session["plan_id"])
    recipes = plan.recipes

    color = "#4A7E13"
    carbs = 0

    for recipe in recipes:
        carbs += recipe.carbohydrates

    carbs = (carbs*3)/5

    if carbs > 100:
        carbs = 100
        color = "#dd3c45"

    carbs_dict = {
                "labels": [
                    "Carbohydrates",
                    "Remainder",
                ],
                "datasets": [
                    {
                        "data": [carbs, 100-carbs],
                        "backgroundColor": [
                            color,
                            "gray"
                        ],
                        "hoverBackgroundColor": [
                            color,
                            "gray"
                        ]
                    }]
            }

    return jsonify(carbs_dict)


@app.route("/protein-data.json")
def protein_data():



     ############SHOWS PROTEIN CALC FOR EACH RECIEPE#############################


    """Return percentage of protein for the five saved recipes."""

    user = User.query.get(session["user_id"])
    # plan = Plan.query.filter_by(user_id=user.user_id).order_by(desc(Plan.plan_id)).first()
    plan = Plan.query.get(session["plan_id"])
    recipes = plan.recipes
    




    color = "#4A7E13"
    protein = 0

    for recipe in recipes:
        protein += recipe.protein

    protein = (protein*3)/5

    if protein > 100:
        protein = 100
        color = "#dd3c45"

    protein_dict = {
                "labels": [
                    "Protein",
                    "Remainder",
                ],
                "datasets": [
                    {
                        "data": [protein, 100-protein],
                        "backgroundColor": [
                            color,
                            "gray"
                        ],
                        "hoverBackgroundColor": [
                            color,
                            "gray"
                        ]
                    }]
            }

    return jsonify(protein_dict)


@app.route("/bmicalculator")
def bmicalculator():
    return render_template("bmicalculator.html");



@app.route('/newmeal', methods=['POST', 'GET'])
def newmeal():


    #####################COLLECTS MEALS FROM USER AND DISPLAYS THEM ####################



    """For displaying the form to add a new meal"""
    form = NewMeals()
    if request.method == 'POST':
        if form.validate_on_submit():
            UPLOAD_FOLDER = './static/'
            image = form.image.data
            filename = secure_filename(image.filename)
            
            image.save(os.path.join(UPLOAD_FOLDER, filename))
            newmeal = Meals(title=form.title.data, prepTime=form.prepTime.data, fat=form.fat.data,
                            carbohydrates=form.carbohydrates.data, protein=form.protein.data,
                            calories=form.calories.data, photo=filename)
            db.session.add(newmeal)
            db.session.commit()
            flash('Meal Saved', 'success')
            return redirect('/results')
        else:
            flash_errors(form)
    return render_template('meals.html', form=form)


@app.route('/meals')
def meals():

    ###########################SHOWS MEALS ADDED#############################


    return render_template('results.html', meals=Meals.query.all())


@app.route('/deliveries')
def track_deliveries():
    user = User.query.get(session["user_id"])

    plans = Plan.query.filter_by(user_id=user.user_id).all()


    
    return render_template('delivery.html',fname=user.fname, plans=plans, status=define_status)

@app.route('/meals/<filename>')
def get_image(filename):
    rootdir = os.getcwd()
    return send_from_directory(os.path.join(rootdir,['UPLOAD_FOLDER']), filename)    

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')





def make_recipe_search_request(cuisine, exclude, intolerant):
    """Makes recipe search API call and returns a list of recipes."""
    #search_url = "{}/recipes/search?".format(domain_url)
    # offset = random.randint(0, 100)

    querystring = {"query": "burger",
                   "diet": "vegetarian",
                   "excludeIngredients": "coconut",
                   "intolerances": "egg, gluten",
                   "number": "10", "offset": "0",
                   "type": "main course"}

    response = requests.request("GET", url, headers=headers, params=querystring)

    response = response.text
    return response

def choose_rand_results(raw_results):
    """Shuffles results. Returns max 12 results that are not in session and
    stores them in session."""

    random.shuffle(raw_results)
    sess_recs = set(session['rec_id'])
    results = []
    counter = 0
    used = 0
    # print "RAW RESULTS: {}".format(raw_results)

    for result in raw_results:
        # print "RESULT: {}".format(result)
        # print "COUNTER: {}".format(counter)
        if result[0] not in sess_recs and counter < 12:
            sess_recs.add(result[0])
            results.append(result)
            counter += 1
            used += 1
        else:
            used += 1
        if counter >= 12:
            break

    session['rec_id'] = list(sess_recs)

    remainder = len(raw_results) - used

    return (results, remainder)





def make_nutrition_info_request(ids):
    """Make bulk nutrition API call using ids of result recipes.
    Returns a response object."""

    nutrition_url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/ingredients/9266/information"

    params = {"includeNutrition": True,
                        "ids": ids
                        }

    return requests.get(nutrition_url,
                            headers=headers,
                            params=params
                            )











if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0", port=8070)