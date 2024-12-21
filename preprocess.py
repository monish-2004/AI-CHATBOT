import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Ensure necessary nltk resources are downloaded
nltk.download('punkt')
nltk.download('wordnet')

# Define preprocess_input function
def preprocess_input(user_input):
    """
    This function takes user input, tokenizes it, and performs lemmatization.

    Args:
    - user_input (str): The user input string.

    Returns:
    - list: A list of lemmatized words from the user input.
    """
    # Tokenize the input sentence into words
    words = word_tokenize(user_input)
    
    # Lemmatize each word and convert it to lowercase
    lemmatized_words = [lemmatizer.lemmatize(word.lower()) for word in words]
    
    return lemmatized_words
