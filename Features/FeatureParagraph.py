from common import Paragraph
import nltk
from nltk.corpus import stopwords
from nltk.tag.stanford import StanfordNERTagger

st = StanfordNERTagger('C:\\Users\\Lior\\Documents\\GitHub\\NLPLab\\stanford-ner-2018-02-27\\classifiers/english.all.3class.distsim.crf.ser.gz',
                       'C:\\Users\\Lior\\Documents\\GitHub\\NLPLab\\stanford-ner-2018-02-27\\stanford-ner.jar',
                       encoding='utf-8')


insecured_word = ['kind of', 'likely']
personal_experience = ['my', 'mine']


class FeatureParagraph:
    def __init__(self, paragraph, label, features_names=None):
        self.paragraph = paragraph
        self.label = label
        self.features_names = features_names
        self.feature_vector = []

        for feature_name in features_names:
            try:
                getattr(self, feature_name)()
            except:
                print(feature_name)
                raise

    def words_avg_in_sentence(self):
        if len(self.paragraph.sentences) != 0:
            self.feature_vector.append((len(nltk.word_tokenize(self.paragraph.text)) / len(self.paragraph.sentences)))
        else:
            self.feature_vector.append(0)

    def words_avg_in_time(self):
        try:
            time = self.paragraph.end_time - self.paragraph.start_time
        except:
            time = 0

        if time != 0:
            self.feature_vector.append(len(nltk.word_tokenize(self.paragraph.text)) / time)
        else:
            self.feature_vector.append(0)

    def word_sentences_in_time(self):
        try:
            time = self.paragraph.end_time - self.paragraph.start_time
        except:
            time = 0

        if time != 0:
            self.feature_vector.append(len(self.paragraph.sentences) / time)
        else:
            self.feature_vector.append(0)

    def real_words_feature(self):
        list_words = nltk.word_tokenize(self.paragraph.text)
        total_words = len(list_words)
        real_words = [w for w in list_words if w not in stopwords.words('english')]
        self.feature_vector.append(len(real_words) / total_words)
        self.feature_vector.append(len(real_words))

    def count_numbers(self):
        amount_of_numbers = 0
        for sent in nltk.sent_tokenize(self.paragraph):
            tokens = nltk.tokenize.word_tokenize(sent)
            for token in tokens:
                try:
                    float(token)
                    amount_of_numbers += 1
                except:
                    a = 3

        self.feature_vector.append(amount_of_numbers)

    def person_mentioned(self):
        amount_of_person_mentioned = 0
        for sent in self.paragraph.sentences:
            tokens = nltk.tokenize.word_tokenize(sent)
            tags = st.tag(tokens)
            for tag in tags:
                if tag[1] == 'PERSON':
                    amount_of_person_mentioned += 1

        self.feature_vector.append(amount_of_person_mentioned)

    def is_personal_experience(self):
        is_personal_experience = 0
        for sent in self.paragraph.sentences:
            tokens = nltk.tokenize.word_tokenize(sent)
            for token in tokens:
                if token in personal_experience:
                    is_personal_experience = 1

        self.feature_vector.append(is_personal_experience)

    def is_insecure(self):
        is_insecure_experience = 0
        for sent in self.paragraph.sentences:
            tokens = nltk.tokenize.word_tokenize(sent)
            for token in tokens:
                if token in insecured_word or str(token).endswith('ish'):
                    is_insecure_experience = 1

        self.feature_vector.append(is_insecure_experience)

    def has_quote(self):
        start_pt = self.paragraph.text.find("\"")
        end_pt = self.paragraph.text.find("\"", start_pt + 1)  # add one to skip the opening "
        quote = self.paragraph.text[start_pt + 1: end_pt + 1]  # add one to get the quote excluding the ""

        if start_pt != -1:
            self.feature_vector.append(1)
            self.feature_vector.append(len(quote))
        else:
            self.feature_vector.append(0)
            self.feature_vector.append(0)
