from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint
import requests

bp = Blueprint('videogame', __name__)


@bp.route('/videogame')
def index():

    response = requests.get('https://api.dccresource.com/api/games')
    all_games = response.json()

    recent_games = {}
    for i in all_games:
        if all_games[i]['year'] >= 2013:
            recent_games.append(all_games[i])

    console_sales = {}
    for j in recent_games:
        platform = recent_games[j]["platform"]
        if recent_games[j]["platform"] not in console_sales.keys():
            console_sales[platform] = recent_games[j]["globalSales"]
        else:
            console_sales[platform] += recent_games[j]["globalSales"]




    return render_template('videogame/index.html')