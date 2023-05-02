from machine import Pin
import math
import struct
from atm90e32_reg import atm90e32_reg
import utime

class atm90e32_ctl:

	def __init__(self, linefreq, pgagain, ugain, igainA, igainB, igainC, csPin, spiLink, initDelay=True):
		self._linefreq = linefreq
		self._pgagain = pgagain
		self._ugain = ugain
		self._igainA = igainA
		self._igainB = igainB
		self._igainC = igainC
		self._spiLink = spiLink

		self._registers = atm90e32_reg()

		# Chip select pin
		self._csPin = Pin(csPin, Pin.OUT)
		self._csPin.on()

		self._init_config()
		
		if initDelay: # Chip requires a bit less than 200mS after init for readings to stabilize
			utime.sleep_ms(200)

	def _init_config(self):
		if (self._linefreq == 4231): # North America power frequency
			FreqHiThresh = 61 * 100
			FreqLoThresh = 59 * 100
			sagV = 90
		else:
			FreqHiThresh = 51 * 100
			FreqLoThresh = 49 * 100
			sagV = 190

		fvSagTh = (sagV * 100 * 1.41421356) / (2 * self._ugain / 32768) # Voltage Sag threshhold in RMS (1.41421356)
		vSagTh = self._round_number(fvSagTh)			# convert to int for sending to the atm90e32.

		self._spiLink.writeRegister(self._csPin, self._registers.SoftReset, 0x789A)		# Perform soft reset
		self._spiLink.writeRegister(self._csPin, self._registers.CfgRegAccEn, 0x55AA)	# enable register config access
		self._spiLink.writeRegister(self._csPin, self._registers.MeterEn, 0x0001)		# Enable Metering

		self._spiLink.writeRegister(self._csPin, self._registers.SagTh, vSagTh)			# Voltage sag threshold
		self._spiLink.writeRegister(self._csPin, self._registers.FreqHiTh, FreqHiThresh)	# High frequency threshold - 61.00Hz
		self._spiLink.writeRegister(self._csPin, self._registers.FreqLoTh, FreqLoThresh)	# Lo frequency threshold - 59.00Hz
        
		self._spiLink.writeRegister(self._csPin, self._registers.EMMIntEn0, 0xB76F)		# Enable interrupts
		self._spiLink.writeRegister(self._csPin, self._registers.EMMIntEn1, 0xDDFD)		# Enable interrupts
		self._spiLink.writeRegister(self._csPin, self._registers.EMMIntState0, 0x0001)	# Clear interrupt flags
		self._spiLink.writeRegister(self._csPin, self._registers.EMMIntState1, 0x0001)	# Clear interrupt flags
		self._spiLink.writeRegister(self._csPin, self._registers.ZXConfig, 0x0A55)		# ZX2, ZX1, ZX0 pin config

		# Set metering config values (CONFIG)
		self._spiLink.writeRegister(self._csPin, self._registers.PLconstH, 0x0861)		# PL Constant MSB (default) - Meter Constant = 3200 - PL Constant = 140625000
		self._spiLink.writeRegister(self._csPin, self._registers.PLconstL, 0xC468)		# PL Constant LSB (default) - this is 4C68 in the application note, which is incorrect
		self._spiLink.writeRegister(self._csPin, self._registers.MMode0, self._linefreq)	# Mode Config (frequency set in main program)
		self._spiLink.writeRegister(self._csPin, self._registers.MMode1, self._pgagain)	# PGA Gain Configuration for Current Channels - 0x002A (x4) # 0x0015 (x2) # 0x0000 (1x)
		self._spiLink.writeRegister(self._csPin, self._registers.PStartTh, 0x0AFC)		# Active Startup Power Threshold - 50% of startup current = 0.9/0.00032 = 2812.5
		self._spiLink.writeRegister(self._csPin, self._registers.QStartTh, 0x0AEC)		# Reactive Startup Power Threshold
		self._spiLink.writeRegister(self._csPin, self._registers.SStartTh, 0x0000)		# Apparent Startup Power Threshold
		self._spiLink.writeRegister(self._csPin, self._registers.PPhaseTh, 0x00BC)		# Active Phase Threshold = 10% of startup current = 0.06/0.00032 = 187.5
		self._spiLink.writeRegister(self._csPin, self._registers.QPhaseTh, 0x0000)		# Reactive Phase Threshold
		self._spiLink.writeRegister(self._csPin, self._registers.SPhaseTh, 0x0000)		# Apparent  Phase Threshold

        # Set metering calibration values (CALIBRATION)
		self._spiLink.writeRegister(self._csPin, self._registers.PQGainA, 0x0000)		# Line calibration gain
		self._spiLink.writeRegister(self._csPin, self._registers.PhiA, 0x0000)			# Line calibration angle
		self._spiLink.writeRegister(self._csPin, self._registers.PQGainB, 0x0000)		# Line calibration gain
		self._spiLink.writeRegister(self._csPin, self._registers.PhiB, 0x0000)			# Line calibration angle
		self._spiLink.writeRegister(self._csPin, self._registers.PQGainC, 0x0000)		# Line calibration gain
		self._spiLink.writeRegister(self._csPin, self._registers.PhiC, 0x0000)			# Line calibration angle
        
		self._spiLink.writeRegister(self._csPin, self._registers.PoffsetA, 0x0000)		# A line active power offset
		self._spiLink.writeRegister(self._csPin, self._registers.QoffsetA, 0x0000)		# A line reactive power offset
		self._spiLink.writeRegister(self._csPin, self._registers.PoffsetB, 0x0000)		# B line active power offset
		self._spiLink.writeRegister(self._csPin, self._registers.QoffsetB, 0x0000)		# B line reactive power offset
		self._spiLink.writeRegister(self._csPin, self._registers.PoffsetC, 0x0000)		# C line active power offset
		self._spiLink.writeRegister(self._csPin, self._registers.QoffsetC, 0x0000)		# C line reactive power offset

        # Set metering calibration values (HARMONIC)
		self._spiLink.writeRegister(self._csPin, self._registers.POffsetAF, 0x0000)		# A Fund. active power offset
		self._spiLink.writeRegister(self._csPin, self._registers.POffsetBF, 0x0000)		# B Fund. active power offset
		self._spiLink.writeRegister(self._csPin, self._registers.POffsetCF, 0x0000)		# C Fund. active power offset 
		self._spiLink.writeRegister(self._csPin, self._registers.PGainAF, 0x0000)		# A Fund. active power gain
		self._spiLink.writeRegister(self._csPin, self._registers.PGainBF, 0x0000)		# B Fund. active power gain
		self._spiLink.writeRegister(self._csPin, self._registers.PGainCF, 0x0000)		# C Fund. active power gain

        # Set measurement calibration values (ADJUST)
		self._spiLink.writeRegister(self._csPin, self._registers.UgainA, self._ugain)	# A Voltage rms gain
		self._spiLink.writeRegister(self._csPin, self._registers.IgainA, self._igainA)	# A line current gain
		self._spiLink.writeRegister(self._csPin, self._registers.UoffsetA, 0x0000)		# A Voltage offset
		self._spiLink.writeRegister(self._csPin, self._registers.IoffsetA, 0x0000)		# A line current offset
		
		self._spiLink.writeRegister(self._csPin, self._registers.UgainB, self._ugain)	# B Voltage rms gain
		self._spiLink.writeRegister(self._csPin, self._registers.IgainB, self._igainB)	# B line current gain
		self._spiLink.writeRegister(self._csPin, self._registers.UoffsetB, 0x0000)		# B Voltage offset
		self._spiLink.writeRegister(self._csPin, self._registers.IoffsetB, 0x0000)		# B line current offset
		
		self._spiLink.writeRegister(self._csPin, self._registers.UgainC, self._ugain)	# C Voltage rms gain
		self._spiLink.writeRegister(self._csPin, self._registers.IgainC, self._igainC)	# C line current gain
		self._spiLink.writeRegister(self._csPin, self._registers.UoffsetC, 0x0000)		# C Voltage offset
		self._spiLink.writeRegister(self._csPin, self._registers.IoffsetC, 0x0000)		# C line current offset

		self._spiLink.writeRegister(self._csPin, self._registers.CfgRegAccEn, 0x0000)	# end configuration

	def _round_number(self, f_num):
		if f_num - math.floor(f_num) < 0.5:
			return math.floor(f_num)
		return math.ceil(f_num)
        
	#####################################################################################
	@property
	def lastSpiData(self):
		reading = self._spiLink.readRegister(self._csPin, self._registers.LastSPIData)
		return reading
	#####################################################################################
	@property
	def sys_status0(self):
		reading = self._spiLink.readRegister(self._csPin, self._registers.EMMIntState0)
		return reading
	#####################################################################################
	@property
	def sys_status1(self):
		reading = self._spiLink.readRegister(self._csPin, self._registers.EMMIntState1)
		return reading
	#####################################################################################
	@property
	def meter_status0(self):
		reading = self._spiLink.readRegister(self._csPin, self._registers.EMMState0)
		return reading
	#####################################################################################
	@property
	def meter_status1(self):
		reading = self._spiLink.readRegister(self._csPin, self._registers.EMMState1)
		return reading


	#####################################################################################
	@property
	def line_voltageA(self):
		reading = self._spiLink.readRegister(self._csPin, self._registers.UrmsA)
		return reading / 100.0
	#####################################################################################
	@property
	def line_voltageB(self):
		reading = self._spiLink.readRegister(self._csPin, self._registers.UrmsB)
		return reading / 100.0
	#####################################################################################
	@property
	def line_voltageC(self):
		reading = self._spiLink.readRegister(self._csPin, self._registers.UrmsC)
		return reading / 100.0


	#####################################################################################
	@property
	def peak_voltageA(self):
		reading = self._spiLink.readRegister2C(self._csPin, self._registers.UPeakA)
		return reading * (self._ugain / 819200.0) # UPeak = UPeakRegValue x (Ugain / (100 x 2^13))
	#####################################################################################
	@property
	def peak_voltageB(self):
		reading = self._spiLink.readRegister2C(self._csPin, self._registers.UPeakB)
		return reading * (self._ugain / 819200.0) # UPeak = UPeakRegValue x (Ugain / (100 x 2^13))
	#####################################################################################
	@property
	def peak_voltageC(self):
		reading = self._spiLink.readRegister2C(self._csPin, self._registers.UPeakC)
		return reading * (self._ugain / 819200.0) # UPeak = UPeakRegValue x (Ugain / (100 x 2^13))


	#####################################################################################
	@property
	def line_current_total(self):
		reading = self._spiLink.readRegister(self._csPin, self._registers.IrmsN)
		return reading / 1000.0
	#####################################################################################
	@property
	def line_currentA(self):
		reading = self._spiLink.readRegister(self._csPin, self._registers.IrmsA)
		return reading / 1000.0
	#####################################################################################
	@property
	def line_currentB(self):
		reading = self._spiLink.readRegister(self._csPin, self._registers.IrmsB)
		return reading / 1000.0
	#####################################################################################
	@property
	def line_currentC(self):
		reading = self._spiLink.readRegister(self._csPin, self._registers.IrmsC)
		return reading / 1000.0


	#####################################################################################
	@property
	def peak_currentA(self):
		reading = self._spiLink.readRegister2C(self._csPin, self._registers.IPeakA)
		return reading * (self._igainA / 8192000.0) # IPeak = IPeakRegValue x (Igain / (1000 x 2^13))
	#####################################################################################
	@property
	def peak_currentB(self):
		reading = self._spiLink.readRegister2C(self._csPin, self._registers.IPeakB)
		return reading * (self._igainB / 8192000.0) # IPeak = IPeakRegValue x (Igain / (1000 x 2^13))
	#####################################################################################
	@property
	def peak_currentC(self):
		reading = self._spiLink.readRegister2C(self._csPin, self._registers.IPeakC)
		return reading * (self._igainC / 8192000.0) # IPeak = IPeakRegValue x (Igain / (1000 x 2^13))


	#####################################################################################
	@property
	def frequency(self):
		reading = self._spiLink.readRegister(self._csPin, self._registers.Freq)
		return reading / 100.0


	#####################################################################################
	@property
	def active_power_total(self):
		reading = self._spiLink.readLongRegister2C(self._csPin, self._registers.PmeanT, self._registers.PmeanTLSB)
		return reading * 0.00032
	#####################################################################################
	@property
	def active_powerA(self):
		reading = self._spiLink.readLongRegister2C(self._csPin, self._registers.PmeanA, self._registers.PmeanALSB)
		return reading * 0.00032
	#####################################################################################
	@property
	def active_powerB(self):
		reading = self._spiLink.readLongRegister2C(self._csPin, self._registers.PmeanB, self._registers.PmeanBLSB)
		return reading * 0.00032
	#####################################################################################
	@property
	def active_powerC(self):
		reading = self._spiLink.readLongRegister2C(self._csPin, self._registers.PmeanC, self._registers.PmeanCLSB)
		return reading * 0.00032
	
	
	#####################################################################################
	@property
	def reactive_power_total(self):
		reading = self._spiLink.readLongRegister2C(self._csPin, self._registers.QmeanT, self._registers.QmeanTLSB)
		return reading * 0.00032
	#####################################################################################
	@property
	def reactive_powerA(self):
		reading = self._spiLink.readLongRegister2C(self._csPin, self._registers.QmeanA, self._registers.QmeanALSB)
		return reading * 0.00032
	#####################################################################################
	@property
	def reactive_powerB(self):
		reading = self._spiLink.readLongRegister2C(self._csPin, self._registers.QmeanB, self._registers.QmeanBLSB)
		return reading * 0.00032
	#####################################################################################
	@property
	def reactive_powerC(self):
		reading = self._spiLink.readLongRegister2C(self._csPin, self._registers.QmeanC, self._registers.QmeanCLSB)
		return reading * 0.00032


	#####################################################################################
	@property
	def apparent_power_total(self):
		reading = self._spiLink.readLongRegister2C(self._csPin, self._registers.SAmeanT, self._registers.SAmeanTLSB)
		return reading * 0.00032
	#####################################################################################
	@property
	def apparent_powerA(self):
		reading = self._spiLink.readLongRegister2C(self._csPin, self._registers.SmeanA, self._registers.SmeanALSB)
		return reading * 0.00032
	#####################################################################################
	@property
	def apparent_powerB(self):
		reading = self._spiLink.readLongRegister2C(self._csPin, self._registers.SmeanB, self._registers.SmeanBLSB)
		return reading * 0.00032
	#####################################################################################
	@property
	def apparent_powerC(self):
		reading = self._spiLink.readLongRegister2C(self._csPin, self._registers.SmeanC, self._registers.SmeanCLSB)
		return reading * 0.00032


	#####################################################################################
	@property
	def power_factor_total(self):
		reading = self._spiLink.readRegister2C(self._csPin, self._registers.PFmeanT)
		return reading * 0.001
	#####################################################################################
	@property
	def power_factorA(self):
		reading = self._spiLink.readRegister2C(self._csPin, self._registers.PFmeanA)
		return reading * 0.001
	#####################################################################################
	@property
	def power_factorB(self):
		reading = self._spiLink.readRegister2C(self._csPin, self._registers.PFmeanB)
		return reading * 0.001
	#####################################################################################
	@property
	def power_factorC(self):
		reading = self._spiLink.readRegister2C(self._csPin, self._registers.PFmeanC)
		return reading * 0.001