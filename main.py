import sys
import os
import Classes.report as report
import Classes.pre_processor as pre_processor
import Classes.unigram_model as unigram_model
import Classes.bigram_model as bigram_model
import Classes.bigram_add_one_smoothing_model as bigram_add_one_smoothing_model

# Pre-Processing Class
pre_processor = pre_processor.PreProcessor()
# Language Models
unigram_model = unigram_model.UnigramModel()
bigram_model = bigram_model.BigramModel()
bigram_add_one_smoothing_model = bigram_add_one_smoothing_model.BigramAddOneSmoothingModel()

# Input obtained from command line arg
training_file = open(sys.argv[1], "r")
testing_file = open(sys.argv[2], "r")

# Make Directory to hold data
if not os.path.exists("./Data"):
    os.mkdir("./Data")

# Padded & lowercased will be in a seperate file, since those will be necessary to answer some questions.
training_padded_lowercase_file = open("./Data/TRAINING_padded_lowercase.txt","w+")
testing_padded_lowercase_file = open("./Data/TESTING_padded_lowercase.txt", "w+")

# Fully processed files (padded, lowercased, unknown tokens)
training_fully_processed_file = open("./Data/TRAINING_fully_processed_file.txt","w+")
testing_fully_processed_file = open("./Data/TESTING_fully_processed_file.txt","w+")

# Pad and lowercase the training and testing files
pre_processor.pad_and_lowercase_sentences(training_file, training_padded_lowercase_file)
pre_processor.pad_and_lowercase_sentences(testing_file, testing_padded_lowercase_file)

# Count occurrences of each word in the training corpus and store the information in processor class in order to use the replace_unknowns method
pre_processor.count_occurrences_in_training_data(training_padded_lowercase_file)

# Replace unknowns with <unk> for training and testing files
pre_processor.replace_unknowns(training_padded_lowercase_file, training_fully_processed_file)
pre_processor.replace_unknowns(testing_padded_lowercase_file, testing_fully_processed_file)

# Train models
unigram_model.train(training_fully_processed_file)
bigram_model.train(training_fully_processed_file)
bigram_add_one_smoothing_model.train(training_fully_processed_file)

# Answer Questions
report = report.Report()
report.question_1(training_fully_processed_file)
report.question_2(training_fully_processed_file)
report.question_3(training_padded_lowercase_file,testing_padded_lowercase_file)
report.question_4(training_fully_processed_file,testing_fully_processed_file,bigram_model)

q5_data = open("q5_data.txt","r")
q5_padded_lowercase_data = open("q5_padded_lowercase.txt","w+")
q5_fully_processed_data = open("q5_fully_processed.txt","w+")

pre_processor.pad_and_lowercase_sentences(q5_data,q5_padded_lowercase_data)
pre_processor.replace_unknowns(q5_padded_lowercase_data,q5_fully_processed_data)

report.question_5(q5_fully_processed_data, unigram_model, bigram_model, bigram_add_one_smoothing_model)
report.question_6(q5_fully_processed_data, unigram_model, bigram_model, bigram_add_one_smoothing_model)
report.question_7(testing_fully_processed_file, unigram_model, bigram_model, bigram_add_one_smoothing_model)