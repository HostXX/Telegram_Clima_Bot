import re
import random
import os
import requests
from bottle import Bottle, response, request as bottle_request
import Clima

class BotHandlerMixin:  
    BOT_URL = None
    
    
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
        message_text = data['message']['text']

        return message_text

    def send_message(self, prepared_data):
        """
        Prepared data should be json which includes at least `chat_id` and `text`
        """       
        message_url = self.BOT_URL + 'sendMessage'
        requests.post(message_url, json=prepared_data)


class TelegramBot(BotHandlerMixin, Bottle):  
    BOT_URL = None
    CLIMA_URL = "https://api.darksky.net/forecast/246b51e71bee40bb6c2891177a6d6035/"
    coordinates = "18.5328281,-69.7907998"

    if os.environ.get('APP_LOCATION') == 'heroku':
      BOT_URL = os.environ.get("API_TOKEN_URL")
    else:
      BOT_URL = 'https://api.telegram.org/bot931660199:AAF__ZLvWzFZz8T5Ykbbwwj1VdnmvwdI0p8/'
    
    
    def __init__(self, *args, **kwargs):
        super(TelegramBot, self).__init__()
        self.route('/', callback=self.post_handler, method="POST")
        
        self.quotes = ["no se", "quisieras contarme una historia?", "Ojala a mau le de por programarme mas opciones","si crees que soy el futuro estás equivocado, lo eres tú. Si tuviera un deseo: desearía ser humano. Para saber cómo se siente sentir... ","xD","no me preguntes demaciadas cosas que aun soy medio bruto xD"]
       

        
    def chat_responses(self,message,data):
        
        if "/start" in message:
            name = data['message']['from']['first_name']
            greet = f"Hola {name} como estas?"
            return greet
            
        
        if "/clima" in message:
          city = None
          clima = Clima.getClima(self.CLIMA_URL,self.coordinates)
          answer = " City: {}\n Temperature: {} -C\n Wheather: {}\n".format(clima["City"],clima['Currently'],clima["Icon"])
          params = ""
          modmessage = str(message).split()
          
          if  len(modmessage) > 1:
            params = str(message).split()[-1]
            
          return answer
        
        
        else: 
            return random.choice(self.quotes)
            
        
    def prepare_data_for_answer(self, data):
        message = self.get_message(data)
        answer = self.chat_responses(message,data)
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
