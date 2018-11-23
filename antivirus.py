import ssl
import urllib
import argparse
import os
import subprocess


def updateDatabase():
    url = "https://rawcdn.githack.com/caokenny/CSE331-Antivirus/59266d4a9e1c4840550e95afa7565e7217f90e16/whitelist.txt"

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    whitelist = open("whitelist.txt", "w")

    with urllib.request.urlopen(url, context=ctx) as u:
        whitelist.write(u.read().decode('ASCII'))

    whitelist.close()


def scanFile(fileName):
    checksum = subprocess.check_output(["shasum", fileName])
    checksum = checksum.decode('ASCII')
    checksum = checksum.split()
    checksum = checksum[0].rstrip('\n')
    safe = False
    whitelist = open("whitelist.txt", "r")
    for line in whitelist:
        if line.rstrip('\n') == checksum:
            safe = True
            break
    whitelist.close()
    if safe:
        return True
    else:
        #CHECK WITH VIRUS DATABASE TO SEE IF VIRUS
        #IF IS VIRUS RETURN FALSE ELSE RETURN TRUE
        print("IDK")



def scanDir(directory):
    filesInDir = subprocess.check_output(["ls", "-1", directory])
    filesInDir = filesInDir.decode('ASCII')
    filesInDir = filesInDir.split('\n')
    filesInDir.pop(len(filesInDir) - 1)
    for i in range(len(filesInDir)):
        if os.path.isdir(directory + "/" + filesInDir[i]):
            scanDir(directory + "/" + filesInDir[i])
        else:
            if scanFile(directory + "/" + filesInDir[i]) is False:
                #CHANGE FILE PERMISSIONS AND CHANGE TO .INFECTED
                #ELSE CONTINUE LOOPING
                print("IDK")






if __name__ == "__main__":
    ##############PARSING STUFF##############
    parser = argparse.ArgumentParser("Linux Antivirus")
    parser.add_argument("-f", "--file", help="Directory or filename to scan")
    parser.add_argument("-u", "--update", help="Update virus and whitelist database",
                        action="store_true")
    # parser.add_argument("-a", "--access", help="Antivirus will run in the background, scanning files before opened",
    #                     action="store_true")
    args = parser.parse_args()
    ##############PARSING STUFF ENDS##############

    #IF UPDATE IS TRUE, UPDATE DATABASE AND EXIT
    if args.update:
        updateDatabase()
        exit(0)


    if args.file is None:
        #LINK ON ACCESS SCANNING CODE TO SCAN OPENED FILES
        print("IDK")

    else:
        if os.path.isdir(args.file):
            scanDir(args.file)
        else:
            if scanFile(args.file) is False:
                #CHANGE PERMISSIONS AND ADD .INFECTED
                print("IDK")
