from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint
import requests

bp = Blueprint('videogame', __name__)


@bp.route('/videogame')
def index():

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

    return render_template('videogame/index.html', console_name=console_name, console_sales_num=console_sales_num)

