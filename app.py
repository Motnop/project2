from flask import Flask, render_template
import data


def count_derection(direction):
    count = 0
    price = []
    night = set()
    tours = data.tours
    for i in tours:
        if tours[i]["departure"] == direction:
            count += 1
            price.append(tours[i]["price"])
            night.add(tours[i]["nights"])
    price.sort()
    min = price[0]
    max = price[-1]
    return {'count': count, 'min': min, 'max': max, 'night_min': sorted(night)[0], 'night_max': sorted(night)[-1]}


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', departure=data.departures, title=data.title, subtitle=data.subtitle,
                           description=data.description, tours=data.tours)


@app.route('/departure/<direction>')
def departure(direction):
    if direction not in data.departures:
        return "Таких направлений нет"
    else:
        return render_template('departure.html', dep=count_derection(direction),
                               direction=data.departures[direction], tours=data.tours, churl=direction)


@app.route('/tour/<id>')
def tour(id):

    return render_template('tour.html', tours=data.tours[int(id)], departure=data.departures)

app.run('0.0.0.0', port=8000, debug=True)