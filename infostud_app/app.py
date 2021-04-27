from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/infostud_db"
mongo = PyMongo(app)


ROWS_PER_PAGE = 15


@app.route("/employer", methods=['POST', 'GET'])
def employer_page():
    if request.method == 'POST':
        employer = request.form['employer']
        if not employer:
            return render_template("employer.html")
        return redirect(url_for("get_jobs_per_employer", name=employer))
    return render_template("employer.html")


@app.route("/city", methods=['POST', 'GET'])
def city_page():
    if request.method == 'POST':
        city = request.form['city']
        if not city:
            return render_template("city.html")
        return redirect(url_for("get_jobs_per_city", name=city))
    return render_template("city.html")


@app.route("/", methods=['GET'])
def get_all_jobs():
    results = mongo.db.infostud_new.find({})
    return render_template('index.html', data=results)


@app.route("/jobs/employer=<name>", methods=['GET'])
def get_jobs_per_employer(name=None):
    results = mongo.db.infostud_new.find({'employer_name':name})
    return render_template('index.html', data=results)


@app.route("/jobs/city=<name>", methods=['GET'])
def get_jobs_per_city(name=None):
    results = mongo.db.infostud_new.find({'$or': [{'city': {'$in': [name]}}, {'city': {'$in': [" "+name]}}]})
    return render_template('index.html', data=results)


if __name__ == '__main__':
    app.run()