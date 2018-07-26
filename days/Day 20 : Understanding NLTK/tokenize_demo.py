import nltk
from nltk.tokenize import sent_tokenize,word_tokenize,WordPunctTokenizer

# Define input text
input_text = "DO you know how tokenization works? It's actually quite interesting! Let's analyse a couple of sentences and figure it out."

# Sentence tokenizer
print("\n Sentence Tokenizer:")
print(sent_tokenize(input_text))

# wordPunt tokenizer
print("\nWord punct tokenizer:")
print(WordPunctTokenizer().tokenize(input_text))