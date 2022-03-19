import serial, time

port = serial.Serial('/dev/tty.usbserial-1410', 57600)
ans = '8' # если здесь стоит восьмёрка, то крутится в одну сторону, а если 9 то в другую
var = bytes(ans.encode('utf-8'))
if port.isOpen():
    print("YES")
    while 1:
        port.write(var)
        time.sleep(1)
else:
    print("NO")

#код ниже выводит все Serial ports
# import sys
# import glob
# import serial
#
#
# def serial_ports():
#     """ Lists serial port names
#
#         :raises EnvironmentError:
#             On unsupported or unknown platforms
#         :returns:
#             A list of the serial ports available on the system
#     """
#     if sys.platform.startswith('win'):
#         ports = ['COM%s' % (i + 1) for i in range(256)]
#     elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
#         # this excludes your current terminal "/dev/tty"
#         ports = glob.glob('/dev/tty[A-Za-z]*')
#     elif sys.platform.startswith('darwin'):
#         ports = glob.glob('/dev/tty.*')
#     else:
#         raise EnvironmentError('Unsupported platform')
#
#     result = []
#     for port in ports:
#         try:
#             s = serial.Serial(port)
#             s.close()
#             result.append(port)
#         except (OSError, serial.SerialException):
#             pass
#     return result
#
#
# if __name__ == '__main__':
#     print(serial_ports())