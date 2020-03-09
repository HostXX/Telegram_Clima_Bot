import requests


def getClima(apiURL,coordinates):
    """This fucntion is used to make a request to a geo-localitatio API and retrieve the results"""
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

