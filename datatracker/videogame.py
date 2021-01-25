from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint
import requests
import operator

bp = Blueprint('videogame', __name__)


@bp.route('/videogame', methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        response = requests.get('https://api.dccresource.com/api/games')
        all_games = response.json()

        # filter all_games for instructor-given question

        recent_games = []

        for game in all_games:
            if game["year"] is not None:
                if game["year"] >= 2013:
                    recent_games.append(game)

        console_sales = {}
        for recent_game in recent_games:
            platform = recent_game["platform"]
            if recent_game["platform"] not in console_sales.keys():
                console_sales[platform] = recent_game["globalSales"]
            else:
                console_sales[platform] += recent_game["globalSales"]

        console_name = []
        console_sales_num = []

        for key in console_sales:
            console_name.append(key)
            console_sales_num.append(console_sales[key])

       #################### #################### #################### #################### ####################
        #filter all_games for custom question
        #Which console has the highest quantity of games made for it? Top 10
        console_games = []
        for game in all_games:
            console_games.append(game)

        console_pair = {}
        for game in console_games:
            platform = game["platform"]
            if platform not in console_pair:#if console not in dictionary yet, start at count of 1
                console_pair[platform] = 1
            else:                               #if key exists, tally the game onto the console_games count.
                console_pair[platform] += 1


        sorted_pairs = dict(sorted(console_pair.items(), key=operator.itemgetter(1), reverse=True))

        top_names = []
        top_qtys = []
        counter = 0
        for name in sorted_pairs:
            if counter < 10:
                top_names.append(name)
                top_qtys.append(sorted_pairs[name])
                counter += 1


        return render_template('videogame/index.html', console_name=console_name, console_sales_num=console_sales_num,
                               top_names=top_names, top_qtys=top_qtys)



