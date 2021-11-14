from utils import remove_special_chars, show_colors_statistics
from data import syntactic_words, colors


# Get a path to a text file and create an object that contain the statistics about the file
class TextStatistics:

    # Initializes the object variables
    def __init__(self, file_path):
        self.__count_word_appearance = dict()
        self.__number_of_rows = 0
        self.__number_of_words = 0
        self.__max_sentence = 0
        self.__number_of_sentences = 0
        self.__longest_sequence_not_contain_k = ""

        # Goes through the entire file and takes the desired information for the statistics
        with open(file_path, "r", encoding='unicode_escape') as f:
            self.__sentence = 0
            self.__sequence_not_contain_k = ""
            for line in f:
                self.line_statistics(line)
            f.close()

        # Counts the words that appears only one time in the file
        self.__number_of_unique_words = list(self.__count_word_appearance.values()).count(1) + list(
            colors.values()).count(1)

        # Calculates the average sentence length in the text file
        self.__average_length = self.__number_of_words // self.__number_of_sentences

        # How many times has the most popular word appeared in the text
        self.__max_appearance_word = max(list(self.__count_word_appearance.values()))

        # How many times the most popular word of which have no syntactic significance appeared in the text
        self.__max_appearance_not_syntactic_word = max([val if syntactic_words.get(key) is None else 0 for key, val in
                                                        self.__count_word_appearance.items()])
        self.max_appearance()

    # Extracts the desired information for statistics from a line in the file
    def line_statistics(self, line):
        self.__number_of_rows += 1
        self.k_sequence(line)
        if line.strip():
            line = line.strip()
            self.sentence(line)
            words_of_sentence = line.split(" ")
            for word in words_of_sentence:
                if word != "":
                    self.__number_of_words += 1
                    self.word_statistics(word)
        elif self.__sentence != "":
            self.end_of_sentence()

    # Extracts the desired information for statistics from a word in the file
    def word_statistics(self, word):
        word = remove_special_chars(word)
        if word in colors.keys():
            colors.update({word: colors.get(word) + 1})
        elif word:
            if word in self.__count_word_appearance.keys():
                self.__count_word_appearance.update({word: self.__count_word_appearance.get(word) + 1})
            else:
                self.__count_word_appearance.update({word: 1})

    # Counts the number of sentences in the text
    def sentence(self, line):
        if not any((c in ".?!") for c in line):
            self.__sentence += len(line.split(" "))
        else:
            idx = [line.find("."), line.find("?"), line.find("!")]
            idx = [i if i > -1 else len(line) for i in idx]
            min_idx = min(idx)
            while min_idx < len(line):
                idx[idx.index(min_idx)] = len(line)
                self.__sentence += len(line[:min_idx + 1].split(" "))
                self.end_of_sentence()
                min_idx = min(idx)

    # Checks if the last sentence found is the longest in the text so far
    def end_of_sentence(self):
        self.__max_sentence = self.__sentence if self.__sentence > self.__max_sentence else self.__max_sentence
        self.__number_of_sentences += 1
        self.__sentence = 0

    # Computes sequences without k in the text and checks if the last sequence found is the longest in the text so far
    def k_sequence(self, line):
        k_idx = line.find("k")
        if k_idx == -1:
            self.__sequence_not_contain_k += "\t" + line
        else:
            while k_idx != -1:
                temp_words = " ".join(line[:k_idx].split(" ")[:-1])
                if len(self.__sequence_not_contain_k + temp_words) > len(self.__longest_sequence_not_contain_k):
                    self.__longest_sequence_not_contain_k = self.__sequence_not_contain_k + "\t" + temp_words
                line = " ".join(line[k_idx:].split(" ")[1:])
                k_idx = line.find("k")
            self.__sequence_not_contain_k = line

    # Finds the most popular word and the most popular non-syntactic in the text
    def max_appearance(self):
        flag = False
        for key, value in self.__count_word_appearance.items():
            if (value == self.__max_appearance_not_syntactic_word) and (syntactic_words.get(key) is None):
                self.__max_appearance_not_syntactic_word = key
                if not flag:
                    self.__max_appearance_word = key
                break
            if value == self.__max_appearance_word and not flag:
                self.__max_appearance_word = key
                flag = True

    # Shows the statistics of the text file
    def show_statistics(self):
        text = "\n=============== Text Statistics ===============\n\n" + \
               f"The amount of lines in the file : {self.__number_of_rows}, \n\n" + \
               f"The amount of words in the file : {self.__number_of_words}, \n\n" + \
               f"The amount of unique words in the file : {self.__number_of_unique_words},  \n\n" + \
               f"Average sentence length : {self.__average_length},  \n\n" + \
               f"Maximum sentence length : {self.__max_sentence},  \n\n" + \
               f"The most popular word in the text : \"{self.__max_appearance_word}\",  \n\n" + \
               "The most popular word in the text that as no syntactic meaning : " + \
               f"\"{self.__max_appearance_not_syntactic_word}\", \n\n" + \
               "The longest word sequence in the text that does not contain the letter k : \n\n" + \
               f"\t\"{self.__longest_sequence_not_contain_k}\"."
        text += show_colors_statistics()
        print(text + "\n============== End Of Statistics ==============")
