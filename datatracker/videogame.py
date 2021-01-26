from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint
import requests
import operator

bp = Blueprint('videogame', __name__)


@bp.route('/videogame', methods=('GET', 'POST'))
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

    unique_consoles = []
    unique_publishers = []
    # Collect unique consoles and unique publishers
    for game in all_games:
        if game["platform"] not in unique_consoles:
            unique_consoles.append(game["platform"])
        if game["publisher"] not in unique_publishers:
            unique_publishers.append(game["publisher"])

    unique_console_dicts = []
    unique_publisher_dicts = []
    # Load list of strings into list of dictionaries as dict-identifying keys
    for platform_name in unique_consoles:
        console_dict = {"console": platform_name}
        unique_console_dicts.append(console_dict)
    for publisher_name in unique_publishers:
        publisher_dict = {"publisher": publisher_name}
        unique_publisher_dicts.append(publisher_dict)
    # Get summation of global sales per platform per publisher.
    for game in all_games:
        for i in range(len(unique_publisher_dicts)):
            publishers_platforms = unique_publisher_dicts[i].keys()
            if game["publisher"] == unique_publisher_dicts[i]["publisher"] and \
                    game["platform"] not in publishers_platforms:
                unique_publisher_dicts[i][game["platform"]] = game["globalSales"]
                break
            elif game["publisher"] == unique_publisher_dicts[i]["publisher"] and \
                    game["platform"] in publishers_platforms:
                unique_publisher_dicts[i][game["platform"]] += game["globalSales"]
                break
    # Get top publisher for each console
    for console in unique_console_dicts:
        for publisher in unique_publisher_dicts:
            console_publisher_keys = console.keys()
            if console["console"] in publisher.keys():
                if len(console_publisher_keys) == 1:  # If a top publisher is not yet established
                    console["topPublisher"] = publisher["publisher"]
                    console["topSales"] = publisher[console["console"]]
                else:  # if top publisher is exceeded, then they are replaced
                    if publisher[console["console"]] > console["topSales"]:
                        console["topPublisher"] = publisher["publisher"]
                        console["topSales"] = publisher[console["console"]]

    # If user is searching for a game (POST) #################################################################

    search_results = []
    unique_titles = []
    if request.method == 'POST':
        search_user_input = request.form["search_input"]
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
        print("Fuck Brady, Fuck Mahomes")

# ########################## ########################## ########################## ##########################
#     # Bonus alternate (maybe trash)
#
#     bonus_data = []
#     all_consoles = []
#     placeholderfordict ={}
#     for game in all_games:
#         if not all_consoles:
#             placeholderfordict[game["platform"]] = 0
#             all_consoles.append(placeholderfordict)
#         elif game["platform"] not in all_consoles:
#             placeholderfordict[game["platform"]] = 0
#             all_consoles.append(placeholderfordict)
#
#     console_dict_bonus = {}
#     console_dict_bonus["consoles_sales"] = placeholderfordict
#
#     for game in all_games:
#         if not bonus_data:
#             console_dict_bonus["publisher"] = game["publisher"]
#             bonus_data.append(console_dict)
#         elif game["publisher"] not in bonus_data:
#             console_dict_bonus["publisher"] = game["publisher"]
#             bonus_data.append(console_dict)
#             for item in bonus_data["consoles_sales"]:   # work in progress. maybe trash
#                 if game["platform"] == item["platform"]:
#                     item["platform"] = game["platform"]
#     print("tree")
# ########################## ########################## ########################## ##########################


    return render_template('videogame/index.html', console_name=console_name, console_sales_num=console_sales_num,
                           top_names=top_names, top_qtys=top_qtys, search_results=search_results,
                           unique_titles=unique_titles, unique_console_dicts=unique_console_dicts)


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

