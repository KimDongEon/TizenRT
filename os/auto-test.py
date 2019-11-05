#import itertools
from collections import OrderedDict
#from systemLib import *

import serial
import time
import re

import sys
sys.stdout.flush()
PORT = sys.argv[1]
PASS_COUNT = 0
FAIL_COUNT = 0

def serial_write(port, send=""):
    print ('\n['+sys._getframe(3).f_code.co_name+']'+"TASH>>"+send)

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
            if lines != None:
                break
            end_time = time.time()
            if (end_time - start_time >= limit_time):
                print ("[serial_read_error]Time over %s" %(limit_time))
                break

        if not lines:
            continue

        lines.pop(0)
        for line in lines:
            print (line),
            ret1 = line.find("failed")
            ret2 = line.find("] FAIL")
            if (ret1 != -1) | (ret2 != -1):
                return False

        receive_cnt = len(receive)
        judge_cnt = 0
        for line in lines:
            for data in receive:
                ret = line.find(data)
                if ret != -1:
                    judge_cnt = judge_cnt + 1
                    break

        if (receive_cnt == judge_cnt):
            return True

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



###### CMD Function #####
def cmd_ls():
    data = []
    data.append("/:")
    data.append("TASH>>")
    execute_cmd("cd /", "", PORT, 5)
    result = execute_cmd("ls", data, PORT, 5)
    return result

def cmd_filesystem_tc():
    data = []
    data.append("End")
    result = execute_cmd("filesystem_tc", data, PORT, 5)
    return result

def cmd_taskmgr_utc():
    data = []
    data.append("End")
    result = execute_cmd("taskmgr_utc", data, PORT, 5)
    return result

###### CMD List #####
CMD_LIST = OrderedDict()
CMD_LIST['ls'] = cmd_ls
CMD_LIST['taskmgr_utc'] = cmd_taskmgr_utc
#CMD_LIST['filesystem_tc'] = cmd_filesystem_tc
#CMD_LIST['pwd'] = cmd_pwd
#CMD_LIST['cd'] = cmd_cd
#CMD_LIST['echo'] = cmd_echo
#CMD_LIST['cat'] = cmd_cat
#CMD_LIST['rm'] = cmd_rm

#CMD_LIST['date'] = cmd_date
#CMD_LIST['df'] = cmd_df
#CMD_LIST['free'] = cmd_free
#CMD_LIST['setenv'] = cmd_setenv
#CMD_LIST['getenv'] = cmd_getenv
#CMD_LIST['unsetenv'] = cmd_unsetenv
#CMD_LIST['mkdir'] = cmd_mkdir
#CMD_LIST['rmdir'] = cmd_rmdir
#CMD_LIST['ps'] = cmd_ps
#CMD_LIST['pwd'] = cmd_pwd
#CMD_LIST['sleep'] = cmd_sleep
#CMD_LIST['uptime'] = cmd_uptime


if (__name__ == '__main__'):
    for key, tc in CMD_LIST.items():
        result = CMD_LIST[key]()
        if result == False:
            print ('\n['+(CMD_LIST[key].__name__)+']' + " : FAIL")
            FAIL_COUNT = FAIL_COUNT + 1
        else:
            print ('\n['+(CMD_LIST[key].__name__)+']' + " : PASS")
            PASS_COUNT = PASS_COUNT + 1

    print ("\n\n########## Auto Test End [PASS : %d, FAIL : %d] ##########"%(PASS_COUNT,FAIL_COUNT))
