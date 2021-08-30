import paramiko
import time
import re
import traceback
import sys
import os # To get your environment variables
import schedule

# Logging Levels #
################
#  CRITICAL 50
#  ERROR    40
#  WARNING  30
#  INFO     20
#  DEBUG    10
###############

# If you want to send logging messages to someone using your email and don't want to hardcode your password in your script
#    ,you should create environment variables and then get information from those.
# To set your environment variable permanently, create a .sh file in /etc/profile.d/ with content: "export ..."
# Python doesn't support 2-step authentication. So if your email has been enabled that feature, you can bypass by 
#    creating an app password (login to your email and create it) and attach with your script
EMAIL_ID = os.environ.get("EMAIL_ID")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")


# Import logging
import logging, logging.handlers # logging.handlers is for email usage

# Define a logger
logger = logging.getLogger("SSH_Parser") # Just a name for this logger

# Set a minimum level for logger. It will track every message from this level to higher ones.
#    By default, logger's level is WARNING. It's better to set it to lower level
logger.setLevel(logging.DEBUG)

# Create handler: FileHandler for file or StreamHandler for stdout
fileHandlerInfo = logging.FileHandler("02_show_ver_info.log")
fileHandlerDebug = logging.FileHandler("02_show_ver_debug.log")
streamHandler = logging.StreamHandler(sys.stdout)
smtpHandler = logging.handlers.SMTPHandler(mailhost=("smtp.gmail.com", 587), # 465 doesn't work
                                           fromaddr=EMAIL_ID,
                                           toaddrs=["php22800@gmail.com"],
                                           subject="Logging Messages From Python",
                                           credentials=(EMAIL_ID, EMAIL_PASSWORD),
                                           secure=() # Use TLS
                                          )

# Set level for handler. What is the difference between logger's level and handler's level?
#    You can think like this: Logger's level is a global restriction. If logger's level is WARNING and handler's level
#    is DEBUG, only messages which fall into WARNING and above are tracked. Handler's level must be in range
#    of logger's one. 
fileHandlerInfo.setLevel(logging.INFO)
fileHandlerDebug.setLevel(logging.DEBUG)
streamHandler.setLevel(logging.WARNING)
smtpHandler.setLevel(logging.WARNING)

# Create formatter (logging message)  and associate with handlers
#    Reference: https://docs.python.org/3/library/logging.html#logrecord-attributes
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(process)d - %(message)s") # Create
fileHandlerInfo.setFormatter(formatter) # Assosciate
fileHandlerDebug.setFormatter(formatter) # Associate
streamHandler.setFormatter(formatter) # Associate
smtpHandler.setFormatter(formatter) 

# Add handlers to the logger
logger.addHandler(fileHandlerInfo)
logger.addHandler(fileHandlerDebug)
logger.addHandler(streamHandler)
logger.addHandler(smtpHandler)

versionPattern = re.compile(r"Version (\S+)")
modelPattern = re.compile(r"Linux (\S+).+")
serialNumberPattern = re.compile(r"Processor board ID (\S+)")
uptimePattern = re.compile(r"(.+) uptime is (.+)")

# Set a message for initializng connection (just for more readable to read the log)
#    Note: It still depends on the logger's level you have set. If you set it to higher (like WARNING), this line won't 
#    work
logger.info(f"{'#'*15} INITIALIZING THE SCRIPT {'#'*15}")

def parser():
    def parse_cisco_version(hostname, username, password):
        # Set a message for connecting to the device
        logger.info(f"Connecting to the device: {hostname}")
        # Set a message for printing username
        logger.info(f"Username: {username}")
        try:
            print("="*25 + " Connecting to device " + hostname  + " " + "="*25)
            session = paramiko.SSHClient()
            session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            session.connect(hostname=hostname,
                            username=username,
                            password=password
                           )
            # Connected
            logger.info("Connected!!!")
            deviceAccess = session.invoke_shell()
            logger.info("Entering privilge EXEC mode...")
            deviceAccess.send(b"enable\n")
            time.sleep(0.5)
            deviceAccess.send(b"123\n")
            time.sleep(0.5)
            deviceAccess.send(b"terminal length 0\n")
            time.sleep(0.5)
            logger.info("Executing command: 'show version'")
            deviceAccess.send(b"show version\n")
            time.sleep(1)
            output = deviceAccess.recv(65000).decode("ascii")
            #print(output)

            # Received output
            # Store the output as debug
            logger.info("Received output")
            logger.debug(f"Output data: {output}")

            versionMatched = versionPattern.search(output)
            versionResult = "IOS version".ljust(18) + ": " + versionMatched.group(1)
            print(versionResult)
            logger.info(versionResult)

            modelMatched = modelPattern.search(output)
            modelResult = ("Model".ljust(18) + ": " + modelMatched.group(1))
            print(modelResult)
            logger.info(modelResult)

            serialNumberMatched = serialNumberPattern.search(output)
            serialNumberResult = "Serial number".ljust(18) + ": " + serialNumberMatched.group(1)
            print(serialNumberResult)
            logger.info(serialNumberResult)

            uptimeMatched = uptimePattern.search(output)
            hostnameResult = "Hostname".ljust(18) + ": " + uptimeMatched.group(1)
            uptimeResult = "Uptime".ljust(18) + ": " + uptimeMatched.group(2)
            print(hostnameResult)
            print(uptimeResult)
            logger.info(hostnameResult)
            logger.info(uptimeResult)

            logger.info("Completed!")
            session.close()
        except paramiko.ssh_exception.AuthenticationException:
            #traceback.print_exc()
            print("Authentication failed!")
            logger.warning("Authentication failed!")
        except AttributeError:
            #traceback.print_exc()
            print("Parsing error. Please check your command")
            logger.error("Parsing error. Please check your command\n")
        except:
            #traceback.print_exc()
            print("Unable to connect to the device")
            logger.critical("Unable to connect to the device")
    parse_cisco_version("192.168.2.101", "admin", "admin")

#parse_cisco_version("192.168.2.101", "admin", "admin")
#schedule.every(15).seconds.do(parse_cisco_version("192.168.2.101", "admin", "admin")) # This is not allowed
schedule.every(15).seconds.do(parser)

while True:
    schedule.run_pending()
    time.sleep(1)

