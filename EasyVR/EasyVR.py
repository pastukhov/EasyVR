#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
#import sys
import time

#from serial.serialutil import SerialException

 


class EasyVR:

# some constants

# Commands
	CMD_BREAK = 'b'  # abort recog or ping
	CMD_SLEEP = 's'  # go to power down
	CMD_KNOB = 'k'  # set si knob <1>
	CMD_LEVEL = 'v'  # set sd level <1>
	CMD_LANGUAGE = 'l'  # set si language <1>
	CMD_TIMEOUT = 'o'  # set timeout <1>
	CMD_RECOG_SI = 'i'  # do si recog from ws <1>
	CMD_TRAIN_SD = 't'  # train sd command at WordSet <1> pos <2>
	CMD_WordSet_SD = 'g'  # insert new command at WordSet <1> pos <2>
	CMD_UNWordSet_SD = 'u'  # remove command at WordSet <1> pos <2>
	CMD_RECOG_SD = 'd'  # do sd recog at WordSet <1> (0 = trigger mixed si/sd)
	CMD_ERASE_SD = 'e'  # reset command at WordSet <1> pos <2>
	CMD_NAME_SD = 'n'  # label command at WordSet <1> pos <2> with length <3> name <4-n>
	CMD_COUNT_SD = 'c'  # get command count for WordSet <1>
	CMD_DUMP_SD = 'p'  # read command data at WordSet <1> pos <2>
	CMD_MASK_SD = 'm'  # get active WordSet mask
	CMD_RESETALL = 'r'  # reset all commands and WordSets
	CMD_ID = 'x'  # get version id
	CMD_DELAY = 'y'  # set transmit delay <1> (log scale)
	CMD_BAUDRATE = 'a'  # set baudrate <1> (bit time, 1=>115200)
	CMD_QUERY_IO = 'q'  # configure, read or write I/O pin <1> of type <2>
	CMD_PLAY_SX = 'w'  # wave table entry <1><2> (10-bit) playback at volume <3>
	CMD_DUMP_SX = 'h'  # dump wave table entries
# Statuses, can be returned
	STS_MASK = 'k'  # mask of active WordSets <1-8>
	STS_COUNT = 'c'  # count of commands <1>
	STS_AWAKEN = 'w'  # back from power down mode
	STS_DATA = 'd'  # provide training <1>, conflict <2>, command label <3-35> (counted string)
	STS_ERROR = 'e'  # signal error code <1-2>
	STS_INVALID = 'v'  # invalid command or argument
	STS_TIMEOUT = 't'  # timeout expired
	STS_INTERR = 'i'  # back from aborted recognition (see 'break')
	STS_SUCCESS = 'o'  # no errors status
	STS_RESULT = 'r'  # recognised sd command <1> - training similar to sd <1>
	STS_SIMILAR = 's'  # recognised si <1> (in mixed si/sd) - training similar to si <1>
	STS_OUT_OF_MEM = 'm'  # no more available commands (see 'WordSet')
	STS_ID = 'x'  # provide version id <1>
	STS_PIN = 'p'  # return pin state <1>
	STS_TABLE_SX = 'h'  # provide table entries count <1-2> (10-bit), table name <3-35> (counted string)

# protocol arguments are in the range 0x40 (-1) to 0x60 (+31) inclusive
	ARG_MIN = 0x40
	ARG_MAX = 0x60
	ARG_ZERO = 0x41
	ARG_ACK = 0x20  # to read more status arguments

# Timeouts


	EASYVR_RX_TIMEOUT = 100  #  default receive timeout (in ms)
	EASYVR_WAKE_TIMEOUT = 200  # wakeup max delay (in ms)
	EASYVR_PLAY_TIMEOUT = 5000  # playback max duration (in ms)
	EASYVR_TOKEN_TIMEOUT = 1500  # token max duration (in ms)



	WAKE_TIMEOUT = EASYVR_WAKE_TIMEOUT
	DEF_TIMEOUT = EASYVR_WAKE_TIMEOUT


	ModuleId = { 
		'VRBOT'  : 0,  # Identifies a VRbot module
		'EASYVR' : 1,  # Identifies an EasyVR module
		'EASYVR2': 2  # Identifies an EasyVR module version 2
		  }

	Language = {
		'ENGLISH' :0,  # Uses the US English word sets
		'ITALIAN' :1,  # Uses the Italian word sets
		'JAPANESE':2,  # Uses the Japanese word sets
		'GERMAN'  :3,  # Uses the German word sets
		'SPANISH' :4,  # Uses the Spanish word sets
		'FRENCH'  :5  # Uses the French word sets
		}

	Group = {
		'TRIGGER' : 0,  # The trigger group (shared with built-in trigger word)
		'PASSWORD' : 16  # The password group (uses speaker verification technology)
		}


	Knob = {
		'LOOSER'  :0,  # Lowest threshold, most results reported 
		'LOOSE'   :1,  # Lower threshold, more results reported 
		'TYPICAL' :2,  # Typical threshold (deafult) 
		'STRICT'  :3,  # Higher threshold, fewer results reported 
		'STRICTER':4  # Highest threshold, fewest results reported 
		}



	Wordset = {
		'TRIGGER_SET'  :0,  # The built-in trigger word set
		'ACTION_SET'   :1,  # The built-in action word set
		'DIRECTION_SET':2,  # The built-in direction word set
		'NUMBER_SET'   :3  # The built-in number word set
		}

	Level = {
		'EASY'   : 1,  # Lowest value, most results reported 
		'NORMAL' : 2 ,  # Typical value (default) 
		'HARD'   : 3,  # Slightly higher value, fewer results reported 
		'HARDER' : 4,  # Higher value, fewer results reported 
		'HARDEST': 5  # Highest value, fewest results reported 
		}


#  Constants to use for baudrate settings

	Baudrate = {
		'B115200' : 1,  # 115200 bps
		'B57600'  : 2,  # 57600 bps
		'B38400'  : 3,  # 38400 bps
		'B19200'  : 6,  # 19200 bps
		'B9600'   : 12  # 9600 bps (default)
		  }
# * Constants for choosing wake-up method in sleep mode 
	WakeMode = {
		'WAKE_ON_CHAR'      : 0,  # Wake up on any character received
		'WAKE_ON_WHISTLE'   : 1,  # Wake up on whistle or any character received
		'WAKE_ON_LOUDSOUND' : 2,  # Wake up on a loud sound or any character received
		'WAKE_ON_2CLAPS'    : 3,  # Wake up on double hands-clap or any character received
		'WAKE_ON_3CLAPS'    : 6  # Wake up on triple hands-clap or any character received
		    }


#  #* Hands-clap sensitivity for wakeup from sleep mode.
#  Use in combination with #WAKE_ON_2CLAPS or #WAKE_ON_3CLAPS 


	ClapSense = {
	      'CLAP_SENSE_LOW'  : 0,  # # Lowest threshold 
	      'CLAP_SENSE_MID'  : 1,  # # Typical threshold 
	      'CLAP_SENSE_HIGH' : 2  # # Highest threshold 
		    }


# * Pin configuration options for the extra I/O connector 


	PinConfig = {
	      'OUTPUT_LOW'  :0,  # # Pin is a low output (0V) 
	      'OUTPUT_HIGH' :1,  # # Pin is a high output (3V) 
	      'INPUT_HIZ'   :2,  # # Pin is an high impedance input 
	      'INPUT_STRONG':3,  # # Pin is an input with strong pull-up (~10K) 
	      'INPUT_WEAK'  :4  # # Pin is an input with weak pull-up (~200K) 
		    }

# * Available pin numbers on the extra I/O connector 

	PinNumber = {
	      "IO1" : 1,  # # Pin IO1 
	      "IO2" : 2,  # # Pin IO2 
	      "IO3" : 3  # # Pin IO3 
		    }


#  Some quick volume settings for the sound playback functions
#  (any value in the range 0-31 can be used) 

	SoundVolume = {
	      'VOL_MIN'    : 0,  # # Lowest volume (almost mute) 
	      'VOL_HALF'   : 7,  # # Half scale volume (softer) 
	      'VOL_FULL'   : 15,  # # Full scale volume (normal) 
	      'VOL_DOUBLE' : 31  # # Double gain volume (louder) 
		      }


# * Special sound index values, always available even when no soundtable is present 

	SoundIndex = {
	      'BEEP' : 0  # # Beep sound 
		      }


# * Flags used by custom grammars 

	GrammarFlag = {
	      'GF_TRIGGER' : 0x10  # # A bit mask that indicate grammar is a trigger (opposed to commands) 
			}


# * Noise rejection level for SonicNet token detection (higher value, fewer results) 

	RejectionLevel = {
	      'REJECTION_MIN':0,  # # Lowest noise rejection, highest sensitivity 
	      'REJECTION_AVG':1,  # # Medium noise rejection, medium sensitivity 
	      'REJECTION_MAX':2  # # Highest noise rejection, lowest sensitivity 
			}

# * Error codes used by various functions 

	ErrorCode = {
    # -- 0x: Data collection errors (patgen, wordspot, t2si)
	    'ERR_DATACOL_TOO_LONG'        : 0x02,  # too long (memory overflow) 
	    'ERR_DATACOL_TOO_NOISY'       : 0x03,  # too noisy 
	    'ERR_DATACOL_TOO_SOFT'        : 0x04,  # spoke too soft 
	    'ERR_DATACOL_TOO_LOUD'        : 0x05,  # spoke too loud 
	    'ERR_DATACOL_TOO_SOON'        : 0x06,  # spoke too soon 
	    'ERR_DATACOL_TOO_CHOPPY'      : 0x07,  # too many segments/too complex 
	    'ERR_DATACOL_BAD_WEIGHTS'     : 0x08,  # invalid SI weights 
	    'ERR_DATACOL_BAD_SETUP'       : 0x09,  # invalid setup 

    # -- 1x: Recognition errors (si, sd, sv, train, t2si)
	    'ERR_RECOG_FAIL'              : 0x11,  # recognition failed 
	    'ERR_RECOG_LOW_CONF'          : 0x12,  # recognition result doubtful 
	    'ERR_RECOG_MID_CONF'          : 0x13,  # recognition result maybe 
	    'ERR_RECOG_BAD_TEMPLATE'      : 0x14,  # invalid SD/SV template 
	    'ERR_RECOG_BAD_WEIGHTS'       : 0x15,  # invalid SI weights 
	    'ERR_RECOG_DURATION'          : 0x17,  # incompatible pattern durations 

    # -- 2x: T2si errors (t2si)
	    'ERR_T2SI_EXCESS_STATES'      : 0x21,  # state structure is too big 
	    'ERR_T2SI_BAD_VERSION'        : 0x22,  # RSC code version/Grammar ROM dont match 
	    'ERR_T2SI_OUT_OF_RAM'         : 0x23,  # reached limit of available RAM 
	    'ERR_T2SI_UNEXPECTED'         : 0x24,  # an unexpected error occurred 
	    'ERR_T2SI_OVERFLOW'           : 0x25,  # ran out of time to process 
	    'ERR_T2SI_PARAMETER'          : 0x26,  # bad macro or grammar parameter 

	    'ERR_T2SI_NN_TOO_BIG'         : 0x29,  # layer size out of limits 
	    'ERR_T2SI_NN_BAD_VERSION'     : 0x2A,  # net structure incompatibility 
	    'ERR_T2SI_NN_NOT_READY'       : 0x2B,  # initialization not complete 
	    'ERR_T2SI_NN_BAD_LAYERS'      : 0x2C,  # not correct number of layers 

	    'ERR_T2SI_TRIG_OOV'           : 0x2D,  # trigger recognized Out Of Vocabulary 
	    'ERR_T2SI_TOO_SHORT'          : 0x2F,  # utterance was too short 

    # -- 4x: Synthesis errors (talk, sxtalk)
	    'ERR_SYNTH_BAD_VERSION'       : 0x4A,  # bad release number in speech file 
	    'ERR_SYNTH_ID_NOT_SET'        : 0x4B,  # (obsolete) bad sentence structure 
	    'ERR_SYNTH_TOO_MANY_TABLES'   : 0x4C,  # (obsolete) too many talk tables 
	    'ERR_SYNTH_BAD_SEN'           : 0x4D,  # (obsolete) bad sentence number 
	    'ERR_SYNTH_BAD_MSG'           : 0x4E,  # bad message data or SX technology files missing 

    # -- 8x: Custom errors
	    'ERR_CUSTOM_NOTA'             : 0x80,  # none of the above (out of grammar) 

    # -- Cx: Internal errors (all)
	    'ERR_SW_STACK_OVERFLOW'       : 0xC0,  # no room left in software stack 
	    'ERR_INTERNAL_T2SI_BAD_SETUP' : 0xCC  # T2SI test mode error 
			}

# Init private vars
	_value = 0
	_status_v = 0                                                                                                                                                                                                                               
	_status_b_command = True                                                                                                                                                                                                                  
	_status_b_builtin = True                                                                                                                                                                                                               
	_status_b_error = True                                                                                                                                                                                                                   
	_status_b_timeout = True                                                                                                                                                                                                                  
	_status_b_invalid = True                                                                                                                                                                                                                
	_status_b_memfull = True                                                                                                                                                                                                                  
	_status_b_conflict = True                                                                                                                                                                                                               
	_status_b_token = True                                                                                                                                                                                                                  



# Pyserial instance
	ser = serial.Serial()
	ser.timeout = 5
	ser.baudrate = 9600
	ser.parity = serial.PARITY_NONE
	ser.stopbits = serial.STOPBITS_ONE
	ser.bytesize = serial.EIGHTBITS


# Open port
	def __init__(self, port):
		try:
			self.ser.port = port
			self.ser.open()
			print "Successfully connected to port %r." % self.ser.port
		except serial.SerialException, e:
			print "could not open serial port '{}': {}".format(self.ser.port, e)
#			print "Error %s connecting to port %r." % self.ser.port 
# 		if self.detect():
# 			return True
# 		else:
# 			return False


	def __del__(self):
		if self.ser.isOpen():
			self.ser.close()
			return True


	def detect(self):
		for i in range(0, 5):
			self.sendCmd(self.CMD_BREAK)
			if self.recv(self.WAKE_TIMEOUT) == self.STS_SUCCESS:
				return True
			return False

	def milisleep(self, ms):
			time.sleep(ms / 1000)

	def send(self, c):
			self.ser.write(c)
			self.milisleep(1)

	def sendArg(self, c):
			self.ser.flush()
			self.ser.write(chr(c + self.ARG_ZERO))

	def sendGroup(self, c):
			self.milisleep(1)
			self.ser.write(c + self.ARG_ZERO)
			self.milisleep(19)

	def recv(self, timeout):
			while (timeout > 0) and self.ser.inWaiting() == 0:
				self.milisleep(1)
				timeout = timeout - 1
			return self.ser.read()

	def recvArg(self, timeout):
			self.send(chr(self.ARG_ACK))
			return self.recv(timeout)

	def stop(self):
		self.sendCmd(self.CMD_BREAK)
		rx = self.recv(self.WAKE_TIMEOUT)
		if rx == self.STS_INTERR or rx == self.STS_SUCCESS:
			return True
		else:
			return False

	def sleep(self, mode):
		self.sendCmd(self.CMD_SLEEP)
		self.sendArg(mode)
		if (self.recv(self.DEF_TIMEOUT) == self.STS_SUCCESS):
			return True
		else:
			return False

	def getID(self):
		self.sendCmd(self.CMD_ID)
		if self.recv(self.DEF_TIMEOUT) == self.STS_ID:
			return self.recvArg(self.DEF_TIMEOUT)
		else:
			return -1

	def setLanguage(self, lang):
		self.sendCmd(self.CMD_LANGUAGE)
		self.sendArg(lang)
		if (self.recv(self.DEF_TIMEOUT) == self.STS_SUCCESS):
			return True
		else:
			return False

	def setTimeout(self, seconds):
		self.sendCmd(self.CMD_TIMEOUT)
		self.sendArg(seconds)
		if (self.recv(self.DEF_TIMEOUT) == self.STS_SUCCESS):
			return True
		else:
			return False

	def setKnob(self, knob):
		self.sendCmd(self.CMD_KNOB)
		self.sendArg(knob)
		if (self.recv(self.DEF_TIMEOUT) == self.STS_SUCCESS):
			return True
		else:
			return False

	def setLevel(self, level):
		self.sendCmd(self.CMD_LEVEL)
		self.sendArg(level)
		if (self.recv(self.DEF_TIMEOUT) == self.STS_SUCCESS):
			return True
		else:
			return False

	def setDelay(self, millis):
		self.sendCmd(self.CMD_DELAY)
		if millis <= 10:
			self.sendArg(millis)
		elif millis <= 100:
			self.sendArg(millis / 10 + 9)
		elif (millis <= 1000):
			self.sendArg(millis / 100 + 18)
		else:
			return False;
		if self.recv(self.DEF_TIMEOUT) == self.STS_SUCCESS:
			return True
		else:
			return False

	def changeBaudrate(self, baud):
		self.sendCmd(self.CMD_BAUDRATE)
		self.sendArg(baud)
		if self.recv(self.DEF_TIMEOUT) == self.STS_SUCCESS:
			return True
		else:
			return False

	def addCommand(self, group, index):
		self.sendCmd(self.CMD_GROUP_SD)
		self.sendGroup(group)
		self.sendArg(index)
		rx = self.recv(self.DEF_TIMEOUT)
		if rx == self.STS_SUCCESS:
			self._status.v = 0
			return True
		if rx == self.STS_OUT_OF_MEM:
			self._status.b._memfull = True
		else:
			return False

	def removeCommand(self, group, index):
		self.sendCmd(self.CMD_UNGROUP_SD)
		self.sendGroup(group)
		self.sendArg(index)
		if self.recv(self.DEF_TIMEOUT) == self.STS_SUCCESS:
			return True
		else:
			return False
		
	def setCommandLabel(self, group, index, name):
		pass
# 		sendCmd(self.CMD_NAME_SD)
# 		sendGroup(group)
# 		sendArg(index)
# 		len = 31
# 		p = name
# 		for p  p != 0 && len > 0; ++p, --len):
# 		  if (isdigit(p)):
# 		    --len
# 		len = 31 - len
 # 
#    		sendArg(len)
#    		for (i = 0; i < len; ++i):
# 			c = name[i]
# 			if (isdigit(c)):
# 				send('^')
# 				sendArg(c - '0')
# 			elif (isalpha(c)):
# 				send(c & ~0x20); # to uppercase
# 			else:
# 		    send('_')
# 		if (self.recv(self.DEF_TIMEOUT) == self.STS_SUCCESS):
# 		  return True
# 		else:
# 		  return False

	def eraseCommand(self, group):
		pass
#		self.sendCmd(self.CMD_ERASE_SD)
#		self.sendGroup(group)
#		self.sendArg(index)
#		if self.recv(self.DEF_TIMEOUT) == self.STS_SUCCESS:
#			return True
#		else:
#			return False

	def getGroupMask(self, mask):
		pass
# 		sendCmd(self.CMD_MASK_SD)
# 		if (self.recv(self.DEF_TIMEOUT) == self.STS_MASK):
# 			for (i = 0; i < 4; ++i):
# 				if (!recvArg(rx, self.DEF_TIMEOUT)):
# 	    				    return False
# 	    ((uint8_t*)&mask)[i] |= rx & 0x0F
# 	    if (!recvArg(rx, self.DEF_TIMEOUT)):
# 	      return False
# 	    ((uint8_t*)&mask)[i] |= (rx << 4) & 0xF0
# 	   return True
# 	 return False

	def recognizeCommand(self, group):
		self.sendCmd(self.CMD_RECOG_SD)
		self.sendArg(group)

	def resetAll(self):
		self.sendCmd(self.CMD_RESETALL)
		self.sendArg(17)
		if self.recv(RESET_TIMEOUT) == self.STS_SUCCESS:
			return True
		else:
			return False


	def sendCmd(self, c):
		self.ser.flush()
		self.send(c)

	def getWord(self):
		return self._status_b_builtin 

	def getCommand(self):
		if self.recv(5) == self.STS_RESULT:
			return ord(self.recvArg(self.DEF_TIMEOUT)) - self.ARG_ZERO
		else:
			return False
     


'''

def hasFinished():
{
  rx = self.recv(NO_TIMEOUT);
  if (rx < 0):
    return False
  
  self._status.v = 0
  
  if rx == STS_SUCCESS:
    return True
  
  elif rx == STS_SIMILAR:
    self._status.b._builtin = True
      if _value = self.recvArg(DEF_TIMEOUT):
      return True
    }
    break;



  elif rx == STS_RESULT:
    self._status.b._command = True
    
  elif rx == STS_TOKEN:
    self._status.b._token = True
  
    if (self.recvArg(rx, DEF_TIMEOUT))
    {
      _value = rx << 5;
      if (self.recvArg(rx, DEF_TIMEOUT))
      {
        _value |= rx;
        return true;
      }
    }
    break;
    
  elif rx == STS_TIMEOUT:
    self._status.b._timeout = True
    return True
    
  elif rx == STS_INVALID:
    self._status.b._invalid = True;
    return True
    
  elif rx == STS_ERROR:
    _status.b._error = true;
    if (self.recvArg(rx, DEF_TIMEOUT))
    {
      _value = rx << 4;
      if (self.recvArg(rx, DEF_TIMEOUT))
      {
        _value |= rx;
        return true;
      }
    }
    break;
  }

  # unexpected condition (communication error)
  self._status.v = 0
  self._status.b._error = True
  return True
}

'''




