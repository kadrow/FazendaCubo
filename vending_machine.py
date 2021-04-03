# To begin, install the libraries that we need to use:
# pip install adafruit-io --user
# pip install adafruit-circuitpython-dht --user 

# import standard python modules.
import time

# import adafruit dht library.
#import adafruit_DHT

# import Adafruit IO REST client.
from Adafruit_IO import Client, Feed

# Delay in-between sensor readings, in seconds.
DHT_READ_TIMEOUT = 5

# Pin connected to DHT11 data pin - @Put here whats is the right number
DHT_DATA_PIN = 26

# Set Adafruit IO key.
# the key is secret so not publish this when we publish this code!
ADAFRUIT_IO_KEY = 'aio_XnQJ04ynzpJ9HdiiZYuSOlcRH0Zm'

# Set  Adafruit IO username.
ADAFRUIT_IO_USERNAME = 'diogocrlopes'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Set up Adafruit IO Feeds.
temperature_feed = aio.feeds('temperature')
humidity_feed = aio.feeds('humidity')
luminosity_feed = aio.feeds('luminosity')
# Set up DHT11 Sensor.
#dht11_sensor = Adafruit_DHT.DHT11

while True:
    #For when we put the Raspberry in the loop:
    #humidity, temperature = Adafruit_DHT.read_retry(dht11_sensor, DHT_DATA_PIN)
    humidity,temperature,luminosity = 30,25,620

    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
        # Send humidity and temperature feeds to Adafruit IO
        temperature = '%.2f'%(temperature)
        humidity = '%.2f'%(humidity)
        aio.send(temperature_feed.key, str(temperature))
        aio.send(humidity_feed.key, str(humidity))
        aio.send(luminosity_feed.key, str(luminosity))
    else:
        print('Error in the read of sensors')
    # Timeout to avoid flooding Adafruit IO
    time.sleep(DHT_READ_TIMEOUT)