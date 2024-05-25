# Device Ping Script
This python script was created to ping devices on your network and provide up/down status. The script then outputs a CSV of all devices that were scanned with their status. In addition, if desired, the script will also send the results via email. 

## Usage
This script requires PrettyTable. Installation is straight forward. From an elevated command prompt, run the following script:

'''
python -m pip install -U prettytable
'''

## Usage
to utilize, open the devicelist.csv and add each of your devices to the list. The first column is the device name and the second column is the device IP address. Ensure the file is saved in the same directory as the DevicePingScript.py script. The script will output CSV file with the results with the Device Name, IPAddress, Status, and Date/Time. 

Once the devicelist.csv file is saved, run the DevicePingScript.py. 

To take this one step further, you can utilize Windows Task Scheduler to run this script on a regular basis. I used this script to email the device status of IP intercoms as a temp solution while we worked to deploy a network monitoring solution. 

## SMTP Setup
To configure SMTP in the script, edit the DevicePingScript.py script in Lines 11-20 with your SMTP information. If utilizing a GMAIL address, follow these instructions to create an App Password for your user: https://knowledge.workspace.google.com/kb/how-to-create-app-passwords-000009237 
<br />
<br />
<br />
<a href="https://www.buymeacoffee.com/mckee3304" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-blue.png" alt="Buy Me A Coffee" height="41" width="174"></a>