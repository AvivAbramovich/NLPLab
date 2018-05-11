from sklearn.svm import SVC
from sklearn import tree
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_selection import RFE


class Classifier:
    def __init__(self, classifier, classifier_name):
        self.classifier = classifier
        self.classifier_name = classifier_name

    # classifier the data and print the accuracy of the Classifier
    def fit(self, feature_vector, feature_labels,k_times):
        avg_score = 0
        kf = KFold(n_splits=k_times, shuffle=True)
        for train_indexes, test_indexes in kf.split(feature_vector):

            # Init all,  the vector by training set indexes
            training_feature_vector = [feature_vector[i] for i in train_indexes]
            result_training = [feature_labels[i] for i in train_indexes]
            test_feature_vector = [feature_vector[i] for i in test_indexes]
            result_test = [feature_labels[i] for i in test_indexes]

            # Calculate the success rate of the predict vector
            self.classifier.fit(training_feature_vector, result_training)
            predicted_vector = self.classifier.predict(test_feature_vector)
            avg_score += accuracy_score(result_test, predicted_vector)

        avg_score /= k_times
        print(self.classifier_name + ":" + "%.2f" % (avg_score * 100) + "%")

    def estimate(self, feature_vector, feature_labels, num_of_features):
        estimator = self.classifier
        selector = RFE(estimator, num_of_features, step=1)
        selector = selector.fit(feature_vector, feature_labels)
        print(self.classifier_name + ":\n" + selector.support_)
        print(self.classifier_name + ":\n" + selector.ranking_)


class ClassifierFactory:
    def __init__(self):
        self.classifiers = [Classifier(SVC(), 'SVM'),
                            Classifier(MultinomialNB(), 'Naive Bayes:'),
                            Classifier( tree.DecisionTreeClassifier(), 'DecisionTree'),
                            Classifier(KNeighborsClassifier(), 'KNN')]

    def fit_all(self, all_feature_vector, all_label,k_times):
        for classifier in self.classifiers:
            classifier.fit(all_feature_vector,all_label,k_times)

    def estimate_all(self,all_feature_vector, all_label, num_of_features):
        for classifier in self.classifiers:
            classifier.fit(all_feature_vector,all_label, num_of_features)



