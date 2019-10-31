#import itertools
from collections import OrderedDict
#from systemLib import *

import serial
import time

import sys
sys.stdout.flush()
PORT = sys.argv[1]

print PORT

def serial_write(port, send=""):
    print ("serial_write : " + send)

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
    flag = 0
    data = []
    print ("[log] receive : "+receive)

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
#        print ("in?")
        sys.stdout.flush()
        time.sleep(0.01)
        if flag == 1:
            flag = 2
            print ("[log]flag : ")
            print (flag)
        while True:
#            print port
            lines = port.readlines()
            for i in lines:
                print ("out : " + i)
                
#            print lines
            if lines != None:
#                print "out1"
                break
            end_time = time.time()
            if (end_time - start_time >= limit_time):
                print ("[serial_read_error]Time over %s" %(limit_time))
                break
#        print "for"
        for line in lines:
            print ("test")
            print ("line "+line)

            # try:
            #     line = line.decode('ISO-8859-1')
            # except UnicodeDecodeError as e:
            #     print (e)
            #     print (type(line))
                       
           # ret = line.find(receive)
           # print "ret : %d"%(ret)

            # data.append(line)

#        print data


#         for line in lines:
#             print ("[log] in line")
#             print (line)
#             try:
#                 line = line.decode('ISO-8859-1')
#             except UnicodeDecodeError as e:
#                 print (e)
#                 print (type(line)
#             date = datetime.now()
#             #print ("[%s]    %s" %(date.strftime('%H:%M:%S:%s'), line))
#             data.append(line)
            
#             ret = line.find(receive)
#             print ("result : ")
#             print ret
            
#             if line.find(receive) != -1:
#                 flag = flag + 1
# #            elif line.find("U-BOOT >") != -1:
# #                serial_write(port, "reset")
#         end_time = time.time()

        # if flag >= 2:
        #     return True, data
        # elif (end_time - start_time >= limit_time):
        #     print ("")
        #     print ("[serial_read]Time over %s" %(limit_time))
        #     print ("")
        #     return False, data

def serial_way(usb_port, send, receive, limit_time):
    port = serial.Serial(usb_port, baudrate=115200, timeout=0.1)
    try:
        serial_write(port, send)
    except:
        time.sleep(5)
        serial_write(port, send)

    result, data = serial_read(port, receive, limit_time)
    return result, data

def execute_cmd(cmd, receive, port,limit_time):
    result, data = serial_way(port, cmd, receive, limit_time)
    return result, data

def cmd_cd():
    execute_cmd("cd /", "", PORT, 5)
    result, data = execute_cmd("cd mnt", "", PORT, 5)
    if result == False:
        print ("cd Fail")
    else:
        print ("cd Pass")
    
def cmd_echo():
    result, data = execute_cmd("echo test > text", "", PORT, 5)
    if result == False:
        print ("echo Fail")
    else:
        print ("echo Pass")

def cmd_cat():
    result, data = execute_cmd("cat text", "", PORT, 5)
    if result == False:
        print ("cat Fail")
    else:
        print ("cat Pass")

def cmd_rm():
    result, data = execute_cmd("rm text", "", PORT, 5)
    if result == False:
        print ("rm Fail")
    else:
        print ("rm Pass")
    
def cmd_pwd():
#    execute_cmd("cd /", "", PORT, 5)
#    execute_cmd("cd mnt", "", PORT, 5)
    result, data = execute_cmd("pwd", "/mnt", PORT, 5)
    print result, data
    if result == False:
        print ("pwd Fail")
    else:
        print ("pwd Pass")


    
CMD_LIST = OrderedDict()
#CMD_LIST['cd'] = cmd_cd
#CMD_LIST['echo'] = cmd_echo
#CMD_LIST['cat'] = cmd_cat
#CMD_LIST['rm'] = cmd_rm
CMD_LIST['pwd'] = cmd_pwd
# CMD_LIST['date'] = cmd_date
# CMD_LIST['df'] = cmd_df
# CMD_LIST['free'] = cmd_free
# CMD_LIST['setenv'] = cmd_setenv
# CMD_LIST['getenv'] = cmd_getenv
# CMD_LIST['unsetenv'] = cmd_unsetenv
# CMD_LIST['ls'] = cmd_ls
# CMD_LIST['mkdir'] = cmd_mkdir
# CMD_LIST['rmdir'] = cmd_rmdir
# CMD_LIST['ps'] = cmd_ps
# CMD_LIST['pwd'] = cmd_pwd
# CMD_LIST['sleep'] = cmd_sleep
# CMD_LIST['uptime'] = cmd_uptime


# {
#     'cat' : cmd_cat,
#     'cd' : cmd_cd,
#     'date' : cmd_date,
#     'df' : cmd_df,
#     'echo' : cmd_echo,
#     'free' : cmd_free,
#     'setenv' : cmd_setenv,
#     'getenv' : cmd_getenv,
#     'unsetenv' : cmd_unsetenv,
#     'ls' : cmd_ls,
#     'mkdir' : cmd_mkdir,
#     'rmdir' : cmd_rmdir,
#     'ps' : cmd_ps,
#     'pwd' : cmd_pwd,
    
# }


if (__name__ == '__main__'):
    for key, tc in CMD_LIST.items():
        CMD_LIST[key]()


        
#            check_tc_result()
#            test_teardown()
