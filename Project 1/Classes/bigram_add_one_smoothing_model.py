import logging
import os
import math
# Configure logging
if not os.path.exists("./Logs"):
    os.mkdir("./Logs")
logging.basicConfig(filename='./Logs/log_file.log', level=logging.INFO)

class BigramAddOneSmoothingModel:
    def __init__(self):
        self.total_words = 0
        self.word_count = {}

    def train(self, corpus):
        logging.info("Starting BigramAddOneSmoothingModel.train({})".format(corpus.name))
        # Reset file pointer
        corpus.seek(0)
        for sentence in corpus:
            for word in sentence.split():
                if word != "<s>":  # Don't include <s>
                    self.word_count[word] = self.word_count.get(word,0)+1
                    self.total_words += 1
        logging.info("Finished BigramAddOneSmoothingModel.train({})".format(corpus.name))

    def calculate_probability(self, previous_word, current_word):
        if current_word == "<s>":
            current_word_frequency = 0
        else:
            current_word_frequency = self.word_count.get(current_word,0)
        if previous_word == "<s>":
            previous_word_frequency = 0
        else:
            previous_word_frequency = self.word_count.get(previous_word,0)
        if previous_word_frequency == 0:
            return 0.0
        return current_word_frequency + 1/previous_word_frequency + self.total_words

    def log_probability(self, corpus):
        corpus.seek(0)
        log_prob = 0.0
        previous_word = "<s>"
        for sentence in corpus:
            for word in sentence.split()[1:]:
                # Retrieve the probability of the bigram from the model
                print("previous:" + previous_word)
                print("current: " + word)
                bigram_prob = self.calculate_probability(previous_word, word)
                if bigram_prob > 0:
                    log_prob += math.log2(bigram_prob)  # Compute log probability
                previous_word = word  # Update previous_word for next iteration
        return log_prob
    
    def perplexity(self, corpus):
        corpus.seek(0)
        log_prob = 0.0
        previous_word = "<s>"
        num_words = 0

        for sentence in corpus:
            for word in sentence.split()[1:]:
                bigram_prob = self.calculate_probability(previous_word, word)
                if bigram_prob > 0:
                    log_prob += math.log2(bigram_prob)
                    num_words += 1
                previous_word = word  # Update previous_word for next iteration

        log_prob_avg = log_prob / num_words
        perplexity = 2 ** (-log_prob_avg)
        return perplexity