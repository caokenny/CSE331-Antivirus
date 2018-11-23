# CSE331-Antivirus
```
usage: Linux Antivirus [-h] [-f FILE] [-u]

optional arguments:

  -h, --help            show this help message and exit
  
  -f FILE, --file FILE  Directory or filename to scan
  
  -u, --update          Update virus and whitelist database
```

## Updating Whitelist/Virus Database
```
python3 antivirus.py -u
```
OR
```
python3 antivirus.py --update
```

## On Demand Scanning
```
python3 antivirus.py -f file.txt
```
OR
```
python3 antivirus.py --file file.txt
```
NOTE: file name must be an absolute path if the file is not in the same directory as antivirus.py for example if file.txt is loacted on my Desktop:
```
python3 antivirus.py -f /Users/KennyCao/Desktop/file.txt
```

## On Access Scanning
```
python3 antivirus.py
```
Simply run antivirus.py with no flags or arguments
