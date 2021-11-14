from data import colors


# Get a string and return the string without special chars
def remove_special_chars(word):
    lower_word = ""
    for char in word:
        lower_word += char.lower() if char.isalnum() else ""
    return lower_word


# Shows colors.txt appeared in the text file
def show_colors_statistics():
    text = ""
    for color, counter in colors.items():
        if counter == 1:
            text += color + " appears " + str(counter) + " time.\n"
        elif counter > 1:
            text += color + " appears " + str(counter) + " times.\n"
    if text:
        return "\n\nColors in the text :\n\n" + text + "\n"
