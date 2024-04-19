import re
class pre_process:
    def process_data(directory):
        # go to each class folder
        # iterate through the txts
        # iterate through the txt character by character
        # make the string lowercase
        # when punctuation is found, add a space before it ||| i.e. is_punctuation(char)
        pass
    def separate_punctuation(text):
        punctuation = r'[.!?,:;"\'():-]'
        processed_text = re.split(punctuation, text)
        return processed_text
    def is_punctuation(char):
        pass