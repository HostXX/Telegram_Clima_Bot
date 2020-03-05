import random
import os
import requests
from bottle import Bottle, response, request as bottle_request


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
    BOT_URL = 'https://api.telegram.org/bot1011361775:AAGF9wBXA4WDpmNzzkzzZJd9fsU-ISd7-HI/'

    def __init__(self, *args, **kwargs):
        super(TelegramBot, self).__init__()
        self.route('/', callback=self.post_handler, method="POST")
        self.quotes = ["no se", "no se, pero felipe es un mamaculo","si crees que soy el futuro estás equivocado, lo eres tú. Si tuviera un deseo: desearía ser humano. Para saber cómo se siente sentir... ","ded"]
        self.categories = ["Suggestions","Big Ass","Dominicana","Black Girls","Porno en espanol","Family","Madre e hijo","18","Mami jordan","Espanol","Toons","Culonas","Milf","Female Ejaculation","Lesbianas","Porno casero"]

        
        
    def chat_responses(self, text):
        if "Mándame" and  "algo" and  "jevi" in text:
            url = "https://www.xnxx.com/search/"
            return url + random.choice(self.categories)
        if "158" and "vídeo" in text:
            return "baquea https://www.xnxx.com/video-flqjf29/158"
       
        if "porno" in text:
            return random.choice(["en un ratico billy","buscate algo aqui, https://www.xnxx.com/"])
        
        if "hola" or "Hola" in text:
            return "hola, en que te puedo ayudar? puedes pedirme porno o que te mande algo jevi" 

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
