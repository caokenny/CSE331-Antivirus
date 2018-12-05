import sys
import os
import binascii
import hashlib


def scanFile(file):
    if os.access(file, os.R_OK):
        # checksum = subprocess.check_output(["shasum", file]).decode('utf-8').split()[0]
        with open(file, "rb") as f:
        	checksum = f.read()
        m = hashlib.sha1()
        m.update(checksum)
        checksum = m.hexdigest()
        whitelist = open("/home/CSE331-Antivirus/whitelist.txt", "r")
        for line in whitelist:
            if line.rstrip('\n') == checksum:
                whitelist.close()
                return True

        viruses = open("/home/CSE331-Antivirus/viruses.txt", "r")
        chunk_size = 1024
        with open(file, "rb") as f:
        	while True:
	            content = binascii.hexlify(f.read(chunk_size)).decode("utf-8")
	            if not content:
	            	break
	            for line in viruses:
	                line = line.split(",")[1].rstrip('\n').split(" ")
	                line = "".join(line)
	                if line in content:
	                    os.chmod(file, 000)
	                    os.rename(file, file + ".infected")
	                    sys.stdout.write("Virus detected: " + file + ".infected" + "\n")
	                    return False
        return True



if __name__ == '__main__':
	file = sys.argv[1]
	scanFile(file)
