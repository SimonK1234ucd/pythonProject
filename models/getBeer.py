import requests

url = "https://beer9.p.rapidapi.com/"

querystring = {"brewery":"Berkshire brewing company"}

headers = {
	"x-rapidapi-key": "db2ace28dcmsh07bc764bed6f237p159ba4jsn2e6f76f626c0",
	"x-rapidapi-host": "beer9.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
