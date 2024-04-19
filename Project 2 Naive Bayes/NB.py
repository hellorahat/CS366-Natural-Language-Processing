from sys import argv
import os
from pathlib import Path
import json

vectors_directory = ("./BOW_Vectors")

class NB:
    def __init__(self):
        self.prior_probabilities = {}
        self.conditional_probabilities = {}

    def train_NB(self, training_directory, NB_parameters_outfile):
        base_dir = os.path.dirname(training_directory)

        # STEP 1: Get prior probabilities
        document_frequency = {}
        total_documents = 0

        # iterate through all classifications in the training directory
        for classification in os.listdir(training_directory):
            classification_path = os.path.join(training_directory, classification)

            # get amount of documents for the current classification
            amount_of_documents = len(os.listdir(classification_path))
            
            # amount of documents in a class
            document_frequency[classification] = amount_of_documents
            # total documents in all classes
            total_documents += amount_of_documents

        for classification, frequency in document_frequency.items():
            self.prior_probabilities[classification] = frequency/total_documents # set prior probability
            print("prior_probabilities[{}] = {} / {} = {}".format(classification, frequency, total_documents, frequency/total_documents))

        # STEP 2: Get conditional probabilities
        
        # Get total words in all documents
        total_words_add_one = 0
        word_frequency_dict = {}

        vec_path = vectors_directory+"/"+base_dir
        for classification in os.listdir(vec_path):
            classification_path = os.path.join(vec_path, classification)
            for vec in os.listdir(classification_path):
                vec_file_path = os.path.join(classification_path, vec)
                with open(vec_file_path, "r") as file:
                    feature_vector = json.load(file)
                    total_words_add_one += self.get_words_in_feature_vector(feature_vector)


        # Now calculate conditional probabilities using the total words
        vec_path = vectors_directory+"/"+base_dir
        for classification in os.listdir(vec_path):
            classification_path = os.path.join(vec_path, classification)
            for vec in os.listdir(classification_path):
                vec_file_path = os.path.join(classification_path, vec)
                with open(vec_file_path, "r") as file:
                    feature_vector = json.load(file)
                    for _,word_frequency_dict in feature_vector.items():
                        self.conditional_probabilities[classification] = {}
                        for word,frequency in word_frequency_dict.items():
                            self.conditional_probabilities[classification][word] = (frequency+1)/total_words_add_one # set conditional probability
                            print("conditional_probabilities[{}][{}] = {} / {} = {}".format(classification, word, frequency+1, total_words_add_one, (frequency+1)/total_words_add_one))

        # STEP 3: Store prior probabilities and conditional probabilities in json
        parameters = {
            "prior_probabilities": self.prior_probabilities,
            "conditional_probabilities": self.conditional_probabilities
        }
        parameters_json = json.dumps(parameters)

        with open(NB_parameters_outfile, "w+") as file:
            file.write(parameters_json)

    def test_NB(self, testing_directory):
        base_dir = os.path.dirname(testing_directory)
        total_words_add_one = 0


        # get total words with add one
        vec_path = vectors_directory+"/"+base_dir
        for classification in os.listdir(vec_path):
            classification_path = os.path.join(vec_path, classification)
            for vec in os.listdir(classification_path):
                vec_file_path = os.path.join(classification_path, vec)
                with open(vec_file_path, "r") as file:
                    feature_vector = json.load(file)
                    total_words_add_one += self.get_words_in_feature_vector(feature_vector)

        # classify each document
        vec_path = vectors_directory+"/"+base_dir
        classification_probabilities = {}
        classes = list(self.prior_probabilities.keys()) # get all classes trained on

        for directory in os.listdir(vec_path):
            classification_path = os.path.join(vec_path, directory)
            for vec in os.listdir(classification_path):
                vec_file_path = os.path.join(classification_path, vec)
                with open(vec_file_path, "r") as file:
                    feature_vector = json.load(file)
                    for _,word_frequency_dict in feature_vector.items():
                        for classification in classes:
                            classification_probabilities[classification] = self.prior_probabilities[classification]
                        for word,frequency in word_frequency_dict.items():
                            for classification in classes:
                                if word in self.conditional_probabilities[classification]:
                                    classification_probabilities[classification] *= (self.conditional_probabilities[classification][word]**frequency) # conditional_probability^frequency
                                else:
                                    print(classification_probabilities[classification])
                                    classification_probabilities[classification] *= (1/total_words_add_one)**frequency # if word not found, add one smoothing distributes probability mass
                        for classification, probability in classification_probabilities.items():
                            print("classification_probabilities[{}] = {}".format(classification,probability))

                        max_class = max(classification_probabilities, key=classification_probabilities.get)
                        print(max_class)
    def get_words_in_feature_vector(self, feature_vector):
        total_words_add_one = 0
        for classification, word_frequency_dict in feature_vector.items():
            for word,frequency in word_frequency_dict.items():
                total_words_add_one += frequency + 1
        return total_words_add_one


NB_Model = NB()
training_directory = argv[1]
testing_directory = argv[2]
NB_parameters_outfile = argv[3]
outFile = argv[4]

NB_Model.train_NB(training_directory, NB_parameters_outfile)
NB_Model.test_NB(testing_directory)