# Project

The app will use external API Alphavantage and is able to provid information about dates, open price, close price, low price, high price and volume of equity trade for company given name.
To use external API, I registered and get a key to have access to their data. In the app, the key is being used instead of Url and by using "from alpha_vantage.timeseries import TimeSeries" the companies information is readable.


# How the app works

There are two get and one post methods in the app. The first one just gives the name of all companies that their data already has been aded and available in database. In this case,presented data are belong to companies: B, FORD, GOOGL,AMZN and MSFT.

	Example:	GET http://35.242.138.254/
	[
 	 "B",
	  "FORD",
	  "GOOGL",
	  "AMZN",
	  "MSFT"
	]

The second GET methods take the company name as a variable and return all the information about that.

	Example: 	GET http://35.242.138.254/MSFT
	{
     	"2019-03-28",
    	"2019-03-27",
   	 "2019-03-26",
   	 "2019-03-25",
   	 "2019-03-22",
   	 "2019-03-21",

The third method is POST method that we just pass the company name. The app extract data for that company from external API and stored data in database.

	Example:	POST http://35.242.138.254/
			Content-Type: application/json

			{"name":"GOOGL"}
			
# Creating clusters with 3-nods named cassandra

	export PROJECT_ID="$(gcloud config get-value project -q)"
	gcloud config set compute/zone europe-west2-b
	gcloud container clusters create cassandra --num-nodes=3 --machine-type "n1-standard-2"
	
# Downloading 3 files which allow peer diversity, cassandra service itself and replication controller
	wget -O cassandra-peer-service.yml http://tinyurl.com/yyxnephy
	wget -O cassandra-service.yml http://tinyurl.com/y65czz8e
	wget -O cassandra-replication-controller.yml http://tinyurl.com/y2crfsl8
	
# Running the three files
	kubectl create -f cassandra-peer-service.yml
	kubectl create -f cassandra-service.yml
	kubectl create -f cassandra-replication-controller.yml
	
# Scaling up number of nods through replication and pick one of the container 
	kubectl scale rc cassandra --replicas=3
	kubectl get pods
	kubectl exec -it cassandra-2wxp6 cqlsh
	
# Creating keyspace
	CREATE KEYSPACE stocks WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 2};

# Build the docker in the same directory
	docker build --tag=stocks-image:1.0 .
	
# Tag the docker
	docker tag stocks-image:1.0 gcr.io/my-first-project-234315/stocks-image:1.0
	
# Push the docker into the Google Repository
	docker push gcr.io/my-first-project-234315/stocks-image:1.0
	
# Run the image in port 8080
	kubectl run stocks-webapp --image=gcr.io/my-first-project-234315/stocks-image:1.0 --port 8080
	
# Exposing the deployment to get an external IP
	kubectl expose deployment stocks-webapp --type=LoadBalancer --port 80 --target-port 8080
