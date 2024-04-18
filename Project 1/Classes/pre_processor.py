import logging
import os
# Configure logging
if not os.path.exists("./Logs"):
    os.mkdir("./Logs")
logging.basicConfig(filename='./Logs/log_file.log', level=logging.INFO)


class PreProcessor:
    def __init__(self):
        # keep track of word count in training data in order to find out which words to replace with <unk>
        self.word_count = {}

    def pad_and_lowercase_sentences(self, in_file, out_file):
        logging.info("Starting PreProcessor.pad_and_lowercase_sentences({}, {})".format(in_file.name, out_file.name))
        # Reset file pointer
        in_file.seek(0)
        out_file.seek(0)

        for sentence in in_file:
            index = sentence.find("\n")
            # place start and end symbols and lowercase the string.
            # the end symbol will be placed in between end of sentence and "\n"
            sentence = "<s> " + sentence.lower()[:index] + " </s>" + sentence.lower()[index:]
            out_file.write(sentence)
        logging.info("Finished PreProcessor.pad_and_lowercase_sentences({}, {})".format(in_file.name, out_file.name))

    def count_occurrences_in_training_data(self, in_file):
        # This function counts the number of occurrences of words in the training corpus. This will be used for the replace_unknowns method.
        logging.info("Starting PreProcessor.count_occurrences({})".format(in_file.name))
        # Reset file pointer
        in_file.seek(0)

        self.word_count = {}
        # Count occurrences of each word
        for sentence in in_file:
            for word in sentence.split():
                # Ignore symbols and line break
                if word == "\n" or word == "<s>" or word == "</s>":
                    continue
                # Count occurrences of each word
                self.word_count[word] = self.word_count.get(word,0)+1
        logging.info("Finished PreProcessor.count_occurrences({})".format(in_file.name))

    def replace_unknowns(self, in_file, out_file):
        logging.info("Starting PreProcessor.replace_unknowns({}, {})".format(in_file.name, out_file.name))
        # Reset file pointer
        in_file.seek(0)
        out_file.seek(0)

        # Replace unknown words with <unk> and write to out_file
        for sentence in in_file:
            new_sentence = ""
            for word in sentence.split():
                # Add symbols to sentence
                if word == "<s>" or word == "</s>":
                    new_sentence += word + " "
                    continue
                # If one occurrence, replace with <unk>
                if (word in self.word_count and self.word_count[word] == 1 and word != "</s>") or (word not in self.word_count and word != "</s>"):
                    new_sentence += "<unk> "
                else:
                    new_sentence += word + " "
            # Write the updated sentence to out_file
            out_file.write(new_sentence + "\n")
        logging.info("Finished PreProcessor.replace_unknowns({}, {})".format(in_file.name, out_file.name))
