#!/usr/bin/python3
#from evdev import InputDevice, categorize, ecodes
import evdev


class BarcodeScan:
    '''
    Barcode scan library by minhcuongit97@gmail.com
    Create date: 18/02/2020
    Last modified date: 18/02/2020
    ** This library support scan Qrcode and barcode for some products that improve the production in the factories
    '''

    def __init__(self):
        self.list_devices = []
        self.current_device = None

    def __str__(self):
        return f"Current device: {self.current_device}"

    def get_list_devices(self):
        '''
        Get list of the devices visible
        '''
        print('Searching for devices...')
        list_deivce = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        print('----List devices-----------')
        for d in list_deivce:
            print(d.fn, d.name, d.phys)
        print('---------------------------')
        self.list_devices = list_deivce
        return list_deivce

    def connect_device(self, deviceId):
        '''
        Connect to a device with an id from get_list_devices method
        '''
        # sample:"/dev/input/event4"
        try:
            if deviceId:
                d = evdev.InputDevice(deviceId)
                print(f"Connected to '{str(d.name)}'")
                self.current_device = d
                return d
            else:
                return None
        except:
            print('An error occurred when connect to a device.')

    def disconnect_device(self):
        '''
        Disconnect to the device to release grab order to other application can use it
        '''
        if self.current_device != None:
            self.current_device.ungrab()
        else:
            print('No device found!')

    def read_data(self):
        '''
        Read data one by one when the device is establish
        This method return name, code and value which read from device
        '''
        if self.current_device:
            print('-----Begin to receive data-----')
            for event in self.current_device.read_loop():
                # print(type(event))
                print(self.current_device.name + " : " + str(event.code) +
                      ' => ' + str(event.value))
        else:
            print('The device is not valid. Please try again.')

    def read_data2(self):
        '''
        Read data one by one when the device is establish
        This method return an event (include key) which read from device
        '''
        if self.current_device:
            print('-----Begin to receive data-----')
            for event in self.current_device.read_loop():
                if event.type == evdev.ecodes.EV_KEY:
                    # print(event)
                    print(evdev.categorize(event))
        else:
            print('The device is not valid. Please try again.')

    def read_data3(self):
        '''
        Read data one by one when the device is establish
        This method return all of the event and categorize which read from device
        '''
        if self.current_device:
            print('-----Begin to receive data-----')
            for event in self.current_device.read_loop():
                if event.type == evdev.ecodes.EV_KEY:
                    # print(event)
                    print(
                        f"event: code:{event.code}, value:{event.value}, type:{event.type}")
                    print(
                        f"categorize: code:{evdev.categorize(event)}, value:{event.value}, type:{event.type}")
        else:
            print('The device is not valid. Please try again.')

    def get_data_realtime(self):
        if self.current_device:
            # Provided as an example taken from my own keyboard attached to a Centos 6 box:
            scancodes = {
                # Scancode: ASCIICode
                0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
                10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'q', 17: u'w', 18: u'e', 19: u'r',
                20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
                30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u';',
                40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n',
                50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT'
            }
            capscodes = {
                0: None, 1: u'ESC', 2: u'!', 3: u'@', 4: u'#', 5: u'$', 6: u'%', 7: u'^', 8: u'&', 9: u'*',
                10: u'(', 11: u')', 12: u'_', 13: u'+', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
                20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL',
                30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':',
                40: u'\'', 41: u'~', 42: u'LSHFT', 43: u'|', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
                50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'RSHFT', 56: u'LALT',  57: u' ', 100: u'RALT'
            }
            # setup vars
            x = ''
            caps = False
            # grab provides exclusive access to the device
            self.current_device.grab()
            # loop
            for event in self.current_device.read_loop():
                if event.type == evdev.ecodes.EV_KEY:
                    # Save the event temporarily to introspect it
                    data = evdev.categorize(event)
                    if data.scancode == 42:
                        if data.keystate == 1:
                            caps = True
                        if data.keystate == 0:
                            caps = False
                    if data.keystate == 1:  # Down events only
                        if caps:
                            key_lookup = u'{}'.format(capscodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(
                                data.scancode)  # Lookup or return UNKNOWN:XX
                        else:
                            key_lookup = u'{}'.format(scancodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(
                                data.scancode)  # Lookup or return UNKNOWN:XX
                        if (data.scancode != 42) and (data.scancode != 28):
                            x += key_lookup
                        if(data.scancode == 28):
                            print(f"Qrcode: {x}")          # Print it all out!
                            #Todo: This method is only using for debug by dev
                            if(x=='release'):
                                self.disconnect_device()
                                return
                            x = ''
        else:
            print('No device found!')


if __name__ == "__main__":
    print('The program is running...')
    barcode = BarcodeScan()
    # print(barcode)
    lsD = barcode.get_list_devices()
    demo_device = "/dev/input/event1"
    device = barcode.connect_device(demo_device)
    # read_data2(device)
    barcode.get_data_realtime()
    print('***Program is exited!!')
