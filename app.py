from flask import Flask, request, jsonify, redirect, flash, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import ssl
import time
import datetime
import json
#from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#app.wsgi_app = ProxyFix(
#	app.wsgi_app, x_for=1, x_host=1
#)

# app.config['MQTT_BROKER_URL'] = 'oppi1.local'
# app.config['MQTT_BROKER_PORT'] = 1883

app.config['MQTT_BROKER_URL'] = 'a2m1ood9u6x4se-ats.iot.us-east-1.amazonaws.com'
app.config['MQTT_BROKER_PORT'] = 8883
app.config['MQTT_TLS_ENABLED'] = True
app.config['MQTT_TLS_CA_CERTS'] = 'certs2/AmazonRootCA1.pem'
app.config['MQTT_TLS_CERTFILE'] = 'certs2/df2e21f240cf0b90d99c30c5b4602548ed414a1696a0f1346a7609e85bd2715e-certificate.pem.crt'
app.config['MQTT_TLS_KEYFILE'] = 'certs2/df2e21f240cf0b90d99c30c5b4602548ed414a1696a0f1346a7609e85bd2715e-private.pem.key'
app.config['MQTT_TLS_VERSION'] = ssl.PROTOCOL_TLSv1_2

topic = "fromflask"

payload = 'wrong payload'

mqtt_client = Mqtt(app)

# socketio = SocketIO(app)

# @socketio.on('publish')

### Getting runtime errors when trying to process information coming in as an MQTT message with HTTPS stuff
### MQTT is translated into HTTPS by the AWS IoT Core upstream instead.

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   mqtt_client.subscribe('toggleheaterackflask')
   mqtt_client.subscribe('rotateprinterackflask')
   mqtt_client.subscribe('takepictureackflask')

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):

   if message.topic == 'toggleheaterackflask':
      #flash('Heater toggle command acknowledged in lab - still monitor temps!')
      #print(payload)
      print('heeh')
      with open("templates/incominglogs.txt", "a") as file1:
      # Writing data to a file
         file1.write(str(datetime.datetime.fromtimestamp(time.time()))+" Toggle Heater Command Acknowledged \n")
      # socketio.emit('incomeing', data='mqtttoflask')
      time.sleep(1)
   elif message.topic == 'rotateprinterackflask':
      print('rotateprinterack')
      with open("templates/incominglogs.txt", "a") as file1:
      # Writing data to a file
         file1.write(str(datetime.datetime.fromtimestamp(time.time()))+" Rotate Printer Command Acknowledged \n")
   elif message.topic == 'takepictureackflask':
      with open("templates/incominglogs.txt", "a") as file1:
      # Writing data to a file
         file1.write(str(datetime.datetime.fromtimestamp(time.time()))+" Take Picture Command Acknowledged \n")
      #### Write to a file the file name of the photo most recently taken
      payload = message.payload.decode()
      with open("templates/picturefilename.txt", "a") as file2:
      # Writing data to a file
         file2.write(str(payload)+"\n")
         file2.write(str(json.loads(str(payload))['takepictureack'])+'.jpg\n')
   return redirect('/')





# @socketio.on('incomeing')
# def publish_message_6():
#    flash('heel')
#    print('ehthefd')

### Test route
# @app.route('/publish', methods=['POST'])
# def publish_message():
#    request_data = request.get_json()
#    publish_result = mqtt_client.publish(request_data['topic'], request_data['msg'])
#    return jsonify({'code': publish_result[0]})


### URL confirmation route for AWS MQTT HTTPS Translator
# @app.route('/', methods=['POST'])
# def publish_message():
#    print(dict(request.headers))
#    request_data = request.get_json()
#    print(request_data)
#    with open("templates/pythonlogs.txt", "a") as file1:
#       # Writing data to a file
#       file1.write(str(datetime.datetime.fromtimestamp(time.time()))+str(request.headers))
#    #publish_result = mqtt_client.publish(request_data['topic'], request_data['msg'])
#    return 4




### Routes to handle outgoing messages from the server to AWS IoT Core
@app.route('/toggleheater', methods=['GET'])
def publish_message_2():
   publish_result = mqtt_client.publish('toggleheaterflask', 'toggleheaterflask')#mqtt specifc, must be kept
   with open("templates/logs.txt", "a") as file1:
      # Writing data to a file
      file1.write(str(datetime.datetime.fromtimestamp(time.time()))+" Heater Toggle Command \n")
   return redirect('/')

@app.route('/rotateprinter', methods=['GET'])
def publish_message_3():
   publish_result = mqtt_client.publish('rotateprinterflask', 'rotateprinterflask')#mqtt specifc, must be kept
   with open("templates/logs.txt", "a") as file1:
      # Writing data to a file
      file1.write(str(datetime.datetime.fromtimestamp(time.time()))+" Printer Rotate Command \n")
   return redirect('/')

@app.route('/takepicture', methods=['GET'])
def publish_message_4():
   publish_result = mqtt_client.publish('takepictureflask', 'takepictureflask')#mqtt specifc, must be kept
   with open("templates/logs.txt", "a") as file1:
      # Writing data to a file
      file1.write(str(datetime.datetime.fromtimestamp(time.time()))+" Take Picture Command \n")
   return redirect('/')

### Routes to handle incoming requests from AWS IoT core
### Local server acknowlodging message received 
### Also used to get latest picture from S3 bucket
### Too difficult to handle with confirming ownership of url - mqtt writing to file works better
# @app.route('/toggleheaterack', methods=['GET'])
# def toggleheaterackfn():
#    with open("templates/logs.txt", "a") as file1:
#       # Writing data to a file
#       file1.write(str(datetime.datetime.fromtimestamp(time.time()))+" Heater Toggle Command Acknowledged \n")
#    return redirect('/')

# @app.route('/rotateprinterack', methods=['GET'])
# def rotateprinterackfn():
#    with open("templates/logs.txt", "a") as file1:
#       # Writing data to a file
#       file1.write(str(datetime.datetime.fromtimestamp(time.time()))+" Printer Rotate Command Acknowledged \n")
#    return redirect('/')

# @app.route('/takepictureack', methods=['GET'])
# def takepictureackfn():
#    with open("templates/logs.txt", "a") as file1:
#       # Writing data to a file
#       file1.write(str(datetime.datetime.fromtimestamp(time.time()))+" Take Picture Command Acknowledged \n")
#    return redirect('/')


### Route to communicate with the script that is running tests automatically
@app.route('/autotimer')
def timetonextfromscript():
   timetonext_sec = float(request.args.get('timetonext'))
   datetimeatnext = time.time() + timetonext_sec
   readable_time = datetime.datetime.fromtimestamp(datetimeatnext)
   with open("templates/timetonext.txt", "a") as file1:
      # Writing data to a file
      file1.write(str(readable_time)+' \n')
   return redirect('/')


### Base Welcome Route
@app.route("/")
def hello_world():
    ### testing text
   #outgoing logs
   f = open('templates/logs.txt', 'r')
   g = f.readlines()[-1]
   #incoming logs
   f2 = open('templates/incominglogs.txt', 'r')
   g2 = f2.readlines()[-1]
   #photo filename
   f3 = open('templates/picturefilename.txt', 'r')
   g3 = f3.readlines()[-1][:-1]#ignore the escpae n for new line
   g31 = "https://oppiphotos.s3.amazonaws.com/dump/file/"+g3

   f4 = open('templates/timetonext.txt', 'r')
   g4 = f4.readlines()[-1]   

   return render_template('index.html', n=g ,n2=g2, n3=g31, n4=g4)


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5023, use_reloader="False", ssl_context='adhoc')
#formerly just app not app.wsgi_app

