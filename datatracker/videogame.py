from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint
import requests
import operator

bp = Blueprint('videogame', __name__)


@bp.route('/videogame', methods=['GET', 'POST', 'POST2'])
def index():
    response = requests.get('https://api.dccresource.com/api/games')
    all_games = response.json()

    # create data structures for future use.
    console_sales = {}
    console_name = []
    console_sales_num = []
    console_pair = {}  # For custom question

    # filter all_games for instructor-given question

    for game in all_games:
        # Checking for custom question
        platform = game["platform"]
        if platform not in console_pair.keys():  # if console not in dictionary yet, start at count of 1
            console_pair[platform] = 1
        else:                               # if key exists, tally the game onto the console_games count.
            console_pair[platform] += 1
        # Checking for user story question
        if game["year"] is not None and game["year"] >= 2013:
            if game["platform"] not in console_sales.keys():
                console_sales[platform] = game["globalSales"]
                console_name.append(platform)
            else:
                console_sales[platform] += game["globalSales"]

    for key in console_sales:
        console_sales_num.append(console_sales[key])

   # ################### #################### #################### #################### ####################
    # custom question
    # Which console has the highest quantity of games made for it? Top 10

    sorted_pairs = dict(sorted(console_pair.items(), key=operator.itemgetter(1), reverse=True))
    top_names = []
    top_qtys = []
    counter = 0
    # Get 2 lists: 1 that includes only the top 10 performing consoles and 1, a list of their corresponding numbers
    for name in sorted_pairs:
        if counter < 10:
            top_names.append(name)
            top_qtys.append(sorted_pairs[name])
            counter += 1
        else:
            break

    #  Bonus  #################################################################################################

    # Collect unique consoles and unique publishers
    unique_consoles_dict = {}

    for game in all_games:
        game_platform = game["platform"]
        if game_platform not in list(unique_consoles_dict):
            unique_consoles_dict[game_platform] = {}
        if game["publisher"] not in list(unique_consoles_dict[game_platform]):
            unique_consoles_dict[game_platform][game["publisher"]] = game["globalSales"]
        elif game["publisher"] in list(unique_consoles_dict[game_platform]):
            unique_consoles_dict[game_platform][game["publisher"]] += game["globalSales"]

    # Sort publishers into descending order, and only take top 5 into new dictionary
    new_consoles_dict = {}
    for console in unique_consoles_dict:
        sorted_publishers = dict(sorted(unique_consoles_dict[console].items(), key=operator.itemgetter(1), reverse=True))
        unique_consoles_dict[console] = sorted_publishers
        new_consoles_dict[console] = {}
        counter = 0
        for publisher in unique_consoles_dict[console]:
            if counter < 5:
                new_consoles_dict[console][publisher] = unique_consoles_dict[console][publisher]
                counter += 1
            else:
                break

    single_console_dict = new_consoles_dict["PS3"]
    console_names = unique_consoles_dict.keys()

    # If user is searching for a game (POST) #################################################################

    search_results = []
    unique_titles = []
    if request.method == 'POST':
        if request.form['user_input'] not in console_names:
            search_user_input = request.form["user_input"]
            # Find all matches to search word(s)
            for game in all_games:
                if search_user_input in game["name"]:
                    game["consolidated"] = False
                    search_results.append(game)
            # Starts a new dictionary representing the title. Creates sub-dictionary under platforms, reps the release.
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
                    # Finds games sharing a title with a game already stored in the unique_titles list.
                    # Add the platform-based release as another mini dictionary under the platforms key
                    for possible_matches in search_results:
                        if possible_matches["consolidated"] is False and result["name"] == possible_matches["name"]:
                            possible_matches["consolidated"] = True
                            platform_dict = {"_id": result["_id"], "platform": possible_matches["platform"],
                                             "year": possible_matches["year"],
                                             "globalSales": possible_matches["globalSales"]}
                            common_title_dict["platforms"].append(platform_dict)
                    # Add uniquely titled game, or set of games, to the list of unique titles.
                    unique_titles.append(common_title_dict)

        else:
            select_user_input = request.form["user_input"]
            single_console_dict = new_consoles_dict[select_user_input]



    return render_template('videogame/index.html', console_name=console_name, console_sales_num=console_sales_num,
                           top_names=top_names, top_qtys=top_qtys, search_results=search_results,
                           unique_titles=unique_titles, single_console_dict=single_console_dict, console_names=console_names)




