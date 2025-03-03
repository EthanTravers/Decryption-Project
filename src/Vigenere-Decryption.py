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

def get_key_length(logger, encryptedText):
    # Find coincidences for each shift
    coincidences = {}
    shiftedText = encryptedText.copy()
    for shift in range(1, len(encryptedText)):
        shiftedText.pop(len(shiftedText)-1)
        # remove the first shift elements from encrypted text
        encryptedTextSection = encryptedText[shift:]
        # check how many coincidences there are with the original text
        coincidences[shift] = get_coincidences(logger, encryptedTextSection, shiftedText)
    # find high anomalies and get average distance between them
    high_anomalies = get_high_anomalies(logger, coincidences)
    average_distance = get_average_distance(logger, high_anomalies)
    return average_distance

def get_coincidences(logger, encryptedTextSection, shiftedText):
    coincidences = 0
    for i in range(len(encryptedTextSection)):
        if encryptedTextSection[i] == shiftedText[i]:
            coincidences += 1
    return coincidences

def get_high_anomalies(logger, coincidences):
    shifts = sorted(coincidences.keys())  # Sort shifts
    peaks = []

    for i in range(1, len(shifts) - 1):
        prev_shift, curr_shift, next_shift = shifts[i - 1], shifts[i], shifts[i + 1]
        if coincidences[curr_shift] > coincidences[prev_shift] and coincidences[curr_shift] > coincidences[next_shift]:
            peaks.append(curr_shift)

    return peaks

def get_average_distance(logger, peaks):
    if len(peaks) < 2:
        return None  # Not enough peaks to compute distance
    distances = [peaks[i + 1] - peaks[i] for i in range(len(peaks) - 1)]
    return np.mean(distances)

def get_vigenere_key(logger, encryptedText, keyLength):
    key = ""
    for i in range(keyLength):
        # Get the ith character of the key
        key += get_vigenere_key_character(logger, encryptedText, encryptedText[i::keyLength])
    return key

def get_vigenere_key_character(logger, encryptedText, subsetEncryptedText):
    """
    Determines the best shift for a Vigenère cipher key character using frequency analysis.
    """
    # Frequency analysis for subset text
    subsetEncryptedTextFrequency = {}
    for char in subsetEncryptedText:
        subsetEncryptedTextFrequency[char] = subsetEncryptedTextFrequency.get(char, 0) + 1

    # Normalize frequencies
    total_chars = sum(subsetEncryptedTextFrequency.values())
    for char in subsetEncryptedTextFrequency:
        subsetEncryptedTextFrequency[char] /= total_chars

    # Sort both dictionaries by keys
    sorted_keys = sorted(english_letter_frequency.keys())

    encryptedCharValues = np.array([english_letter_frequency[k] for k in sorted_keys])
    subsetCharValues = np.array([subsetEncryptedTextFrequency.get(k, 0) for k in sorted_keys])

    shift_scores = {}

    # Try all shifts
    for shift in range(len(sorted_keys)):
        correlation_score = np.sum(encryptedCharValues * subsetCharValues)
        shift_scores[shift] = correlation_score
        subsetCharValues = np.roll(subsetCharValues, -1)  # Circular shift

    # Best shift index
    best_shift = max(shift_scores, key=shift_scores.get)

    # Convert shift number back to letter
    best_shift_char = chr((best_shift % 26) + 97)  # Ensures lowercase mapping

    return best_shift_char


def vigenere_decrypt(logger, ciphertext, key):
    decrypted_text = []
    key = key.lower()
    key_length = len(key)
    key_index = 0  # To track position in key

    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % key_length]) - ord('a')
            if char.isupper():
                new_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                new_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            decrypted_text.append(new_char)
            key_index += 1  # Move to next key letter only if alphabetic char
        else:
            decrypted_text.append(char)  # Preserve spaces and punctuation

    return ''.join(decrypted_text)

def main():
    start_time = time.time()
    logger = get_logger()
    # Take encrypted message file from command line
    if len(sys.argv) != 2:
        sys.exit(1)

    encryptedTextDirectory = sys.argv[1]
    encryptedText = open(encryptedTextDirectory, "r").read()
    logger.info(f"Converting encrypted text to numerical values...")
    # Find spaces and convert text to numerical values
    uniqueChars = []
    numerical_values = []
    for i in range(len(encryptedText)):
        if encryptedText[i] == ' ':
            uniqueChars.append((i, i + 1,' '))
        elif encryptedText[i] == '.':
            uniqueChars.append((i, i + 1,'.'))
        elif encryptedText[i].lower() in alphabet_dict:
            numerical_values.append(alphabet_dict[encryptedText[i].lower()])

    logger.info(f"Attempting to get the key length...")

    # Get the key length
    keyLength = int(get_key_length(logger, numerical_values))
    logger.info(f"Key Length: {keyLength}")

    logger.info(f"Finding the frequency of each character in the encrypted text...")

    # Find the vigenere key
    logger.info("Attempting to find the Vigenere key...")
    key = get_vigenere_key(logger, numerical_values, keyLength)
    end_time = time.time()
    logger.info("Vigenere Key: " + key)
    logger.info(f"Time taken: {end_time - start_time} seconds")

    # Decrypt the message
    logger.info("Decrypting messaging using the key...")
    decryptedText = vigenere_decrypt(logger, encryptedText, key)

    # Write the decrypted text to a file
    decryptedTextFile = open("./Challenge-Text/Q1_Answer.txt", "w")
    decryptedTextFile.write(decryptedText)
    decryptedTextFile.close()
    logger.info("Decrypted text written to Q1_Answer.txt")
if __name__ == "__main__":
    main()