# Python libraries that we need to import for our bot
import random

# Importamos Flask el framework y pymessenger para uso del Bot
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'ACCESS_TOKEN'  # ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = 'EAAeZAlfWVhZB4BAFeeqi26A9r3ElHI7TuxhZAYIgDpGE4EN0tAIS0qynZBeyFURM8yo2vBCJZCxJTbNngUpZAW26sMA47f6sMP7ZB1LSZAZBjjHVNYRl3z6lYKKAz8XQiqTqvmrBldDnjGhPO7YvZAg8Bx70LbSFLyjjbh9KqlfNZBCd4QXW2sLQrPY'  # VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)


# Recibiremos mensajes que Facebook nos envia al bot en este punto de acceso
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        # Antes de poder comunicarte con el bot, Facebook implementa un token de verificacion
        # que confirme que todas las peticiones vienen de Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # Si no se obtuvo la peticion por GET, debe ser POST
    else:
        # obtiene calquier mensaje que un usuario envie al bot objeto json
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # Identificador de usuario de Facebook para saber donde enviar la respuesta
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                    # SI el usuario envia foto o video
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    # Compara el token enviado por facebook y verifica si coincide con el token que yo envio
    # Si coinciden se permite la peticion, sino devuelvo un error else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Se ha producido un error debido a que el token es invalido'


# Escoge un mensaje de bienvenida aleatorio para el usuario
def get_message():
    sample_responses = ["Bienvenido a Tango Bot!", "En que puedo ayudarle. Tango Bot", "Comenteme su duda!",
                        "Bienvenido :)"]
    # Devuelve alguna de las opciones configuradas de Inicio
    return random.choice(sample_responses)


# Se usa PyMessenger para enviar respuesta al usuario
def send_message(recipient_id, response):
    # Envia el mesage de respuesta al usuario
    bot.send_text_message(recipient_id, response)
    return " Envio Exitoso!"


if __name__ == "__main__":
    app.run()
