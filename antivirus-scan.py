import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--update", help="Update virus and whitelist database",
                    action="store_true")
parser.add_argument("N", help="Directory or filename to scan",
                    action="store_true")
args = parser.parse_args()