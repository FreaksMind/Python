import random

def generate(length = 10, addSpecialChars=False, includeNumbers=False, addUpperChars=False):
    final_set = "qwertyuiopasdfghjklzxcvbnm"
    
    if addSpecialChars:
        final_set += "!@#$%^&*"

    if includeNumbers:
        final_set += "0123456789"

    if addUpperChars:
        final_set += final_set.upper()
    
    char_list = list(final_set)
    random.shuffle(char_list)
    final_password = ""
    for _ in range(0, length):
        final_password += final_set[int(random.uniform(0, len(final_set)))]

    return final_password
