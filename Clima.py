import requests

#coordinates = "18.4667,-69.9000"
#apiURL = "https://api.darksky.net/forecast/246b51e71bee40bb6c2891177a6d6035/"
def getCoordinates(apiURL,location):
    requestData = requests.get(apiURL + location)
    jsonResponse = {
        "xCord" : requestData[""],
        "yCord" : requestData[""]
    }
    
    return requestData


def getClima(apiURL,coordinates):
    requestData = requests.get(apiURL + str(coordinates)).json()
    celcius = (int(requestData['currently']['temperature']) - 32) * 5 / 9
    jsonResponse = {
            "City": requestData["timezone"],
            "Icon": requestData["currently"]["icon"],
            "Currently": round(celcius),
        }
    #print(requestData.json())
    #print(jsonResponse)
    return jsonResponse

#getClima(apiURL,coordinates)

