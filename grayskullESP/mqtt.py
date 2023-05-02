import ujson
import binascii
import time
from umqtt.simple import MQTTClient
from common import get_mqtt_cfg
from common import get_network_cfg
from common import get_machine_id
from sensor_collect import collect
from mqtt_as import MQTTClient
from mqtt_local import config
import uasyncio as asyncio
import machine


####################################################################


# Received messages from subscriptions will be delivered to this callback
def sub_callback(topic,msg):
    if msg.decode() == "topic goes here":
        print("your code goes here")


def reset():
    print("Resetting...")
    time.sleep(5)
    machine.reset()

   
def mqtt_send_loop():    
    mqtt_config = get_mqtt_cfg()
    network_config = get_network_cfg()
    async_config = {}
    async_config['user'] = mqtt_config['user']
    async_config['password'] = mqtt_config['password']
    async_config['server'] = mqtt_config['server']
    async_config['port'] = mqtt_config['port']
    async_config['topic'] = mqtt_config['topic']
    async_config['ssl'] = mqtt_config['ssl']
    async_config['ssl_params'] = {"server_hostname": async_config['server']}
    async_config['ssid'] = network_config['ssid']
    async_config['wifi_pw'] = network_config['password']
    async_config["queue_len"] = 1
    async_config['clean'] = True
    async_config['keepalive'] = 30
    async_config['client_id'] = get_machine_id().encode()
    async_config['response_time'] = 10
    async_config['max_repubs'] = 4
    async_config['clean_init'] = True
    async_config['ping_interval'] = 0    
    will_statement = str(get_machine_id()) + " has lost connection."
    async_config['will'] = [async_config['topic'], will_statement, False, 0]
    
    
    async def messages(client):  # Respond to incoming messages
        async for topic, msg, retained in client.queue:
            print((topic, msg, retained))
            

    async def up(client):  # Respond to connectivity being (re)established
        while True:
            await client.up.wait()  # Wait on an Event
            client.up.clear()
            await client.subscribe(async_config['topic'], 1)  # renew subscriptions


    async def main(client):
        await client.connect()
        for coroutine in (up, messages):
            asyncio.create_task(coroutine(client))
        while True:
            await asyncio.sleep(1)
            sensor_data_input=collect()
            sensor_data_input = ujson.dumps(sensor_data_input).encode()
            # If WiFi is down the following will pause for the duration.
            await client.publish(async_config['topic'], sensor_data_input, qos = 1)
            
    
    MQTTClient.DEBUG = True  # Optional: print diagnostic messages
    client = MQTTClient(async_config)
    try:
        sensor_data=collect()      
        asyncio.run(main(client))
    finally:
        client.close()  # Prevent LmacRxBlk:1 errors