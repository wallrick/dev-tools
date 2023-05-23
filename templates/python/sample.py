#!env python3

import sys
import getopt
import requests


def help():
    print(sys.argv[0] + " -i <argi> -o <argo>")
    sys.exit()


def http_client():
    api_url = "https://apikeys.googleapis.com/v2/keys:lookupKey"
    response = requests.get(api_url)
    return response.json()


def main(argv):
    argi = ("",)
    argo = ""
    opts, args = getopt.getopt(argv[1:], "hi:o:", ["argi=", "argo="])
    for opt, arg in opts:
        if opt == "-h":
            help()
        elif opt in ("-i", "--argi"):
            argi = arg.strip()
        elif opt in ("-o", "--argo"):
            argo = arg.strip()

    print("argi - ", argi)
    print("argo - ", argo)

    n = len(sys.argv)
    print("\nTotal arguments passed:", n - 1)
    print("Name of script:", sys.argv[0])
    print("Arguments passed:", end=" ")

    for i in range(1, n):
        print(sys.argv[i], end=" ")

    print("\n\nhttp client result: " + str(http_client()))


if __name__ == "__main__":
    main(sys.argv)
