import spacy
import pandas as pd
import random
nlp = spacy.load("en_core_web_sm")
print("Model loaded successfully")
a=random.choice(['Python', 'Java'])
print(a)