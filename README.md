# CSE331 Project - Antivirus for Linux
Before running the following commands:
- Make sure the antivirus program is in your current directory
- Make sure the antivirus program is executable
- Make sure you have Ubuntu 16.04 (strictly 32-bit version only) and Python3 on VirtualBox


```
usage: ./antivirus [-h] [-f FILE] [-u]

optional arguments:

  -h, --help            show this help message and exit
  
  -f FILE, --file FILE  a file or directory for scanning
  
  -u, --update          update whitelist and viruses database
```

## Update Whitelist/Viruslist Database
```
./antivirus -u
```
OR
```
./antivirus --update
```

## On Demand Scanning
```
./antivirus -f FILE
```
OR
```
./antivirus --file FILE
```

## On Access Scanning
```
sudo make clean all
sudo insmod antivirus_open.ko
```

## Stop On Accessing Scanning
```
sudo rmmod antivirus_open
```
