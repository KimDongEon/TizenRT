#import itertools
from collections import OrderedDict
#from systemLib import *

import serial
import time

import sys
sys.stdout.flush()
PORT = sys.argv[1]
PASS_COUNT = 0

def serial_write(port, send=""):
    print ('['+sys._getframe(3).f_code.co_name+']'+"TASH>>"+send)

    if port.isOpen() == False:
        try:
            port.open()
            print ("Port connect = ", port.isOpen())
        except FileNotFoundError:
            print ("FILE Not Found Error")
            time.sleep(2)
            port.open()
        except serial.serialutil.SerialException:
            print ("serial.serialutil.SerialException")
            time.sleep(2)
            port.open()
    
    if send.find("\n") != -1:
        port.write((send).encode())
    else:
        port.write((send+"\n").encode())
    time.sleep(0.1)

def serial_read(port, receive="", limit_time=1):
    sys.stdout.flush()
    if port.isOpen() == False:
        try:
            port.open()
            print ("Port connect = ", port.isOpen())
        except FileNotFoundError:
            print ("FILE Not Found Error")
            time.sleep(2)
            port.open()
        except serial.serialutil.SerialException:
            print ("serial.serialutil.SerialException")
            time.sleep(2)
            port.open()

        print ("Port connect = ", port.isOpen())

    start_time = time.time()
    while(True):
        sys.stdout.flush()
        time.sleep(0.01)

        while(True):
            lines = port.readlines()
            print lines
            if lines != None:
                break
            end_time = time.time()
            if (end_time - start_time >= limit_time):
                print ("[serial_read_error]Time over %s" %(limit_time))
                break

        for line in lines:
            ret = line.find(receive)
            if ret != -1:
                print ('['+sys._getframe(3).f_code.co_name+']'+"TASH>>"+receive)
                return True

        return False


def serial_way(usb_port, send, receive, limit_time):
    port = serial.Serial(usb_port, baudrate=115200, timeout=0.1)
    try:
        serial_write(port, send)
    except:
        time.sleep(5)
        serial_write(port, send)

    result = serial_read(port, receive, limit_time)
    return result

def execute_cmd(cmd, receive, port,limit_time):
    result = serial_way(port, cmd, receive, limit_time)
    return result
    
def cmd_pwd():
    execute_cmd("cd /", "", PORT, 5)
    execute_cmd("cd mnt", "", PORT, 5)
    result = execute_cmd("pwd", "/mnt", PORT, 5)
    
    if result == False:
        print (sys._getframe(0).f_code.co_name + " : Fail")
    else:
        print (sys._getframe(0).f_code.co_name + " : Pass")

        
CMD_LIST = OrderedDict()
#CMD_LIST['cd'] = cmd_cd
#CMD_LIST['echo'] = cmd_echo
#CMD_LIST['cat'] = cmd_cat
#CMD_LIST['rm'] = cmd_rm
CMD_LIST['pwd'] = cmd_pwd
#CMD_LIST['date'] = cmd_date
#CMD_LIST['df'] = cmd_df
#CMD_LIST['free'] = cmd_free
#CMD_LIST['setenv'] = cmd_setenv
#CMD_LIST['getenv'] = cmd_getenv
#CMD_LIST['unsetenv'] = cmd_unsetenv
#CMD_LIST['ls'] = cmd_ls
#CMD_LIST['mkdir'] = cmd_mkdir
#CMD_LIST['rmdir'] = cmd_rmdir
#CMD_LIST['ps'] = cmd_ps
#CMD_LIST['pwd'] = cmd_pwd
#CMD_LIST['sleep'] = cmd_sleep
#CMD_LIST['uptime'] = cmd_uptime
#CMD_LIST['filesystem_tc'] = cmd_filesystem_tc

if (__name__ == '__main__'):
    for key, tc in CMD_LIST.items():
        CMD_LIST[key]()
