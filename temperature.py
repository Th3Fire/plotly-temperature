import plotly.plotly as py
import json
from time import sleep
import RPi.GPIO as GPIO
import datetime
from ds18b20 import DS18B20

with open('config.json') as config_file:
    plotly_user_config = json.load(config_file)

py.sign_in(plotly_user_config["plotly_username"], plotly_user_config["plotly_api_key"])

url = py.plot([
    {
        'x': [], 'y': [], 'type': 'scatter',
        'stream': {
            'token': plotly_user_config['plotly_streaming_tokens'][0],
            'maxpoints': 200
        }
    }], filename='Raspberry Pi Streaming Example Values')

print "View your streaming graph here: ", url

# temperature sensor middle pin connected channel 0 of mcp3008



stream = py.Stream(plotly_user_config['plotly_streaming_tokens'][0])
stream.open()

#the main sensor reading and plotting loop
while True:
    sensor = DS18B20()
    time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    temperatures = sensor.get_temperatures([DS18B20.DEGREES_C, DS18B20.DEGREES_F, DS18B20.KELVIN])
    print("Degrees Celsius: %f" % temperatures[0])

    temp_C = "%.1f" % temperatures[0]
    print("Degrees Celsius: %s" % temp_C)

    # write the data to plotly
    stream.write({'x': time, 'y': temp_C})

    # delay between stream posts
    sleep(5)