from flask import render_template, request, flash
import requests
from flask_login import login_required
from .import bp as main


@main.route('/students', methods=['GET'])
@login_required
def students():
    my_students=["Thu", "Leo", "Sydney", "Josh", "Chris", "Fernado", "Benny", "Vicky", "Bradley"]
    return render_template("students.html.j2",students=my_students)

@main.route('/ergast', methods=['GET','POST'])
@login_required
def ergast():
    if request.method == 'POST':
        year = request.form.get('year')
        round = request.form.get('round')
        url = f'http://ergast.com/api/f1/{year}/{round}/driverStandings.json'
        response = requests.get(url)
        if response.ok:
            #do stuff with the data
            ## This part I changed from class.. 
            # instead of the try else I check to make sure the Driver standing list
            #  is not empty before we grab the data
            data = response.json()["MRData"]["StandingsTable"]["StandingsLists"]
            if not data:
                flash(f'There is no info for {year} round {round}','warning')
                return render_template("ergast.html.j2")

            data = data[0].get("DriverStandings")
            all_racers = []
            for racer in data:
                racer_dict={
                    'first_name':racer['Driver']['givenName'],
                    'last_name':racer['Driver']['familyName'],
                    'position':racer['position'],
                    'wins':racer['wins'],
                    'DOB':racer['Driver']['dateOfBirth'],
                    'nationality':racer['Driver']['nationality'],
                    'constructor':racer['Constructors'][0]['name']
                }
                all_racers.append(racer_dict)
            return render_template("ergast.html.j2",racers=all_racers)
        else:
            flash("Houston We Have a Problem",'danger')
            render_template("ergast.html.j2")
    return render_template("ergast.html.j2")

