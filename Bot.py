import requests
from bottle import Bottle, response, request as bottle_request
import re
import random
import os
import Clima

class BotHandlerMixin:
   BOT_URL = None

    if os.environ.get('APP_LOCATION') == 'heroku':
      BOT_URL = os.environ.get("API_TOKEN_URL")

    def get_chat_id(self, data):
        """
        Method to extract chat id from telegram request.
        """
        chat_id = data['message']['chat']['id']

        return chat_id

    def get_message(self, data):
        """
        Method to extract message id from telegram request.
        """
        message = data

        return message  

    def send_message(self, prepared_data):
        """
        Prepared data should be json which includes at least `chat_id` and `text`
        """       
        message_url = self.BOT_URL + 'sendMessage'
        requests.post(message_url, json=prepared_data)


class TelegramBot(BotHandlerMixin, Bottle):  
  
    BOT_URL = None
    CLIMA_API_URL=None

    if os.environ.get('APP_LOCATION') == 'heroku':
      BOT_URL = os.environ.get("API_TOKEN_URL")

    def __init__(self, *args, **kwargs):
        super(TelegramBot, self).__init__()
        self.route('/', callback=self.post_handler, method="POST")
        
        self.quotes = ["no se", "quisieras contarme una historia?", "Ojala a mau le de por programarme mas opciones","si crees que soy el futuro estás equivocado, lo eres tú. Si tuviera un deseo: desearía ser humano. Para saber cómo se siente sentir... ","xD","no me preguntes demaciadas cosas que aun soy medio bruto xD"]
       

        
    def chat_responses(self,message):
      
        if 'location' in message['message']:
          latitude = message['message']['location']['latitude']
          longitude = message['message']['location']['longitude']
          coordinates = str(latitude) + ',' + str(longitude)
          clima = Clima.getClima(self.CLIMA_API_URL,coordinates)
          answer = f" City: {clima['City']}\n Temperature: {clima['Currently']} -C\n Wheather: {clima['Icon']}\n"
            
          return answer
        
        if "/start" in message['message']['text']:
            name = message['message']['from']['first_name']
            greet = f"Hi {name} how you doing?\nSend me a location and I will tell you the current wheather!!!"
            
            return greet
        
        else:
          return random.choice(self.quotes)  
        
    def prepare_data_for_answer(self, data):
        message = self.get_message(data)
        answer = self.chat_responses(message)
        chat_id = self.get_chat_id(data)
        
        json_data = {
            "chat_id": chat_id,
            "text": answer,
        }

        return json_data

    def post_handler(self):
        data = bottle_request.json
        answer_data = self.prepare_data_for_answer(data)
        self.send_message(answer_data)

        return response


if __name__ == '__main__':  
    app = TelegramBot()
    if os.environ.get('APP_LOCATION') == 'heroku':
      app.run(host="0.0.0.0", port=int(os.environ.get("PORT",8080)))
    else:
      app.run(host='localhost', port=8080, debug=True)
