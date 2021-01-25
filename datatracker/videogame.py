from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint
import requests
import operator

bp = Blueprint('videogame', __name__)


@bp.route('/videogame', methods=('GET', 'POST'))
def index():
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
        if platform not in console_pair: #if console not in dictionary yet, start at count of 1
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

    search_results = []
    unique_titles = []
    if request.method == 'POST':
        search_user_input = request.form["search_input"]
        for game in all_games:
            if search_user_input in game["name"]:
                game["consolidated"] = False
                search_results.append(game)

        for result in search_results:
            if result["consolidated"] is False:
                result["consolidated"] = True
                platform_dict = {"_id": result["_id"], "platform": result["platform"],
                                 "year": result["year"],
                                 "globalSales": result["globalSales"]}
                common_title_dict = {"name": result["name"],
                                     "genre": result["genre"],
                                     "publisher": result["publisher"],
                                     "platforms": [platform_dict]}

                for possible_matches in search_results:
                    if possible_matches["consolidated"] is False and result["name"] == possible_matches["name"]:
                        possible_matches["consolidated"] = True
                        platform_dict = {"_id": result["_id"], "platform": possible_matches["platform"],
                                         "year": possible_matches["year"],
                                         "globalSales": possible_matches["globalSales"]}
                        common_title_dict["platforms"].append(platform_dict)
                unique_titles.append(common_title_dict)
        print("Fuck Brady, Fuck Mahomes")

    return render_template('videogame/index.html', console_name=console_name, console_sales_num=console_sales_num,
                           top_names=top_names, top_qtys=top_qtys, search_results=search_results,
                           unique_titles=unique_titles)





@bp.route('/layout_example')
def layout_example():

    response = requests.get('https://api.dccresource.com/api/games')
    all_games = response.json()
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
    return render_template('videogame/layout_example.html', console_name=console_name, console_sales_num=console_sales_num)

