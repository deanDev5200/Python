from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import wikipedia as wiki
username = "Dean"
wiki.set_lang('id')
question_words = ["apa", "apakah", "siapa", "bagaimana", "kenapa", "kapan", "dimana", 
              "mengapa", "pernahkah", 
             "mana", "bisakah", "maukah", 
             "haruskah", "punyakah", "berapa", "berapakah"]


def stem(text:str):
    fact = StemmerFactory()
    stemmer = fact.create_stemmer()
    return stemmer.stem(text)

def answer_question(question:str):
    respond = ""
    question = question.lower()
    stemmed = stem(question)
    print(stemmed)
    tokenized = word_tokenize(question)

    if any(x in tokenized[0] for x in question_words):
        if tokenized[0] == question_words[0]:
            if stemmed.find("adalah cerdas buat") != -1:
                respond = "Benar sekali!"
            elif stemmed.find("kabar") != -1:
                respond = f"Aku sangat baik, terimakasih telah bertanya, bagaimana denganmu " + username
        elif tokenized[0] == question_words[1]:
            if stemmed.find("adalah cerdas buat") != -1:
                respond = "Benar sekali!"
            elif stemmed.find("kamu cerdas buat") != -1:
                respond = "Benar sekali!"
        elif tokenized[0] == question_words[2]:
            print(tokenized[1])
            if tokenized[1] == "namamu":
                respond = f"Nama saya adalah"
            elif tokenized[1] == "kamu":
                respond = f"Namaku Dia sangat suka programming, Dia berasal dari Buleleng, Bali"
            else:
                search_term = question.split(tokenized[0])[-1]
                f = "Aku tidak menemukan apapun"
                try:
                    f = wiki.summary(search_term, sentences=5)
                except wiki.exceptions.PageError:
                    pass
                respond = f
        elif tokenized[0] == question_words[3]:
            if stemmed.find("gempa kini") != -1:
                respond = "hdskrthseghrd"
        print(respond)
        print("This is a question!")
    else:
        print("This is not a question!")

quest = input("Enter: ")
answer_question(quest)
