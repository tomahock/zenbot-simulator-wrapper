#!/usr/bin/env python
from flask import Flask, request, redirect, render_template, url_for
from flask_autoindex import AutoIndex
from pymongo import MongoClient
import subprocess
import datetime
import json

app = Flask(__name__, static_url_path='/static')
results_index = AutoIndex(app, browse_root='./static/results', add_url_rules=False)


@app.route("/")
def get_index():
    client = MongoClient()
    db = client.zenbot4
    collection = db.resume_markers
    cursor = collection.find()
    markers = []
    for m in cursor:
        markers.append(m)

    client.close()
    markersJson = json.dumps(markers, ensure_ascii=True)

    return render_template("index.html", markers=markers, markersJson=markersJson)


@app.route("/results/")
def get_files():
    path = request.args.get('path') if request.args.get('path') else ''

    return results_index.render_autoindex(path, endpoint='get_files')


@app.route("/", methods=['POST'])
def post_index():
    strategy = request.form['strategy']
    days = request.form['days']
    buy_pct = request.form['buy_pct']
    sell_pct = request.form['sell_pct']
    markup_pct = request.form['markup_pct']
    order_adjust_time = request.form['order_adjust_time']
    sell_stop_pct = request.form['sell_stop_pct']
    buy_stop_pct = request.form['buy_stop_pct']
    max_sell_loss_pct = request.form['max_sell_loss_pct']
    rsi_periods = request.form['rsi_periods']
    selector = request.form['selector']

    today = datetime.date.today()

    command = [
        "zenbot",
        "sim",
        selector,
        "--strategy", strategy,
        "--days", days,
        "--buy_pct", buy_pct,
        "--sell_pct", sell_pct,
        "--markup_pct", markup_pct,
        "--order_adjust_time", order_adjust_time,
        "--sell_stop_pct", sell_stop_pct,
        "--buy_stop_pct", buy_stop_pct,
        "--max_sell_loss_pct", max_sell_loss_pct,
        "--rsi_periods", rsi_periods,
    ]

    filename = "static/results/%s-%s.html" % ('_'.join(command), today)

    command.append("--filename")
    command.append(filename)

    subprocess.Popen(command)

    return redirect(url_for('get_files'))


if __name__ == '__main__':
    app.run(port=8091, host='127.0.0.1')
