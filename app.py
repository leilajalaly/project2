from alpha_vantage.timeseries import TimeSeries
from flask import Flask
from flask_cqlalchemy import CQLAlchemy

#Flask setup
app = Flask(__name__)
app.config['CASSANDRA_HOSTS'] = ['localhost']
app.config['CASSANDRA_KEYSPACE'] = "stocks"
app.config['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = True
db = CQLAlchemy(app)

class Equity(db.Model):
    equity_name = db.columns.Text(primary_key=True,required=True)
    equity_timestamp = db.columns.List(db.columns.Text,required=False)
    equity_open = db.columns.List(db.columns.Text,required=False)
    equity_high = db.columns.List(db.columns.Text,required=False)
    equity_low = db.columns.List(db.columns.Text,required=False)
    equity_close = db.columns.List(db.columns.Text,required=False)
    equity_volume = db.columns.List(db.columns.Text,required=False)
db.sync_db()


@app.route('/equity/<name>', methods=['GET'])
def get_quotes(name):

	#Initialize external API Alphavantage
	ts = TimeSeries(key='10LJJQ5BQXUED1VF')
	data = ts.get_daily(name)

	#Extract dates to list
	dates = data[0].keys()
	timestamp=list(dates)

	#Extract quotes

	open_quote=[]
	for i in dates:
		open_quote.append(data[0][i]['1. open'])

	high_quote=[]
	for i in dates:
		high_quote.append(data[0][i]['2. high'])

	low_quote=[]
	for i in dates:
		low_quote.append(data[0][i]['3. low'])

	close_quote=[]
	for i in dates:
		close_quote.append(data[0][i]['4. close'])

	volume=[]
	for i in dates:
		volume.append(data[0][i]['5. volume'])

	#Add data to db

	Equity.create(equity_name=name,equity_timestamp=timestamp,equity_open=open_quote,equity_high=high_quote,equity_low=low_quote,equity_close=close_quote,equity_volume=volume)

	equity_data=Equity.get(equity_name=name)

	return()


if __name__ == '__main__':
    app.run(port=8080, debug=True)
