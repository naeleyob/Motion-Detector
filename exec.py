import RPi.GPIO as GPIO
import time
import datetime
import os
import socket


def getTime():
    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    return date_time

def log(date_time):
    file = open("timelogs.txt", "w")
    file.write(date_time)
    file.write('\n')
    file.close()

def appendLog(date_time):
    file = open("timelogs.txt", "a")
    file.write(date_time)
    file.write('\n')
    file.close()




if __name__ == '__main__':


    s = socket.socket()
    host = socket.gethostname()
    #print("hostname recieved!")
    print("The Host Name is: %s"% host)
    port = 8080
    s.bind(('', port))
    s.listen(1)
    print("establishing connection...")
    #time.sleep(2)
    conn, addr = s.accept()
    print("Connection established!")


    #sensor = 17
    #LED = 18

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(18,GPIO.OUT)

    GPIO.setup(17, GPIO.IN)
    GPIO.setwarnings(False)

    state = 0
    print("Awaiting motion")
    tally = 0

    try:
        while True:
            #time.sleep(0.1)
            state = GPIO.input(17)


            if state == 1:
                GPIO.output(18,True)
                date_time = getTime()
                if tally == 0:
                    log(date_time)
                else:
                    appendLog(date_time)
                tally += 1

                time.sleep(5)
            else:
                GPIO.output(18,False)
                #time.sleep(2)
    except KeyboardInterrupt:
        filename = "timelogs.txt"
        file = open(filename, 'rb')
        toSend = file.read(1024)
        conn.send(toSend)
        print("\nMotion detector stopped and the log file has ben transmitted successfully!")
        os.system("rm timelogs.txt")
    finally:
        GPIO.cleanup()
