from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

fact = StemmerFactory()
stemmer = fact.create_stemmer()
print(stemmer.stem("memecahkan masalahnya dan menerjunkan parasutnya"))