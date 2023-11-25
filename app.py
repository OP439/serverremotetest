from flask import Flask, request, jsonify, redirect, flash, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import ssl

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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
      # socketio.emit('incomeing', data='mqtttoflask')
   elif message.topic == 'rotateprinterackflask':
      flash('Rotate printer command acknowledged in lab - monitor rotation graph')
   elif message.topic == 'takepictureackflask':
      flash('Take picture command acknowledged in lab - may take time to upload')
      payload = message.payload.decode()
      print(payload)

# @socketio.on('incomeing')
# def publish_message_6():
#    flash('heel')
#    print('ehthefd')

#test route
@app.route('/publish', methods=['POST'])
def publish_message():
   request_data = request.get_json()
   publish_result = mqtt_client.publish(request_data['topic'], request_data['msg'])
   return jsonify({'code': publish_result[0]})

@app.route('/toggleheater', methods=['GET'])
def publish_message_2():
   publish_result = mqtt_client.publish('toggleheaterflask', 'toggleheaterflask')#mqtt specifc, must be kept
   flash('Heater toggled (hopefully) - monitor temperatures, wait for acknowledge')
   return redirect('/')

@app.route('/rotateprinter', methods=['GET'])
def publish_message_3():
   publish_result = mqtt_client.publish('rotateprinterflask', 'rotateprinterflask')#mqtt specifc, must be kept
   flash('Printer rotated (hopefully) - monitor position on graphs, wait for acknowledge')
   return redirect('/')

@app.route('/takepicture', methods=['GET'])
def publish_message_4():
   publish_result = mqtt_client.publish('takepictureflask', 'takepictureflask')#mqtt specifc, must be kept
   flash('Picture taken (hopefully) - monitor datetime below picture, wait for acknowledge')
   return redirect('/')

@app.route("/")
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5023, use_reloader="False", ssl_context='adhoc')


