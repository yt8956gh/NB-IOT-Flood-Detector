import serial
import os
import json
import base64
import sys
import requests
import traceback
from time import sleep


class NBiot:
    
    def __init__(self):

        self.ser = serial.Serial("/dev/serial0", 9600, timeout=0.5)
        sleep(1)


    def nbiot_init(self):

        self.send_cmd("AT+CSQ")
        self.send_cmd("AT+CGATT?")
        self.send_cmd("AT+CGNAPN")
        # self.send_cmd("AT+CSTT=\"internet.iot\"")
        self.send_cmd("AT+CNMP?",3)
        self.send_cmd("AT+CMNB?",3)
        self.send_cmd("AT+NBSC?")
        self.send_cmd("AT+CPSI?")
        self.send_cmd("AT+HTTPTERM")
        self.send_cmd("AT+SAPBR=3,1,\"Contype\",\"GPRS\"")
        self.send_cmd("AT+SAPBR=3,1,\"APN\",\"internet.iot\"")
        self.send_cmd("AT+SAPBR=1,1")
        self.send_cmd("AT+HTTPINIT")


    def send_cmd(self, cmd, delay=1):

        if cmd[-2:]=="\r\n":
            print("have RN")
        else:
            cmd+="\r\n"

        self.ser.write(cmd.encode('ascii'))
        sleep(1)
        result = self.ser.readline()

        while len(result)!=0:

            result = result.decode('ascii')

            if result[0:3]=="AT+":
                print("[cmd] "+result, end="")
            elif result[0:2]!='\r\n':
                result = result.replace("<br/>","\n> ")
                result = result.replace("<br>","\n> ")
                print("> "+result, end="")

            result = self.ser.readline()

        print("")


    def send_cmd_action(self, cmd):
        
        if cmd[-2:]=="\r\n":
            print("Hint: There are \\r\\n in command.")
        else:
            cmd+="\r\n"

        self.ser.write(cmd.encode('ascii'))
        sleep(1)

        print("Waiting ",end="", flush=True)

        while True:

            try:
                result = self.ser.readline().decode('ascii')
            except:
                traceback.print_exc()
                print("The file trasferred is too large")
                break

            print(".", end="", flush=True)

            if result.find("+HTTPACTION:",0, len(result))!=-1:
                print("\n\n<-----Retrieved response from server----->\n")
                response = result[12:].split(",")

                print("Method: %s\nStatus: %s\nResLen: %s" % tuple(response))

                if response[1]=="200":
                    print("<-----Response Text----->\n")
                    self.send_cmd("AT+HTTPREAD")

                break
            elif result.find("ERROR", 0, len(result))!=-1:
                print("\n"+result)
                break
        print("")


    def send_file(self, filename='./test.jpg'):

        with open(filename, 'rb') as file:
            self.send_cmd("AT+HTTPPARA=\"CID\",1")
            self.send_cmd("AT+HTTPPARA=\"URL\", \"http://ccrcapi.isdc.org.tw/datapi_v1/camera_img\"")
            # self.send_cmd("AT+HTTPPARA=\"Content-Disposition\", \"form-data\"")

            data={}
        
            url = 'http://crcapi.isdc.org.tw/datapi_v1/camera_img'
            img = {'img':open(filename, 'rb')}
            form_data = {"access_token":"S0YUPrMAre60igE+iMvsWfdxs5MUwwUUMdjkveK/w73J/ANfPJZJYT3t8OP1tF3H ",
                    "pass_code":"Winnie the pooh",
                    "machine_id":0}

            req = requests.Request("POST", url, data=form_data, files=img)
            req.encoding = 'utf8'
            prepared = req.prepare()

            data = prepared.body

            self.send_cmd("AT+HTTPPARA=\"CONTENT\", \"%s\"" % prepared.headers['Content-Type'])

            print(type(data))
            # print("Post Response: %s" % str(r.content).replace("<br/>","\n"))


            size = int(prepared.headers['Content-Length'])
            syssize = sys.getsizeof(data)
            print("size with getsize: ", syssize)
            print("size with content-Length: ", size)

            if self.ser.isOpen():
                
                cmd = "AT+HTTPDATA=%d,%d" % (size, 10000)
                self.send_cmd(cmd)
                sleep(1)
                (self.ser.write(data, ))

            sleep(1)

            print("Waiting ",end="", flush=True)

            while True:
                result = self.ser.readline()
                result = result.decode('ascii')
                print(".", end="", flush=True)

                if result.find("DOWNLOAD",0, len(result))!=-1:
                    print("\n"+result)
                    break
                elif result.find("OK", 0, len(result))!=-1:
                    print("\n"+result)
                    break
                elif result.find("ERROR", 0, len(result))!=-1:
                    print("\n"+result)
                    break
            print("")

        self.send_cmd_action("AT+HTTPACTION=1")


    def send_data(self, device, height, battery):

        self.send_cmd("AT+HTTPPARA=\"CID\",1")
        self.send_cmd("AT+HTTPPARA=\"URL\", \"http://ccrcapi.isdc.org.tw/datapi_v1/sensor_data\"")
        # self.send_cmd("AT+HTTPPARA=\"Content-Disposition\", \"form-data\"")

        data={}
    
        url = 'http://ccrcapi.isdc.org.tw/datapi_v1/sensor_data'
        form_data = {"access_token":"S0YUPrMAre60igE+iMvsWfdxs5MUwwUUMdjkveK/w73J/ANfPJZJYT3t8OP1tF3H ",
                "pass_code":"Winnie the pooh",
                "machine_id":0,
                "height":height,
                "battery":battery}

        req = requests.Request("POST", url, data=form_data)
        prepared = req.prepare()

        data = prepared.body

        self.send_cmd("AT+HTTPPARA=\"CONTENT\", \"%s\"" % prepared.headers['Content-Type'])

        print(type(data))
        # print("Post Response: %s" % str(r.content).replace("<br/>","\n"))


        size = int(prepared.headers['Content-Length'])
        syssize = sys.getsizeof(data)
        print("size with getsize: ", syssize)
        print("size with content-Length: ", size)

        if self.ser.isOpen():
            
            cmd = "AT+HTTPDATA=%d,%d" % (size, 10000)
            self.send_cmd(cmd)
            sleep(1)
            (self.ser.write(data.encode(), ))

        sleep(1)

        print("Waiting ",end="", flush=True)

        while True:
            result = self.ser.readline()
            result = result.decode('ascii')
            print(".", end="", flush=True)

            if result.find("DOWNLOAD",0, len(result))!=-1:
                print("\n"+result)
                break
            elif result.find("OK", 0, len(result))!=-1:
                print("\n"+result)
                break
            elif result.find("ERROR", 0, len(result))!=-1:
                print("\n"+result)
                break
        print("")

        self.send_cmd_action("AT+HTTPACTION=1")


if __name__ == "__main__":
    nbiot = NBiot()
