# Project

The app will use external API Alphavantage and is able to provid information about dates, open price, close price, low price, high price and volume of equity trade for companies.

In the first GET method the app will provide the name of company.

        @app.route('/', methods = ['GET'])
        def get_all_equity_names():
	q = Equity.all()
	count = len(q)
	name=[]
	for i in range(count):
		name.append(q[i]['equity_name'])
	return jsonify(name)
        
        
In the second GET method the app will provide all of the detail about company given name.

        @app.route('/<name>', methods = ['GET'])
	def get_data_by_name(name):
	q = Equity.all()
	count = len(q)
	names=[]
	for i in range(count):
		names.append(q[i]['equity_name'])
	if name in names:
		named_records = dict(Equity.get(equity_name=name))
		return jsonify(named_records), 200
	else:
		return jsonify({'error':'equity name not found!'}), 404
 
 Another option available in this app is post method. It take the name of the company and add its relevent information to app therefore, we can accsses to that information via GET method.
        
        @app.route('/', methods=['POST'])
        def create_records():

	if not request.json or not 'name' in request.json:
		return jsonify({'error':'the new record needs to have an equity name'}), 400
	name_input = {'name': request.json['name']}
	equity = name_input['name']
        
The last part of the app create a table by creating columns first

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

	Equity.create		(equity_name=equity,equity_timestamp=timestamp,equity_open=open_quote,equity_high=high_quote,equity_low=low_quote,equity_close=close_quote,equity_volume=volume)
        
