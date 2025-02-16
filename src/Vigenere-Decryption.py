import sys
import logging
from colorama import Fore, Style, init

# Initialize colorama
init()
# Create a dictionary to map the alphabet to numbers
alphabet_dict = {chr(i + 97): i for i in range(26)}

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

def get_key_length(logger, encryptedText):
    # Find coincidences for each shift
    coincidences = {}
    logger.info(len(encryptedText)-1)
    for shift in range(1, len(encryptedText)-1):
        pass
    pass


def main():
    logger = get_logger()

    # Take encrypted message from command line
    if len(sys.argv) != 2:
        sys.exit(1)

    encryptedTextDirectory = sys.argv[1]
    encryptedText = open(encryptedTextDirectory, "r").read()
    logger.info(f"Encrypted Text: {encryptedText}")
    logger.info(f"Converting encrypted text to numerical values...")
    # Find spaces and convert text to numerical values
    space_indices = []
    numerical_values = []
    for i in range(len(encryptedText)):
        if encryptedText[i] == ' ':
            space_indices.append((i, i + 1))
        elif encryptedText[i].lower() in alphabet_dict:
            numerical_values.append(alphabet_dict[encryptedText[i].lower()])

    logger.info(f"Space Indices: {space_indices}")
    logger.info(f"Space Indeces Len: {len(space_indices)}")
    logger.info(f"Encrypted Text (Numerical): {numerical_values}")


    logger.info(f"Attempting to get the key length...")
    keyLength = get_key_length(logger, numerical_values)
    logger.info(f"Key Length: {keyLength}")



if __name__ == "__main__":
    main()