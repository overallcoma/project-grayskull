class atm90e32_reg:
	def __init__(self):
		#* STATUS REGISTERS *#
		self.MeterEn = 0x00   # Metering Enable
		self.ChannelMapI = 0x01  # Current Channel Mapping Configuration
		self.ChannelMapU = 0x02  # Voltage Channel Mapping Configuration
		self.SagPeakDetCfg = 0x05  # Sag and Peak Detector Period Configuration
		self.OVth = 0x06    # Over Voltage Threshold
		self.ZXConfig = 0x07   # Zero-Crossing Config
		self.SagTh = 0x08    # Voltage Sag Th
		self.PhaseLossTh = 0x09  # Voltage Phase Losing Th
		self.INWarnTh = 0x0A   # Neutral Current (Calculated) Warning Threshold
		self.OIth = 0x0B    # Over Current Threshold
		self.FreqLoTh = 0x0C  # Low Threshold for Frequency Detection
		self.FreqHiTh = 0x0D  # High Threshold for Frequency Detection
		self.PMPwrCtrl = 0x0E  # Partial Measurement Mode Power Control
		self.IRQ0MergeCfg = 0x0F  # IRQ0 Merge Configuration

		#* EMM STATUS REGISTERS *#
		self.SoftReset = 0x70  # Software Reset
		self.EMMState0 = 0x71  # EMM State 0
		self.EMMState1 = 0x72  # EMM State 1
		self.EMMIntState0 = 0x73   # EMM Interrupt Status 0
		self.EMMIntState1 = 0x74   # EMM Interrupt Status 1
		self.EMMIntEn0 = 0x75  # EMM Interrupt Enable 0
		self.EMMIntEn1 = 0x76  # EMM Interrupt Enable 1
		self.LastSPIData = 0x78  # Last Read/Write SPI Value
		self.CRCErrStatus = 0x79  # CRC Error Status
		self.CRCDigest = 0x7A  # CRC Digest
		self.CfgRegAccEn = 0x7F  # Configure Register Access Enable

		#* LOW POWER MODE REGISTERS - NOT USED *#
		self.DetectCtrl = 0x10
		self.DetectTh1 = 0x11
		self.DetectTh2 = 0x12
		self.DetectTh3 = 0x13
		self.PMOffsetA = 0x14
		self.PMOffsetB = 0x15
		self.PMOffsetC = 0x16
		self.PMPGA = 0x17
		self.PMIrmsA = 0x18
		self.PMIrmsB = 0x19
		self.PMIrmsC = 0x1A
		self.PMConfig = 0x10B
		self.PMAvgSamples = 0x1C
		self.PMIrmsLSB = 0x1D

		#* CONFIGURATION REGISTERS *#
		self.PLconstH = 0x31   # High Word of PL_Constant
		self.PLconstL = 0x32   # Low Word of PL_Constant
		self.MMode0 = 0x33   # Metering Mode Config
		self.MMode1 = 0x34   # PGA Gain Configuration for Current Channels
		self.PStartTh = 0x35   # Startup Power Th (P)
		self.QStartTh = 0x36   # Startup Power Th (Q)
		self.SStartTh = 0x37  # Startup Power Th (S)
		self.PPhaseTh = 0x38   # Startup Power Accum Th (P)
		self.QPhaseTh = 0x39  # Startup Power Accum Th (Q)
		self.SPhaseTh = 0x3A  # Startup Power Accum Th (S)

		#* CALIBRATION REGISTERS *#
		self.PoffsetA = 0x41   # A Line Power Offset (P)
		self.QoffsetA = 0x42   # A Line Power Offset (Q)
		self.PoffsetB = 0x43   # B Line Power Offset (P)
		self.QoffsetB = 0x44   # B Line Power Offset (Q)
		self.PoffsetC = 0x45   # C Line Power Offset (P)
		self.QoffsetC = 0x46   # C Line Power Offset (Q)
		self.PQGainA = 0x47   # A Line Calibration Gain
		self.PhiA = 0x48     # A Line Calibration Angle
		self.PQGainB = 0x49   # B Line Calibration Gain
		self.PhiB = 0x4A     # B Line Calibration Angle
		self.PQGainC = 0x4B   # C Line Calibration Gain
		self.PhiC = 0x4C     # C Line Calibration Angle

		#* FUNDAMENTAL#HARMONIC ENERGY CALIBRATION REGISTERS *#
		self.POffsetAF = 0x51  # A Fund Power Offset (P)
		self.POffsetBF = 0x52  # B Fund Power Offset (P)
		self.POffsetCF = 0x53  # C Fund Power Offset (P)
		self.PGainAF = 0x54  # A Fund Power Gain (P)
		self.PGainBF = 0x55  # B Fund Power Gain (P)
		self.PGainCF = 0x56  # C Fund Power Gain (P)

		#* MEASUREMENT CALIBRATION REGISTERS *#
		self.UgainA = 0x61   # A Voltage RMS Gain
		self.IgainA = 0x62   # A Current RMS Gain
		self.UoffsetA = 0x63   # A Voltage Offset
		self.IoffsetA = 0x64   # A Current Offset
		self.UgainB = 0x65   # B Voltage RMS Gain
		self.IgainB = 0x66   # B Current RMS Gain
		self.UoffsetB = 0x67   # B Voltage Offset
		self.IoffsetB = 0x68   # B Current Offset
		self.UgainC = 0x69   # C Voltage RMS Gain
		self.IgainC = 0x6A   # C Current RMS Gain
		self.UoffsetC = 0x6B   # C Voltage Offset
		self.IoffsetC = 0x6C   # C Current Offset
		self.IoffsetN = 0x6E   # N Current Offset

		#* ENERGY REGISTERS *#
		self.APenergyT = 0x80   # Total Forward Active
		self.APenergyA = 0x81   # A Forward Active
		self.APenergyB = 0x82   # B Forward Active
		self.APenergyC = 0x83   # C Forward Active
		self.ANenergyT = 0x84   # Total Reverse Active
		self.ANenergyA = 0x85   # A Reverse Active
		self.ANenergyB = 0x86   # B Reverse Active
		self.ANenergyC = 0x87   # C Reverse Active
		self.RPenergyT = 0x88   # Total Forward Reactive
		self.RPenergyA = 0x89   # A Forward Reactive
		self.RPenergyB = 0x8A   # B Forward Reactive
		self.RPenergyC = 0x8B   # C Forward Reactive
		self.RNenergyT = 0x8C   # Total Reverse Reactive
		self.RNenergyA = 0x8D   # A Reverse Reactive
		self.RNenergyB = 0x8E   # B Reverse Reactive
		self.RNenergyC = 0x8F   # C Reverse Reactive

		self.SAenergyT = 0x90   # Total Apparent Energy
		self.SenergyA = 0x91    # A Apparent Energy
		self.SenergyB = 0x92   # B Apparent Energy
		self.SenergyC = 0x93   # C Apparent Energy


		#* FUNDAMENTAL # HARMONIC ENERGY REGISTERS *#
		self.APenergyTF = 0xA0  # Total Forward Fund. Energy
		self.APenergyAF = 0xA1  # A Forward Fund. Energy
		self.APenergyBF = 0xA2  # B Forward Fund. Energy
		self.APenergyCF = 0xA3  # C Forward Fund. Energy
		self.ANenergyTF = 0xA4   # Total Reverse Fund Energy
		self.ANenergyAF = 0xA5  # A Reverse Fund. Energy
		self.ANenergyBF = 0xA6  # B Reverse Fund. Energy
		self.ANenergyCF = 0xA7  # C Reverse Fund. Energy
		self.APenergyTH = 0xA8  # Total Forward Harm. Energy
		self.APenergyAH = 0xA9  # A Forward Harm. Energy
		self.APenergyBH = 0xAA  # B Forward Harm. Energy
		self.APenergyCH = 0xAB  # C Forward Harm. Energy
		self.ANenergyTH = 0xAC  # Total Reverse Harm. Energy
		self.ANenergyAH = 0xAD   # A Reverse Harm. Energy
		self.ANenergyBH = 0xAE   # B Reverse Harm. Energy
		self.ANenergyCH = 0xAF   # C Reverse Harm. Energy

		#* POWER & P.F. REGISTERS *#
		self.PmeanT = 0xB0   # Total Mean Power (P)
		self.PmeanA = 0xB1   # A Mean Power (P)
		self.PmeanB = 0xB2   # B Mean Power (P)
		self.PmeanC = 0xB3   # C Mean Power (P)
		self.QmeanT = 0xB4   # Total Mean Power (Q)
		self.QmeanA = 0xB5   # A Mean Power (Q)
		self.QmeanB = 0xB6   # B Mean Power (Q)
		self.QmeanC = 0xB7   # C Mean Power (Q)
		self.SAmeanT = 0xB8   # Total Mean Power (S)
		self.SmeanA = 0xB9   # A Mean Power (S)
		self.SmeanB = 0xBA   # B Mean Power (S)
		self.SmeanC = 0xBB   # C Mean Power (S)
		self.PFmeanT = 0xBC   # Mean Power Factor
		self.PFmeanA = 0xBD   # A Power Factor
		self.PFmeanB = 0xBE   # B Power Factor
		self.PFmeanC = 0xBF   # C Power Factor

		self.PmeanTLSB = 0xC0   # Lower Word (Tot. Act. Power)
		self.PmeanALSB = 0xC1   # Lower Word (A Act. Power)
		self.PmeanBLSB = 0xC2   # Lower Word (B Act. Power)
		self.PmeanCLSB = 0xC3   # Lower Word (C Act. Power)
		self.QmeanTLSB = 0xC4   # Lower Word (Tot. React. Power)
		self.QmeanALSB = 0xC5   # Lower Word (A React. Power)
		self.QmeanBLSB = 0xC6   # Lower Word (B React. Power)
		self.QmeanCLSB = 0xC7   # Lower Word (C React. Power)
		self.SAmeanTLSB = 0xC8  # Lower Word (Tot. App. Power)
		self.SmeanALSB = 0xC9   # Lower Word (A App. Power)
		self.SmeanBLSB = 0xCA   # Lower Word (B App. Power)
		self.SmeanCLSB = 0xCB   # Lower Word (C App. Power)

		#* FUND#HARM POWER & V#I RMS REGISTERS *#
		self.PmeanTF = 0xD0   # Total Active Fund. Power
		self.PmeanAF = 0xD1   # A Active Fund. Power
		self.PmeanBF = 0xD2   # B Active Fund. Power
		self.PmeanCF = 0xD3   # C Active Fund. Power
		self.PmeanTH = 0xD4   # Total Active Harm. Power
		self.PmeanAH = 0xD5   # A Active Harm. Power
		self.PmeanBH = 0xD6   # B Active Harm. Power
		self.PmeanCH = 0xD7   # C Active Harm. Power
		self.UrmsA = 0xD9    # A RMS Voltage
		self.UrmsB = 0xDA    # B RMS Voltage
		self.UrmsC = 0xDB    # C RMS Voltage
		self.IrmsA = 0xDD    # A RMS Current
		self.IrmsB = 0xDE    # B RMS Current
		self.IrmsC = 0xDF    # C RMS Current
		self.IrmsN = 0xDC    # Calculated N RMS Current

		self.PmeanTFLSB = 0xE0  # Lower Word (Tot. Act. Fund. Power)
		self.PmeanAFLSB = 0xE1  # Lower Word (A Act. Fund. Power)
		self.PmeanBFLSB = 0xE2  # Lower Word (B Act. Fund. Power)
		self.PmeanCFLSB = 0xE3  # Lower Word (C Act. Fund. Power)
		self.PmeanTHLSB = 0xE4  # Lower Word (Tot. Act. Harm. Power)
		self.PmeanAHLSB = 0xE5  # Lower Word (A Act. Harm. Power)
		self.PmeanBHLSB = 0xE6  # Lower Word (B Act. Harm. Power)
		self.PmeanCHLSB = 0xE7  # Lower Word (C Act. Harm. Power)
		# 0xE8	    ## Reserved Register
		self.UrmsALSB = 0xE9  # Lower Word (A RMS Voltage)
		self.UrmsBLSB = 0xEA  # Lower Word (B RMS Voltage)
		self.UrmsCLSB = 0xEB  # Lower Word (C RMS Voltage)
		# 0xEC	    ## Reserved Register
		self.IrmsALSB = 0xED  # Lower Word (A RMS Current)
		self.IrmsBLSB = 0xEE  # Lower Word (B RMS Current)
		self.IrmsCLSB = 0xEF  # Lower Word (C RMS Current)

		#* PEAK, FREQUENCY, ANGLE & TEMPTEMP REGISTERS*#
		self.UPeakA = 0xF1   # A Voltage Peak
		self.UPeakB = 0xF2   # B Voltage Peak
		self.UPeakC = 0xF3   # C Voltage Peak
		# 0xF4	    ## Reserved Register
		self.IPeakA = 0xF5   # A Current Peak
		self.IPeakB = 0xF6   # B Current Peak
		self.IPeakC = 0xF7   # C Current Peak
		self.Freq = 0xF8    # Frequency
		self.PAngleA = 0xF9   # A Mean Phase Angle
		self.PAngleB = 0xFA   # B Mean Phase Angle
		self.PAngleC = 0xFB   # C Mean Phase Angle
		self.Temp = 0xFC   # Measured Temperature
		self.UangleA = 0xFD  # A Voltage Phase Angle
		self.UangleB = 0xFE  # B Voltage Phase Angle
		self.UangleC = 0xFF  # C Voltage Phase Angle