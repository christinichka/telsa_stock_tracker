import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


STOCK_API_KEY = "YOUR STOCK API KEY"
NEWS_API_KEY = "YOUR NEWS API KEY"
TWILIO_SID = "YOUR TWILIO SID"
TWILIO_TOKEN = "YOUR TWILIO TOKEN"

# https://www.alphavantage.co/documentation/#daily

# Get yesterday's closing stock price. 
stock_params = {
	"function": "TIME_SERIES_DAILY",
	"symbol": STOCK_NAME,
	"apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing)

# Find the positive difference between the two day's closing prices. 
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing)
up_down = None
if difference > 0:
	up_down = "🔺"
else:
	up_down = "🔻"


# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
difference_percent = round((difference / float(yesterday_closing_price)) * 100)
print(difference_percent)


# https://newsapi.org/ 

# If percentage is greater than 1 then use the News API to get articles related to the COMPANY_NAME.
if abs(difference_percent) > 1:
	news_params ={
	"apikey": NEWS_API_KEY,
	"qInTitle": COMPANY_NAME,
	}

	news_response = requests.get(NEWS_ENDPOINT, params=news_params)
	articles = news_response.json()["articles"]


# Use Python slice operator to create a list that contains the first 3 articles. 

three_articles = articles[:3]
print(three_articles)
    


    # Use twilio.com/docs/sms/quickstart/python to send a separate message with each article's title and description to your phone number. 

# Create a new list of the first 3 article's headline and description using list comprehension.
formatted_articles = [f"{STOCK_NAME}: {up_down}{difference_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]


# Send each article as a separate message via Twilio. 
client = Client(TWILIO_SID, TWILIO_TOKEN)

for article in formatted_articles:
	message = client.messages.create(
		body=article,
		from_="YOUR TWILIO PHONE NUMBER",
		to="YOUR PHONE NUMBER",
	)



