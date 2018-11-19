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


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Linux Antivirus")
    parser.add_argument("FILE", help="Directory or filename to scan")
    parser.add_argument("-u", "--update", help="Update virus and whitelist database",
                        action="store_true")
    args = parser.parse_args()
    if args.update:
        updateDatabase()
        exit(0)

    if os.path.isdir(args.FILE):
        print("Is a directory")
    else:
        checksum = subprocess.check_output(["shasum", args.FILE])
        checksum = checksum.decode('ASCII')
        checksum = checksum.split()
        checksum = checksum[0].rstrip('\n')
        safe = False
        whitelist = open("whitelist.txt", "r")
        for line in whitelist:
            if line.rstrip('\n') == checksum:
                safe = True
                break
        if safe:
            print("File is safe")

