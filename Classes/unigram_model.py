import logging
import os
import math
# Configure logging
if not os.path.exists("./Logs"):
    os.mkdir("./Logs")
logging.basicConfig(filename='./Logs/log_file.log', level=logging.INFO)

class UnigramModel:
    def __init__(self):
        self.total_words = 0
        self.word_count = {}
    def train(self, corpus):
        logging.info("Starting UnigramModel.train({})".format(corpus.name))
        # Reset file pointer
        corpus.seek(0)

        # Determine frequency
        for sentence in corpus:
            for word in sentence.split():
                # Don't count <s>
                if word != "<s>":
                    self.word_count[word] = self.word_count.get(word,0)+1
                    self.total_words += 1

        logging.info("Finished UnigramModel.train({})".format(corpus.name))

    def calculate_probability(self, word):
        probability = self.word_count.get(word,0) / self.total_words
        return probability
    
    def log_probability(self, corpus):
        corpus.seek(0)
        log_prob = 0.0
        for sentence in corpus:
            for word in sentence:
                if word != "<s>":
                    unigram_prob = self.calculate_probability(word)
                    if unigram_prob > 0:
                        log_prob += math.log2(self.calculate_probability(word))
        return log_prob
    
    def perplexity(self, corpus):
        corpus.seek(0)
        log_prob = 0.0
        for sentence in corpus:
            for word in sentence.split():
                if word != "<s>":
                    word_prob = self.calculate_probability(word)
                    if word_prob > 0:
                        log_prob += math.log2(word_prob)
        log_prob_avg = log_prob / self.total_words
        perplexity = 2 ** (-log_prob_avg)
        return perplexity