# To begin, install the libraries that we need to use:
# pip install adafruit-io --user
# pip install adafruit-circuitpython-dht --user 


# import standard python modules.
import sys
import time
import RPi.GPIO as GPIO
import math

# import adafruit dht library.
import Adafruit_DHT

# import Adafruit IO REST client.
from Adafruit_IO import MQTTClient

# Delay in-between sensor readings, in seconds.
DHT_READ_TIMEOUT = 10

# Pin connected to DHT11, Luminosity and PUM data pin - @Put here whats is the right number
DHT_DATA_PIN = 17
PUMP_DATA_PIN = 37
LDR_DATA_PIN = 7
LIGHT_DATA_PIN = 13
FAN_DATA_PIN = 15

#Setup of GPIO to work with BOARD PIN mode and OUTPUT
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(PUMP_DATA_PIN,GPIO.OUT)
GPIO.setup(LIGHT_DATA_PIN,GPIO.OUT)
GPIO.setup(FAN_DATA_PIN,GPIO.OUT)

# Set Adafruit IO key.
# the key is secret so not publish this when we publish this code!
ADAFRUIT_IO_KEY = '****'

# Set  Adafruit IO username.
ADAFRUIT_IO_USERNAME = '****'

#Set the ID of the feed to subscribe to for updates.
PUMP_ID = 'pump'
LIGHT_ID = 'light'
FAN_ID = 'fan'

# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to topic changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Listening for changes on ', PUMP_ID)
    print('Listening for changes on ', LIGHT_ID)
    print('Listening for changes on ', FAN_ID)
    # Subscribe to changes on a group, `PUMP_ID`
    client.subscribe(PUMP_ID)
    client.subscribe(LIGHT_ID)
    client.subscribe(FAN_ID)
    
def subscribe(client, userdata, mid, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print('Subscribed to {0} with QoS {1}'.format(PUMP_ID, granted_qos[0]))
    print('Subscribed to {0} with QoS {1}'.format(LIGHT_ID, granted_qos[0]))
    print('Subscribed to {0} with QoS {1}'.format(FAN_ID, granted_qos[0]))
    
def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, topic_id, payload):
    # Message function will be called when a subscribed topic has a new value.
    # The topic_id parameter identifies the topic, and the payload parameter has
    # the new value.
    print('Topic {0} received new value: {1}'.format(topic_id, payload))
    if topic_id == 'pump':
        if payload == 'OFF':
            GPIO.output(PUMP_DATA_PIN, GPIO.HIGH)
        elif payload == 'ON':
            GPIO.output(PUMP_DATA_PIN, GPIO.LOW)
    if topic_id == 'light':
        if payload == 'OFF':
            GPIO.output(LIGHT_DATA_PIN, GPIO.HIGH)
        elif payload == 'ON':
            GPIO.output(LIGHT_DATA_PIN, GPIO.LOW)
    if topic_id == 'fan':
        if payload == 'OFF':
            GPIO.output(FAN_DATA_PIN, GPIO.HIGH)
        elif payload == 'ON':
            GPIO.output(FAN_DATA_PIN, GPIO.LOW)
# Create an instance of MQTT client

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message
client.on_subscribe  = subscribe
# Connect to the Adafruit IO server.
client.connect()

# Now the program needs to use a client loop function to ensure messages are
# sent and received.The program going to run a thread in the background so you can continue
# doing things.
client.loop_background()

# Now send new values every 5 seconds.
print('Publishing a new message every 15 seconds (press Ctrl-C to quit)...')

# Set up Adafruit IO Feeds.
temperature_feed = 'temperature'
humidity_feed = 'humidity'
luminosity_feed = 'luminosity'

# Set up DHT11 Sensor.
dht11_sensor = Adafruit_DHT.DHT11

def rc_time (LDR_DATA_PIN):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(LDR_DATA_PIN, GPIO.OUT)
    GPIO.output(LDR_DATA_PIN, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(LDR_DATA_PIN, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(LDR_DATA_PIN) == GPIO.LOW):
        count += 1

    return count

def evaluate_luminosity(luminosity):
    if luminosity <= 90:
        leds_on = 4
    elif luminosity > 90 and luminosity <= 110:
        leds_on = 3
    elif luminosity > 110 and luminosity <= 130:
        leds_on = 2
    elif luminosity > 130 and luminosity <= 200:
        leds_on = 1
    else:
        leds_on = 0
    return leds_on

while True:
    #For when we put the Raspberry in the loop:
    humidity, temperature = Adafruit_DHT.read_retry(dht11_sensor, DHT_DATA_PIN)
   
    luminosity = rc_time(LDR_DATA_PIN) #returns the time it takes the capacitor to charge to 3/4
    leds_on = evaluate_luminosity(luminosity)


    
    if humidity is not None and temperature is not None and humidity < 100:
        print('Temp={0:0.1f}*C Humidity={1:0.1f}% Luminosity={2:0.1f} Leds ON = {3:0.1f}'.format(temperature, humidity, luminosity, leds_on))
        #print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
        # Send humidity and temperature feeds to Adafruit IO
        temperature = '%.2f'%(temperature)
        humidity = '%.2f'%(humidity)
        #luminosity = '%.2f'%(luminosity)
        
        client.publish(temperature_feed, str(temperature))
        client.publish(humidity_feed, str(humidity))
        client.publish(luminosity_feed, str(leds_on))
        
    else:
        print('Error in the read of sensors')
        
    # Timeout to avoid flooding Adafruit IO
    time.sleep(DHT_READ_TIMEOUT)
