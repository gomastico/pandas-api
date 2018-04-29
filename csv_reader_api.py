import pandas as pd
from flask import Flask, request, jsonify

database = pd.read_csv('test.csv', parse_dates=['Date'])
voters_columns = [col for col in database if ' - ' in col]

app = Flask(__name__)


@app.route('/get_voters_where')
def voters():
    args = request.args
    columns = voters_columns.copy()
    data = database

    if args.get('county'): data = data[data.County == args['county']]
    if args.get('month'): data = data[data.Date.dt.month == args['month']]
    if args.get('limit'): data = data.iloc[:int(args['limit'])]
    if args.get('party'): columns = [col for col in columns if col.split(' - ')[0] == args['party']]
    if args.get('status'): columns = [col for col in columns if col.split(' - '[0] == args['status'])]

    columns = ['Date', 'County', 'Grand Total'] + columns
    result = data[columns].to_dict('records')

    return jsonify(
        data=result
    )


if __name__ == '__main__':
    app.run(debug=True)
