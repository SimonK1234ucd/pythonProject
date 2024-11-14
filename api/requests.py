import requests

def runGetRequest(url):
    print("Running get request to", url)

    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return "Error", response.status_code
    except Exception as e:
        return "Error", e
