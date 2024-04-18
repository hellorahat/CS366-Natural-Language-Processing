import os
if not os.path.exists("./Report"):
    os.mkdir("./Report")

def count_bigrams(corpus):
    bigrams = {}
    corpus.seek(0)
    for sentence in corpus:
        words = sentence.split()
        for i in range(len(words) - 1):
            bigram = (words[i], words[i+1])
            bigrams[bigram] = bigrams.get(bigram, 0) + 1
    return bigrams

class Report:
    def __init__(self):
        self.out_file = open("./Report/Questions.txt","w")
        

    def question_1(self, corpus):
        corpus.seek(0)
        word_set = set()
        for sentence in corpus:
            for word in sentence.split():
                if word != "<s>":
                    word_set.add(word)
        self.out_file.write("Question 1: {} word types.\n".format(len(word_set)))

    def question_2(self, corpus):
        corpus.seek(0)
        word_count = 0
        for sentence in corpus:
            for word in sentence.split():
                if word != "<s>":
                    word_count += 1
        self.out_file.write("Question 2: {} word tokens.\n".format(word_count))

    def question_3(self, training_corpus, test_corpus):
        # Reset file pointers
        training_corpus.seek(0)
        test_corpus.seek(0)

        # Count total word tokens and types in training corpus
        training_word_tokens = 0
        training_word_types = set()
        for sentence in training_corpus:
            for word in sentence.split():
                if word != "<s>":
                    training_word_tokens += 1
                    training_word_types.add(word)

        # Count total word tokens and types in test corpus
        test_word_tokens = 0
        test_word_types = set()
        for sentence in test_corpus:
            for word in sentence.split():
                if word != "<s>":
                    test_word_tokens += 1
                    test_word_types.add(word)

        # Count tokens and types not in training corpus
        not_in_training_tokens = 0
        not_in_training_types = set()
        for word in test_word_types:
            if word not in training_word_types:
                not_in_training_tokens += 1
                not_in_training_types.add(word)

        # Calculate percentages
        token_percent = (not_in_training_tokens / test_word_tokens) * 100
        type_percent = (len(not_in_training_types) / len(test_word_types)) * 100

        # Write results to output file
        self.out_file.write("Question 3: {}% of word tokens and {}% of word types from the test corpus did not occur in the training corpus.\n".format(token_percent, type_percent))

    def question_4(self, training_corpus, test_corpus, bigram_model):
        # Reset file pointers
        training_corpus.seek(0)
        test_corpus.seek(0)
        # Count bigrams in training and test corpora
        training_bigrams = count_bigrams(training_corpus)
        test_bigrams = count_bigrams(test_corpus)

        # Count unseen bigrams in test corpus
        unseen_bigrams_count = 0
        for bigram in test_bigrams:
            if bigram not in training_bigrams:
                unseen_bigrams_count += 1

        # Calculate percentage of unseen bigrams
        total_test_bigrams = sum(test_bigrams.values())
        percentage_unseen_bigrams = (unseen_bigrams_count / total_test_bigrams) * 100

        # Write results to output file
        self.out_file.write("Question 4: Percentage of unseen bigrams in the test corpus: {}%\n".format(percentage_unseen_bigrams))
    
    def question_5(self, sentence, unigram_model, bigram_model, bigram_model_add_one_smoothing):
        self.out_file.write("Question 5: Unigram log probability = {},  Bigram log probability = {},   Bigram Add One Smoothing Log Probability = {}+\n".format(unigram_model.log_probability(sentence),bigram_model.log_probability(sentence),bigram_model_add_one_smoothing.log_probability(sentence)))

    def question_6(self, sentence, unigram_model, bigram_model, bigram_model_add_one_smoothing):
        self.out_file.write("Question 6: Calculating perplexity for sample sentence: Unigram perplexity = {},  Bigram perplexity = {},   Bigram Add One Smoothing perplexity = {}+\n".format(unigram_model.perplexity(sentence),bigram_model.perplexity(sentence),bigram_model_add_one_smoothing.perplexity(sentence)))

    def question_7(self, test_corpus, unigram_model, bigram_model, bigram_model_add_one_smoothing):
        self.out_file.write("Question 7: Calculating perplexity for test corpus: Unigram perplexity = {},  Bigram perplexity = {},   Bigram Add One Smoothing perplexity = {}+\n".format(unigram_model.perplexity(test_corpus),bigram_model.perplexity(test_corpus),bigram_model_add_one_smoothing.perplexity(test_corpus)))
