from text_statistics import TextStatistics

# Creates a statistic object on the text file and displays the information
if __name__ == '__main__':
    file_path = ""
    text_statistics = TextStatistics(file_path)
    text_statistics.show_statistics()
