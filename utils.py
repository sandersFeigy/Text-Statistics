# Get a string and return the string without special chars
def remove_special_chars(word):
    lower_word = ""
    for char in word:
        lower_word += char.lower() if char.isalnum() else ""
    return lower_word

