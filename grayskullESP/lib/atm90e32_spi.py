from machine import Pin, SPI
import utime
import struct

# atm90e32 Datasheet: http://ww1.microchip.com/downloads/en/devicedoc/Atmel-46003-SE-M90E32AS-Datasheet.pdf
# atm90e32 Uses 15 bit addresses, unlike many SPI devices which utilize 7 bit addresses, and read/write data 
# is fixed at 16 bits, so we will always operate on two byte chunks.

class atm90e32_spi:
	SPI_WRITE = 0
	SPI_READ = 1

	def __init__(self, sckPin=Pin(18), mosiPin=Pin(23), misoPin=Pin(19)):
		# MicroPython ESP8266 SPI Reference: https://docs.micropython.org/en/latest/esp8266/quickref.html#hardware-spi-bus
		# MicroPython ESP32 SPI Reference: https://docs.micropython.org/en/latest/esp32/quickref.html#hardware-spi-bus
		self.spi = SPI(1, baudrate=200000, polarity=1, phase=1, bits=8, firstbit=0, sck=sckPin, mosi=mosiPin, miso=misoPin)

	#####################################################################################
	# Base SPI request
	def _spi_raw(self, csPin, rw, address, value):
		if rw != self.SPI_READ and rw != self.SPI_WRITE:
			return -1 # Check that 'rw' is a valid value
		if address < 0 or address > 0xFFFF:
			return -2 # Check that 'address' is a valid value
		if value < 0 or value > 0xFFFF:
			return -3 # Check that 'value' is a valid value

		address |= rw << 15 # Set RW bit flag

		csPin.off() # Enable the chip select
		utime.sleep_us(10)

		self.spi.write(struct.pack('>H', address)) # Send the address
		# utime.sleep_us(4) # This was in original code, not immediately seeing a requirement in the datasheet, and we're not running SPI very quickly.

		if (rw == self.SPI_READ):
			result = struct.unpack('>H', self.spi.read(2))[0]
		else:
			self.spi.write(struct.pack('>H', value))
			result = 0

		csPin.on() # Disable chip select, we're done with this transaction

		return result

	#####################################################################################
	# Read a 16bit register
	def readRegister(self, csPin, address):
		return self._spi_raw(csPin, self.SPI_READ, address, 0xFFFF)
		
	#####################################################################################
	# Read a 16bit register, Two's Complement Format
	def readRegister2C(self, csPin, address):
		value = self._spi_raw(csPin, self.SPI_READ, address, 0xFFFF)
		return value - int((value << 1) & 2**16)

	#####################################################################################
	# Write a 16bit register
	def writeRegister(self, csPin, address, value):
		return self._spi_raw(csPin, self.SPI_WRITE, address, value)

	#####################################################################################
	# Read a 32bit register, Two's Complement Format
	def readLongRegister2C(self, csPin, address_high, address_low):
		value_h = self._spi_raw(csPin, self.SPI_READ, address_high, 0xFFFF)
		value_l = self._spi_raw(csPin, self.SPI_READ, address_low, 0xFFFF)
		value = (value_h << 16) | value_l
		return value - int((value << 1) & 2**32)
