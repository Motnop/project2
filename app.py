from flask import Flask, render_template
import data



def top_tours(tours, count_top, type_sort):
    new_tours = {}
    keys = sorted(tours, key=lambda x: tours[x][type_sort], reverse=True)
    print(keys)
    for key in keys[:count_top]:
        new_tours[key] = tours.get(key, 'нет ключа')
    return new_tours

def count_derection_stats(direction):
    # Исходя из заданного направления считает количество туров, ночей(мин, макс), цену(мин, макс)
    tours = list(filter(lambda tour: tour['departure'] == direction, data.tours.values()))
    count = len(tours)
    price_max = max(tours, key=lambda x: x['price'])['price']
    price_min = min(tours, key=lambda x: x['price'])['price']
    night_min = min(tours, key=lambda x: x['nights'])['nights']
    night_max = max(tours, key=lambda x: x['nights'])['nights']
    return {
        'count': count,
        'min': price_min,
        'max': price_max,
        'night_min': night_min,
        'night_max': night_max
     }


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                            departures=data.departures, title=data.title,
                            subtitle=data.subtitle,
                            description=data.description, tours=top_tours(data.tours, 6, 'price')
                            )


@app.route('/departure/<direction>')
def departure(direction):
    if direction not in data.departures:
        return "Таких направлений не найдено!"
    else:
        return render_template('departure.html',
                                departures=data.departures, title=data.title,
                                stats=count_derection_stats(direction),
                                direction=data.departures[direction],
                                tours=data.tours,
                                churl=direction
                                )


@app.route('/tour/<id>')
def tour(id):
    return render_template('tour.html',
                            departures=data.departures, title=data.title,
                            tour=data.tours[int(id)],
                            )

app.run('0.0.0.0', port=8000, debug=True)
