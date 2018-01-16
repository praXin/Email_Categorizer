import nltk
import random
import os
from nltk.tokenize import word_tokenize
import pickle
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC, NuSVC

def cat():
    business = os.fsencode("C:/Users/pravi/Anaconda3/PROGRAMS/Mini_Project/preprocessed_dataset/Business/") #Give your dataset paths here
    document_edit= os.fsencode("C:/Users/pravi/Anaconda3/PROGRAMS/Mini_Project/preprocessed_dataset/Document editing or checking/")
    employment_arrangements = os.fsencode("C:/Users/pravi/Anaconda3/PROGRAMS/Mini_Project/preprocessed_dataset/Employment arrangements/")
    logistic_arrangements = os.fsencode("C:/Users/pravi/Anaconda3/PROGRAMS/Mini_Project/preprocessed_dataset/Logistic Arrangements/")
    personal_prof = os.fsencode("C:/Users/pravi/Anaconda3/PROGRAMS/Mini_Project/preprocessed_dataset/Personal but in professional context/")
    purely_personal = os.fsencode("C:/Users/pravi/Anaconda3/PROGRAMS/Mini_Project/preprocessed_dataset/Purely Personal/")
    documents = []
    all_words = []

    os.chdir("C:/Users/pravi/Anaconda3/PROGRAMS/Mini_Project/preprocessed_dataset/Business/")
    for file in os.listdir(business):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            op = open(filename,"r")
            f = op.read()
            for w in word_tokenize(f):
                all_words.append(w.lower())
            documents.append( (f,"business") )
            op.close()

    os.chdir("..")
    os.chdir("C:/Users/pravi/Anaconda3/PROGRAMS/Mini_Project/preprocessed_dataset/Document editing or checking/")
    for file in os.listdir(document_edit):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            op = open(filename,"r")
            f = op.read()
            for w in word_tokenize(f):
                all_words.append(w.lower())
            documents.append( (f,"document_edit") )
            op.close()

    os.chdir("..")
    os.chdir("C:/Users/pravi/Anaconda3/PROGRAMS/Mini_Project/preprocessed_dataset/Employment arrangements/")
    for file in os.listdir(employment_arrangements):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            op = open(filename,"r")
            f = op.read()
            for w in word_tokenize(f):
                all_words.append(w.lower())
            documents.append( (f,"employment_arrangements") )
            op.close()

    os.chdir("..")
    os.chdir("C:/Users/pravi/Anaconda3/PROGRAMS/Mini_Project/preprocessed_dataset/Logistic Arrangements/")
    for file in os.listdir(logistic_arrangements):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            op = open(filename,"r")
            f = op.read()
            for w in word_tokenize(f):
                all_words.append(w.lower())
            documents.append( (f,"logistic_arrangements") )
            op.close()

    os.chdir("..")
    os.chdir("C:/Users/pravi/Anaconda3/PROGRAMS/Mini_Project/preprocessed_dataset/Personal but in professional context/")
    for file in os.listdir(personal_prof):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            op = open(filename,"r")
            f = op.read()
            for w in word_tokenize(f):
                all_words.append(w.lower())
            documents.append( (f,"personal_prof") )
            op.close()

    os.chdir("C:/Users/pravi/Anaconda3/PROGRAMS/Mini_Project/preprocessed_dataset/Purely Personal/")
    for file in os.listdir(purely_personal):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            op = open(filename,"r")
            f = op.read()
            for w in word_tokenize(f):
                all_words.append(w.lower())
            documents.append( (f,"purely_personal") )
            op.close()

    os.chdir("..")
    os.chdir("..")
    word_features = list(all_words)[:5000]

    featuresets = [(find_features(mail, word_features), category) 
                    for (mail, category) in documents]

    random.shuffle(featuresets)
    
    train_num = int(0.85*(len(featuresets))) #85% of featuresets is used for training
    test_num = int(0.15*(len(featuresets))) #15% of featuresets is used for testing
    training_set = featuresets[:train_num]
    testing_set = featuresets[-test_num:]

    classifier = nltk.NaiveBayesClassifier.train(training_set)
    p = open('my_classifier.pickle', 'wb')
    pickle.dump(classifier, p)
    p.close()
    print("Naive Bayes accuracy percent: ", (nltk.classify.accuracy(classifier, testing_set))*100)

    MNB_classifier = SklearnClassifier(MultinomialNB())
    MNB_classifier.train(training_set)
    p5 = open('my_MNB_classifier.pickle', 'wb')
    pickle.dump(MNB_classifier, p5)
    p5.close()
    print("Multinomial NB accuracy percent: ",(nltk.classify.accuracy(MNB_classifier, testing_set))*100)

    LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
    LogisticRegression_classifier.train(training_set)
    p6 = open('my_logisticRegression_classifier.pickle', 'wb')
    pickle.dump(LogisticRegression_classifier, p6)
    p6.close()
    # return LogisticRegression_classifier.classify(find_features(text))
    print("Logistic Regression accuracy percent: ",(nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

    LinearSVM_classifier = SklearnClassifier(LinearSVC())
    LinearSVM_classifier.train(training_set)
    p7 = open('my_linear_svc_classifier.pickle', 'wb')
    pickle.dump(LinearSVM_classifier, p7)
    p7.close()
    print("Linear SVM accuracy percent: ",(nltk.classify.accuracy(LinearSVM_classifier, testing_set))*100)

def find_features(document,wf):
    words = word_tokenize(document)
    features = {}
    for w in wf:
        features[w] = (w in words)
    return features
if __name__=="__main__":
	cat()