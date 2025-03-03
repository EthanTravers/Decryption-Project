import sys
import logging
from colorama import Fore, Style, init
import numpy as np
import time

# Initialize colorama
init()
# Create a dictionary to map the alphabet to numbers
alphabet_dict = {chr(i + 97): i for i in range(26)}
english_letter_frequency = {
    0: 0.08167,  # a
    1: 0.01492,  # b
    2: 0.02782,  # c
    3: 0.04253,  # d
    4: 0.12702,  # e
    5: 0.02228,  # f
    6: 0.02015,  # g
    7: 0.06094,  # h
    8: 0.06966,  # i
    9: 0.00153,  # j
    10: 0.00772,  # k
    11: 0.04025,  # l
    12: 0.02406,  # m
    13: 0.06749,  # n
    14: 0.07507,  # o
    15: 0.01929,  # p
    16: 0.00095,  # q
    17: 0.05987,  # r
    18: 0.06327,  # s
    19: 0.09056,  # t
    20: 0.02758,  # u
    21: 0.00978,  # v
    22: 0.02360,  # w
    23: 0.00150,  # x
    24: 0.01974,  # y
    25: 0.00074   # z
}

class CustomFormatter(logging.Formatter):
    def format(self, record):
        level_color = {
            'DEBUG': Fore.LIGHTCYAN_EX,
            'INFO': Fore.LIGHTGREEN_EX,
            'WARNING': Fore.LIGHTYELLOW_EX,
            'ERROR': Fore.LIGHTRED_EX,
            'CRITICAL': Fore.LIGHTRED_EX
        }
        log_fmt = f"{Style.BRIGHT}{Fore.LIGHTBLUE_EX}[%(asctime)s]{Style.RESET_ALL} {Style.BRIGHT}{level_color.get(record.levelname, Fore.WHITE)}[%(levelname)s]{Style.RESET_ALL} {Style.BRIGHT}%(message)s{Style.RESET_ALL}"
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)


def get_logger():
    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())

    logger.addHandler(ch)
    return logger

def main():
    start_time = time.time()
    logger = get_logger()
    # Take encrypted message file from command line
    if len(sys.argv) != 2:
        sys.exit(1)

    encryptedTextDirectory = sys.argv[1]
    encryptedText = open(encryptedTextDirectory, "r").read()

    logger.info("Encrypted Text: " + encryptedText)
    logger.info("Encrypted Text Length: " + str(len(encryptedText)))
if __name__ == "__main__":
    main()