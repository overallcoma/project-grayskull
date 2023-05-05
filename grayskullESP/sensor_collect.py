from atm90e32_spi import atm90e32_spi
from atm90e32_ctl import atm90e32_ctl
import ujson
from common import get_machine_id


def collect():
    spiConn = atm90e32_spi()
    config_file = open("config.json")
    config = ujson.load(config_file)
    sensors_config = config["nodeConfig"]["sensors"]

    linefreq = sensors_config["linefreq"]
    pgagain = sensors_config["pgagain"]
    ugain = sensors_config["ugain"]

    def amps_calc(watts, volts):
        amps = int(watts) / int(volts)
        return amps

    def get_sensor_status(sensornumber):
        sensornumber = str(sensornumber)
        sensor_config = sensors_config[sensornumber]
        gain = sensor_config["gain"]
        pin = sensor_config["pin"]
        collected_data = atm90e32_ctl(linefreq, pgagain, ugain, gain, gain, gain, pin, spiConn)
        watts = collected_data.apparent_power_total
        volts = collected_data.line_voltageA
        amps = amps_calc(watts,volts)
        status = {
            "watts": watts,
            "volts": volts,
            "amps": amps
            } 
        return status

    sensor_output = []

    for key, value in sensors_config.items():
        if "sensor" in key:
            
            if value["name"] == "NA":
                continue
            
            sensor_id = str(key)
            output_dict = get_sensor_status(sensor_id)
            output_dict["name"] = value["name"]
            sensor_output.append(output_dict)
    return(sensor_output)
