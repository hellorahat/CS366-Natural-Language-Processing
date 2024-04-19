from sys import argv
import json
import os

if not os.path.exists("BOW_Vectors"):
    os.makedirs("BOW_Vectors")


def process_data(directory):
        if not os.path.exists("BOW_Vectors/"+directory):
            os.makedirs("BOW_Vectors/"+directory)

        # iterate through all classifications
        for classification in os.listdir(directory):
            # make sub-directory BOW_Vectors/classification
            if not os.path.exists("BOW_Vectors"+"/"+directory+"/"+classification):
                os.makedirs("BOW_Vectors"+"/"+directory+"/"+classification)

            classification_path = os.path.join(directory, classification)

            # check if the classification is a directory
            if not os.path.isdir(classification_path): 
                continue

            # iterate through all documents in a classification
            for document in os.listdir(classification_path):
                document_path = os.path.join(classification_path, document)

                # open each txt to process them
                with open(document_path, "r") as file:
                    text = file.read()

                    # lowercase the content
                    text = text.lower()
                    
                    # seperate punctuation from content
                    text = separate_punctuation(text)

                    
                    # update BOW feature vector for the txt
                    BOW_feature_vector = create_BOW_vector(text, classification)

                    # after tjhe txt is processed, put feature vector into .json
                    with open("BOW_Vectors"+"/"+directory+"/"+classification+"/"+document+".json","w") as file:
                        json.dump(BOW_feature_vector, file)

def separate_punctuation(text):
    new_text = ""
    for char in text:
        if is_punctuation(char):
            new_text += " " + char + " "
        else:
            new_text += char
    return new_text

def is_punctuation(char):
    punctuation = ".!?,:;\"\'():-"
    return char in punctuation

def create_BOW_vector(text, classification):
    vec = {}
    words = text.split()
    for word in words:
        if classification not in vec:
            vec[classification] = {}
        vec[classification][word] = vec[classification].get(word, 0) + 1
    return vec


# main
process_data(argv[1])