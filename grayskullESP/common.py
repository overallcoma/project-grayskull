import common
import ujson
import binascii

import machine


def get_machine_id():
    machine_unique_hex = machine.unique_id()
    machine_unique_bytestring = binascii.hexlify(machine_unique_hex)
    machine_unique_string = machine_unique_bytestring.decode()
    return machine_unique_string


def get_mqtt_cfg():
    config_file = open("config.json")
    config = ujson.load(config_file)    
    mqtt_config = config["nodeConfig"]["mqtt"]
    return mqtt_config


def get_network_cfg():
    config_file = open("config.json")
    config = ujson.load(config_file)
    config = config['nodeConfig']['network']
    return config