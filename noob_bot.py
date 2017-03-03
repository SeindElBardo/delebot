"""
	El objetivo de este bot es servir de guía para aprender las cosas básicas de
	un bot de telegram.

	Podéis aprender más en https://github.com/eternnoir/pyTelegramBotAPI ,
	también os facilito la documentación https://core.telegram.org/bots/api
	Dicho esto y suponiendo que ya tenemos un bot creado desde @botFather, vamos a darle.
"""
import telebot
import time
from threading import Thread, Lock # Necesario para multihilos

# Necesario para programar tareas
import datetime	#https://docs.python.org/2/library/datetime.html
import logging	# Se pone porque es necesario para añadir trabajos en otros métodos, o algo así
from apscheduler.schedulers.background import BackgroundScheduler
# http://apscheduler.readthedocs.io/en/latest/modules/triggers/date.html?highlight=trigger%20alias
# http://apscheduler.readthedocs.io/en/latest/modules/schedulers/base.html
scheduler = BackgroundScheduler()
scheduler.start()        # start the scheduleruler
logging.basicConfig()




"""
Para saber que bot ejecuta el programa se necesita inicializarlo
con un token, este lo obtendreís al crear un bot y está feo que 
el token este en algún lugar público, al igual que los ids, por eso todos los
que aparecen son inventados.
Añadid a esta función un string con el token para vincularlo.
"""
bot = telebot.TeleBot() 


myLock = Lock ()
myTiempo = 0
t = None

tupla = {}

"""
Por ahora vamos a trabajar con dos tipos de comandos, el comando puro y el texto inline,
para este segundo hay que activar la opción en el bot desde botFather.

Empezamos por los comandos puros, en los que al bot le escribes "/loquesea", la primera línea
es un decorador que se encarga de capturar estos comandos, las palabras que estén en la lista
de commands serán las que disparen la función. Es importante que los comandos estén completamente
en minusculas.

Cuando se ejecuta la función el parámetro que siempre recogemos es message, esto es el mensaje
que ha mandado la persona que ha ejecutado, es este caso "/loquesea" lo gracioso es que el mensaje
tiene mucha información del usuario que podemos utilizar.
Consultad https://core.telegram.org/bots/api#message para destriparlo mejor.

En este método lo único que hacemos es utilizar ese mensaje para obtener el usuario que lo mando
y de él su nombre (el encode no sé si en python3 nos lo podemos ahorrar), y lo concatenamos con un Hola.

Por último, el bot tiene una función para mandar mensajes cuyos parametros son el chat al que enviarlo
y el texto.
"""
@bot.message_handler(commands=['hello'])
def helloWorld(message):
	text = "Hola, " + str(message.from_user.first_name.encode('utf-8'))
	bot.send_message(message.chat.id, text)

"""
Este es el echo de toda la vida, pero tiene una particularidad, si hacemos un echo simple rollo
"/echo caca" va a volver "/echo caca", en este método se llama a la función parseeitor que me he
hecho yo para retirar el comando y obtener sólo el texto.
"""
@bot.message_handler(commands=['echo'])
def send_mensaje(message):
	if message.text.count(' ') > 0:
		i = message.text.index(' ')
		mensaje = message.text[i+1:]
		if (mensaje.lower().find("soy imbecil") != -1) or (mensaje.lower().encode('utf-8').find("soy imbécil") != -1):
			mensaje = "Eres imbécil"
	else:
		mensaje = "Leer la mente no forma parte de mis funciones, aún."

	bot.send_message(message.chat.id, mensaje)

"""
Sabiendo que desde un mensaje podemos extraer el id del chat (que es negativo si es un grupo y positivo
si es un usuario), bastaría con hacer un print o volcarlo en algún fichero para tenerlo a nuestra disposición.
De que sirve esto, pues que puedes usar el bot. Por ejemplo, sabiendo el id del chat de Clara, podemos
hacer una función que mande el mensaje escrito. Esto lo puedes hacer también para un grupo.
"""
@bot.message_handler(commands=['sendclara'])
def sendMensajeBP(message):
	idClara = 4542368453
	if message.text.count(' ') > 0:
		i = message.text.index(' ')
		mensaje = message.text[i+1:]
		bot.send_message(idClara, mensaje)
	else:
		bot.reply_to(message, "Leer la mente no forma parte de mis funciones, aún.")

"""
La Api de TelegramBot funciona por norma con 2 hilos, pero podemos crear más, explicar hilos
no es el objetivo de este tutorial, pero básicamente se utilizan una sería de variables y objetos
para lanzar un hilo que ejecuta una función (target) con unos parámetros (args)
"""
@bot.message_handler(commands=['countdown'])
def starCountdown(message):
	global t
	if message.text.count(' ') > 0:
		i = message.text.index(' ')
		mensaje = message.text[i+1:]
	try:
		t = Thread(target=countdown, args=(int(mensaje), message.chat.id))
		t.start()
	except:
		bot.send_message(message.chat.id, "Necesito que me digas cuantos segundos de cuenta atrás quieres")

# Una variante graciosa
@bot.message_handler(commands=['countdownm'])
def starCountdownm(message):
	global t
	if message.text.count(' ') > 0:
		i = message.text.index(' ')
		mensaje = message.text[i+1:]
	try:
		t = Thread(target=countdownm, args=(int(mensaje), message.chat.id))
		t.start()
	except:
		bot.send_message(message.chat.id, "Necesito que me digas cuantos segundos de cuenta atrás quieres")


"""
Para creación de eventos he utilizado APScheduler. Lo interesante de esta función es el
"register_next_step_handler()", esto aún no tengo muy claro como va exactamente, pero
le pasas el mensaje asociado y el método que tiene que disparar a continuación, y entra
en un proceso de conversación por pasos. En este caso el bot va realizando preguntas
y registrando la respuesta para poder generar la tarea programada.
"""
@bot.message_handler(commands=['newevent'])
def newevent(message):
	bot.send_message(message.chat.id, "Veo que quieres crear un evento al que seguramente no pueda ir...")
	msg = bot.send_message(message.chat.id, "¿Cómo se llama el evento?")
	bot.register_next_step_handler(msg, eventname)


"""
Como se dijo al principio, el bot puede ejecutar cosas sin que sea en comando, para ello
los parámetros del decorador son los siguietes. (pone Sonia porque mi bot se llamaba Sonia)
"""
@bot.message_handler(func=lambda message: True)
def helloWay(message):
	#datos(message)
	if (message.text.lower() == "hola") or (message.text.lower() == "hola sonia") or (message.text.lower() == "hola, sonia"):
		text = "Hola, " + str(message.from_user.first_name.encode('utf-8'))
		bot.send_message(message.chat.id, text)
	if 	message.text.lower() == "sonia":
		bot.send_message(message.chat.id, "¿Qué?")

"""
Tontería del día, pues claro que el bot puede mandar stickers, pero hasta donde sé, necesita el id
del sticker y la única forma de conseguirlo es usar el siguiente decorador para que el bot
capture el sticker y haga cosas, entre ellas imprimir el id para que lo conozcas. En esta versión
lo imprime por consola, pero puedes hacer que te lo envie en mensaje de chat y una vez lo tienes
puedes usar la función send_sticker(idchat,idsticker) para hacer el gamba.
"""
@bot.message_handler(content_types=['sticker'])
def helloWay2(message):
	print (message.sticker)
	#bot.send_sticker(-1145466928, u'BQADBAADbA0AAhXc8gJGl1goxph6PwI')



def countdown(seg, id, mensaje = "Ya han pasado los "):
	time.sleep(seg)
	bot.send_message(id, mensaje + str(seg) + " segundos")

def countdownm(seg, id, mensaje = "Ya han pasado los "):
	while seg > 0:
		if ((seg) > 10):
			bot.send_message(id, str(seg))
			if seg - 5 >= 10:
				time.sleep(5)
				seg -= 5
			else:
				time.sleep(seg-10)
				seg = 10

		else:
			bot.send_message(id, str(seg))
			time.sleep(1)
			seg -= 1
	bot.send_message(id, "0!!!!!!!!!!!!!!!")
	bot.send_sticker(id, u'BQADBAAD9gADETZyATbRLSUVxInbAg')

##########################################
### METODOS DE PROGRAMACIÓN DE EVENTOS ###
##########################################

# Programación generica


def eventname(message):
	try:
		tupla[message.chat.id] = {}
		tupla[message.chat.id]["id"] = message.text
		bot.send_message(message.chat.id, "Necesito que me digas cuándo mandar el mensaje del evento, siguiendo este formato:")
		bot.send_message(message.chat.id, "<año> <mes> <día> <hora> <minuto>")
		msg = bot.send_message(message.chat.id, "Es importante separar con espacios, un ejemplo sería: 2017 8 5 16 0")
		bot.register_next_step_handler(msg, eventdate)

	except Exception as e:
		bot.send_sticker(message.chat.id, u'BQADBAADHAEAAhE2cgFYepVIFraC8gI')
		time.sleep(2)
		bot.reply_to(message, '¡Ya la has liado! Ha explotado el proceso')


def eventdate(message):
	try:
		text = message.text.lower().split(' ')
		tupla[message.chat.id]["datetime"] = datetime.datetime(int(text[0]), int(text[1]), int(text[2]), int(text[3]), int(text[4]))
		msg = bot.send_message(message.chat.id, "Bien, ¿qué mensaje quieres que mande?")
		bot.register_next_step_handler(msg, eventmessage)

	except Exception as e:
		bot.send_sticker(message.chat.id, u'BQADBAADHAEAAhE2cgFYepVIFraC8gI')
		time.sleep(2)
		bot.reply_to(message, '¡Ya la has liado! Ha explotado el proceso')


def eventmessage(message):
	try:
		tupla[message.chat.id]["message"] = message.text
		newjob(message)
		bot.send_message(message.chat.id, "¡Evento creado!")

	except Exception as e:
		bot.send_sticker(message.chat.id, u'BQADBAADHAEAAhE2cgFYepVIFraC8gI')
		time.sleep(2)
		bot.reply_to(message, '¡Ya la has liado! Ha explotado el proceso')

# Se lanza la tarea programada
def newjob(message):
	scheduler.add_job(sendmensajegerico, run_date=(tupla[message.chat.id]['datetime']), args=[(message.chat.id), (tupla[message.chat.id]['message'])], id=tupla[message.chat.id]['id'], replace_existing=True)

def sendmensajegerico(destinatario, text):
	bot.send_message(destinatario, text)



print ("i'm ready!")
bot.polling()	# Función que ejecuta el bot para escuchar mensajes.