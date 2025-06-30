import random
import nltk
import wikipedia
from nltk.tokenize import word_tokenize

# checking for tokenizer
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading punkt...")
    nltk.download('punkt')

# Tokenizer
def tokenize(text):
    return word_tokenize(text.lower())

#Wikipedia summary
def fetch_wikipedia_info(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except wikipedia.exceptions.DisambiguationError as e:
        for option in e.options:
            try:
                return wikipedia.summary(option, sentences=2)
            except:
                continue
        return f"The topic is too broad. Try being more specific like: {e.options[0]}"
    except wikipedia.exceptions.PageError:
        search_results = wikipedia.search(query)
        for result in search_results:
            try:
                return wikipedia.summary(result, sentences=2)
            except:
                continue
        return "Sorry, I couldn’t find anything on that."
    except Exception:
        return "Something went wrong while fetching information."

# intent patterns
intents = {
    "intents": [
        {
            "tag": "greeting",
            "patterns": ["hi", "hello", "hey", "good morning"],
            "responses": ["Hello!", "Hi there!", "Greetings!"]
        },
        {
            "tag": "name",
            "patterns": ["what is your name", "who are you", "your name"],
            "responses": ["I'm ChatBot!", "I'm your friendly AI assistant."]
        },
        {
            "tag": "bye",
            "patterns": ["bye", "goodbye", "see you later"],
            "responses": ["Goodbye!", "Talk to you later!", "Have a great day!"]
        },
        {
            "tag": "book",
            "patterns": ["recommend a book", "suggest a book", "book recommendation"],
            "responses": []  # Handled dynamically
        },
        {
            "tag": "movie",
            "patterns": ["recommend a movie", "suggest a movie", "movie recommendation"],
            "responses": []
        },
        {
            "tag": "learning",
            "patterns": ["recommend an app", "suggest a learning app", "learning tools", "how to learn coding"],
            "responses": []
        }
    ]
}

# recommendations
recommendation_topics = {
    "book": ["Atomic Habits", "Sapiens", "The Alchemist", "Rich Dad Poor Dad", "Deep Work"],
    "movie": ["Inception", "Interstellar", "The Shawshank Redemption", "The Matrix", "The Dark Knight"],
    "learning": ["Khan Academy", "Coursera", "edX", "SoloLearn", "Codecademy"]
}

#response function
def get_response(user_input):
    user_input = user_input.lower()

    #wikipedia info request
    if any(kw in user_input for kw in ["tell me about", "what is", "who is", "where is"]):
        topic = (
            user_input.replace("tell me about", "")
            .replace("what is", "")
            .replace("who is", "")
            .replace("where is", "")
            .replace("?", "")
            .strip()
        )
        return fetch_wikipedia_info(topic)

    #Token matching
    tokens = set(tokenize(user_input))
    best_match = None
    max_matches = 0

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            pattern_tokens = set(tokenize(pattern))
            common = tokens & pattern_tokens
            if len(common) > max_matches:
                max_matches = len(common)
                best_match = intent

    if best_match:
        tag = best_match["tag"]

        # Wikipedia recommendations
        if tag in recommendation_topics:
            topic = random.choice(recommendation_topics[tag])
            summary = fetch_wikipedia_info(topic)
            return f"{tag.capitalize()} suggestion: {topic}\n{summary}"

        # Static response 
        if max_matches >= 2 or (max_matches >= 1 and len(tokens) <= 2):
            return random.choice(best_match["responses"])

    return "Sorry, I didn't understand that."

# Chat loop
def run_chatbot():
    print("ChatBot: Hello! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("ChatBot: Bye! 👋")
            break
        response = get_response(user_input)
        print("ChatBot:", response)

# Start the chatbot
if __name__ == "__main__":
    run_chatbot()
