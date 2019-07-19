import serial
from time import sleep


class NBiot:
    
    def __init__(self):

        self.ser = serial.Serial("/dev/serial0", 9600, timeout=0.5)
        sleep(1)


    def setting_init(self):

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
        # self.send_cmd("AT+SAPBR=1,1")
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
                print("[cmd] " + result, end="")
            elif result[0:2]!='\r\n':
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
            result = self.ser.readline().decode('ascii')
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


    def send_data(self, device, height, pm25):
        
        self.send_cmd("AT+HTTPPARA=\"URL\",\"http://ccrc.twnict.com/function/db_access.php?pass=mimicat&device_name=%s&height=%d&pm25=%d\"" % (device,height,pm25))
        sleep(2)
        self.send_cmd_action("AT+HTTPACTION=0")
        sleep(1)
        

if __name__ == "__main__":
    main()


