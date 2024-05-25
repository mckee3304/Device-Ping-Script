import os
import time
import csv
import ssl
import smtplib
from datetime import datetime, date
from prettytable import PrettyTable
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

## CONFIGURE SMTP INFORMATION HERE
# define email addresses to use
addr_to   = 'TO EMAIL'
addr_from = 'FROM EMAIL (Likely the same as the SMTP User)'

# define SMTP email server details
smtp_server = 'SMTP ADDRESS (i.e. smtp.gmail.com)'
smtp_user   = 'SMTP USER'
smtp_pass   = 'SMTP PASSWORD'
## END SMTP CONFIGURATION

# define time
now = datetime.now()

# define script start time
startTime = time.time()
startTimeNormal = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time())) #converts time from epoch to normal

# define PrettyTable
tbl = PrettyTable(["Device", "IPAddress", "Status", "Date/Time"])

# define log file name to include filename + time
logSavePath = './'
logFileNameString = str("ScriptLog-")
logFileDate = now.strftime("%m%d%Y")
LogFileDateString = str(logFileDate)
logFileExtension = ".txt"
logFileName =  os.path.join(logSavePath, logFileNameString + LogFileDateString + logFileExtension)

# create log file
logFile = open(logFileName, "a")

# define results file name to include filename + time
resultsSavePath = './'
resultsFileNameString = str("DeviceReport-")
resultsFileDate = now.strftime("%m%d%Y")
resultsFileDateString = str(resultsFileDate)
resultsFileExtension = ".csv"
resultsFileName =  os.path.join(resultsSavePath, resultsFileNameString + resultsFileDateString + resultsFileExtension)

# create results file
resultsFile = open(resultsFileName, "w", newline="")

# start script 
print("Starting Device Ping Script...")
logFile.write("Start Time: " + str(startTimeNormal) + "\n")

# open list of devices
with open('devicelist.csv', 'r') as csvinput:
    reader = csv.DictReader(csvinput)       
    for row in reader:
        ip = row["IPAddress"]
        response = os.popen(f"ping {ip} -n 2").read()
        if "Received = 1" in response:
            device = row["Device"]
            ipAddress = ip
            statusUp = str("UP")
            print(str(statusUp) + "   " + str(ipAddress) + "   " + str(device))
            # write device issue to log
            logFile.write(str(statusUp) + "     " + str(ipAddress) + "   " + str(device) + "\n")
        elif "Received = 2" in response:
            device = row["Device"]
            ipAddress = ip
            statusUp = str("UP")
            print(str(statusUp) + "   " + str(ipAddress) + "   " + str(device))
            # write device issue to log
            logFile.write(str(statusUp) + "     " + str(ipAddress) + "   " + str(device) + "\n")        
        else:
            device = row["Device"]
            ipAddress = ip
            statusDown = str("Down")
            dateTime = now.strftime("%m/%d/%Y %H:%M:%S")
            print(str(statusDown) + "   " + str(ipAddress) + "   " + str(device))
            # write device issue to log
            logFile.write(str(statusDown) + "   " + str(ipAddress) + "   " + str(device) + "\n")
            # start building our PrettyTable by selecting the elements to be included
            tbl.add_row( [device, ipAddress, statusDown, dateTime] )
            
# convert PrettyTable to csv and write resultsFile 
resultsFile.write(tbl.get_csv_string(sortby="IPAddress"))

# start email of results
print("\n" + "Emailing results...")
        
# create a secure SSL context
context = ssl.create_default_context()

# construct email
msg = MIMEMultipart('alternative')
msg['To'] = addr_to
msg['From'] = addr_from
msg['Subject'] = 'Device Report - ' + str(now.strftime("%m/%d/%Y"))

# create the body of the message (a plain-text and an HTML version).
text = tbl.get_string(sortby="IPAddress")
html = tbl.get_html_string(sortby="IPAddress")

# record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# attach parts into message container.
msg.attach(part1)
msg.attach(part2)
    
try:
    # send the message via SMTP
    s = smtplib.SMTP(smtp_server,587)
    s.ehlo()
    s.starttls(context=context)
    s.ehlo()
    s.login(smtp_user,smtp_pass)
    s.sendmail(addr_from, addr_to, msg.as_string())
    print("\n" + "Email Sent Successfully!")
    # write to log if sending email succeeded
    logFile.write("Sucessfully Sent Email!" + "\n")
    s.quit()
except:
    # write to log if sending email failed
    print("\n" + "Email Failed to Send!")
    logFile.write("Emailing results Failed!" + "\n")  
    
# calculate time it took to complete script
endTime = time.time()
endTimeNormal = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time())) #converts time from epoch to normal
executionTime = ((endTime - startTime)/60)
calulatedTime = round(executionTime, 2)

# close log file
logFile.write("End Time: " + str(endTimeNormal) + "\n")
logFile.write("Total Execution Time: " + str(calulatedTime) + " Minutes" + "\n")
logFile.close()

# script complete
print("\n" + "Device Ping Script Completed!")
