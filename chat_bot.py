import nltk
from nltk.corpus import stopwords
import pandas as pd
import heapq
import laptop as Laptop

# Check if NLTK packages are downloaded, if not, download them
nltk_packages = ['punkt', 'stopwords']
for package in nltk_packages:
    try:
        nltk.data.find(package)
    except LookupError:
        nltk.download(package)

# Load csv file
dataset_url = "https://raw.githubusercontent.com/37Degrees/DataSets/master/laptops.csv"
try:
    dataset = pd.read_csv(dataset_url, encoding="ISO-8859-1")
except:
    print("Failed to load dataset")
    dataset = pd.DataFrame()

# Create a list of Laptop objects
Laptop.create_list_of_laptops(dataset)

# Initialize a conversation history
conversation_history = []

# Last computer recommended
actual = 0

# Information options
data = ['light', 'weight', 'lightest', 'weightless', 'cheap', 'cheapest', 'expensive', 'ram', 'fast', 'fastest', 'storage', 'memory', 'gaming']


# Update conversation history
def update_conversation_history(user_input, recommendations):
    entry = {
        "user_input": user_input,
        "recommendations": recommendations["message"]
    }
    conversation_history.append(entry)


# Get previous recommendations
def retrieve_previous_recommendations(input):
    previous_recommendations = []

    for entry in reversed(conversation_history):
        if "continue" in input or "previous" in input or "more" in input or "another" in input:
            # Retrieve recommendations from the previous entry
            previous_recommendations = entry["recommendations"]
            break
        elif input in entry["user_input"]:
            # Retrieve recommendations from the entry matching the user's query
            previous_recommendations = entry["recommendations"]
            break

    return previous_recommendations


# Actual conversation context
def generate_contextual_recommendations(input, previous_recommendations):
    # Combine the current user input with the previous recommendations
    context = filterStopWords(getTokens(input),
                              stopwords.words('english'))  # Preprocess user input (e.g., remove stopwords, tokenize)
    if len(previous_recommendations) > 0:
        previous_recommendations = filterStopWords(getTokens(previous_recommendations), stop_words=stopwords.words(
            'english'))  # Preprocess previous recommendations (e.g., remove stopwords, tokenize)
    context.extend(previous_recommendations)  # Combine with previous recommendations
    # Apply recommendation algorithm based on the updated context
    contextual_recommendations = recommendation_algorithm(context, input)

    return contextual_recommendations


# natural language processing
def getTokens(sentence):
    return nltk.word_tokenize(sentence.lower())


def filterStopWords(tokens, stop_words):
    return [token for token in tokens if token not in stop_words]


# Constants
FILTER_BEST = 'best'
FILTER_CHEAP = 'cheap'
FILTER_CHEAP_PLUS = 'cheapest'
FILTER_EXPENSIVE = 'expensive'
FILTER_RAM = 'ram'
FILTER_RAM_FAST = 'fast'
FILTER_RAM_FAST_PLUS = 'fastest'
FILTER_STORAGE = 'storage'
FILTER_MEMORY = 'memory'
FILTER_SCREEN = 'screen'
FILTER_BIG = 'big'
FILTER_MEDIUM = 'medium'
FILTER_LIGHT = 'light'
FILTER_MANUFACTURER = 'brand'
FILTER_TYPE = 'gaming'


# Rules
def listBrandLaptops(laptops, brand):
    return [laptop for laptop in laptops if laptop.manufacture.lower() == brand]


def get_sorted_laptops(laptops, brand, key, reverse=False):
    if brand[1] is True:
        laptops = [x for x in laptops if x.manufacture.lower() == brand[0]]
    return sorted(laptops, key=key, reverse=reverse)


def highPrice(laptops, brand):
    highest_sorted = get_sorted_laptops(laptops, brand, key=lambda x: x.price, reverse=True)
    return highest_sorted[:min(len(highest_sorted), len(highest_sorted))]


def lowPrice(laptops, brand):
    lowest_sorted = get_sorted_laptops(laptops, brand, key=lambda l: l.price)
    return lowest_sorted[:min(len(lowest_sorted), len(lowest_sorted))]


def lightWeight(laptops, brand):
    if brand[1] is False:
        computer = min(laptops, key=lambda l: l.weight)
    else:
        filter_brand = listBrandLaptops(laptops, brand[0])
        computer = min(filter_brand, key=lambda l: l.weight)
    return computer


def ramCapacity(laptops, brand):
    if brand[1] is False:
        highest_ram = laptops
    else:
        highest_ram = listBrandLaptops(laptops, brand)

    return heapq.nlargest(len(highest_ram), highest_ram, key=lambda x: x.ram)


def highStorage(laptops, brand):
    if brand[1] is False:
        highest_storage = sorted(laptops, key=lambda x: x.storage, reverse=True)
    else:
        filter_brand = listBrandLaptops(laptops, brand[0])
        highest_storage = sorted(filter_brand, key=lambda x: x.storage, reverse=True)

    return highest_storage


def gaming(laptops):
    gaming_laptops = [l for l in laptops if 'Gaming' in l.category]
    highest_ram = sorted(gaming_laptops, key=lambda x: (x.category != 'Gaming', x.ram), reverse=True)
    return highest_ram[:1]


# Search in tokens
def searchBrand(tokens):
    words = tokens.split(" ")
    for i, x in enumerate(words):
        if x == "brand":
            return [tokens[i - 1], True]
    return ["", False]


def searchNum(tokens):
    for x in tokens:
        if x.isnumeric():
            return [x, True]
    return ["1", False]


def user_input(message):
    previous_recommendations = retrieve_previous_recommendations(message)
    # Saludo del usuario
    response = {}
    if any(greeting in message.lower() for greeting in ['hola', 'hi', 'hello']):
        response["message"] = "Hello! I'm here to help you. How can I assist you today?"
    elif any(how_are_you in message.lower() for how_are_you in ['how are you']):
        response["message"] = "I'm fine, thank you. How can I assist you today?"
    else:
        response = generate_contextual_recommendations(message, previous_recommendations)
    if response:
        print(response)
        update_conversation_history(message, response)
    else:
        response["message"] = "Sorry, I don't understand. Could you please rephrase?"
    return response


def recommendation_algorithm(context, input):
    global actual
    tokens = context
    num = searchNum(input)
    brand = searchBrand(input)
    low_price = lowPrice(Laptop.laptops, brand)
    high_price = highPrice(Laptop.laptops, brand)
    fast_options = ramCapacity(Laptop.laptops, brand)
    high_storage = highStorage(Laptop.laptops, brand)
    gaming_opt = gaming(Laptop.laptops)

    if "continue" in input or "another" in input:
        actual += 1
    elif "previous" in input:
        actual -= 1
    elif "more" in input:
        actual += 5
    else:
        actual = 0

    print(tokens)
    if any(keyword in tokens for keyword in ['light', 'weight', 'lightest', 'weightless']):
        computer = lightWeight(Laptop.laptops, brand) if brand else lightWeight(Laptop.laptops, "")
        resp = {
            "message": f"The {'lightest' if brand else 'lightest'} computer on the market is: {computer.manufacture} {computer.model} with a weight of  {computer.weight}kg and a price of {computer.price}€."
        }
        return resp

    if any(keyword in tokens for keyword in ['cheap', 'cheapest']):
        computer = low_price[actual]
        if brand[1] is True:
            if num[1] is False:
                resp = {
                    "message": f"The {computer.model} is their cheapest computer and has a price of {computer.price}€."}
                return resp
            else:
                computer = low_price[:min(int(num[0]), len(low_price))]
                actual = int(num[0])
                resp = {"message": f"The {num[0]} cheapest laptops in the market are:"}
                resp["message"] += " ".join(
                    [f"{laptop.price}€ -> {laptop.model} from {laptop.manufacture}" for laptop in computer])
                return resp
        else:
            if num[1] is False:
                resp = {
                    "message": f"The {computer.model} is the cheapest computer in the market, it is from the brand {computer.manufacture} and has a price of {computer.price}€."}
                return resp
            else:
                computer = low_price[:min(int(num[0]), len(low_price))]
                actual = int(num[0])
                resp = {"message": f"The cheapest {num[0]} laptops in the market are:"}
                resp["message"] += " ".join(
                    [f"{laptop.model} from {laptop.manufacture} -> {laptop.price}€" for laptop in computer])
                return resp

    if 'expensive' in tokens:
        computer = high_price[actual]
        if brand[1] is True:
            if num[1] is False:
                resp = {
                    "message": f"The {computer.model} is their most expensive computer and has a price of {computer.price}€."}
                return resp
            else:
                computer = high_price[:min(int(num[0]), len(high_price))]
                actual = int(num[0])
                resp = {"message": f"The {num[0]} most expensive laptops in the market are:"}
                resp["message"] += " ".join(
                    [f"{laptop.model} from {laptop.manufacture} -> {laptop.price}€" for laptop in computer])
                return resp
        else:
            if num[1] is False:
                resp = {
                    "message": f"The {computer.model} is the most expensive computer in the market nowadays, it is from the brand {computer.manufacture} and has a price of {computer.price}€."}
                return resp
            else:
                computer = high_price[:min(int(num[0]), len(high_price))]
                actual = int(num[0])
                resp = {"message": f"The {num[0]} most expensive laptops in the market are:"}
                resp["message"] += " ".join(
                    [f"{laptop.model} from {laptop.manufacture} -> {laptop.price}€" for laptop in computer])
                return resp

    if any(keyword in tokens for keyword in ['ram', 'fast', 'fastest']):
        computer = fast_options[actual]
        print(len(fast_options), " actual ", actual)
        if brand[1] is True:
            if num[1] is False:
                resp = {
                    "message": f"The {computer.model} is their fastest computer, it has a price of {computer.price}€ and a speed of {int(computer.ram)}GB."}
                return resp
            else:
                computer = fast_options[:min(int(num[0]), len(fast_options))]
                actual = int(num[0])
                resp = {"message": f"The {num[0]} fastest laptops in the market are:"}
                resp["message"] += " ".join(
                    [f"{int(laptop.ram)}GB -> {laptop.model} from {laptop.manufacture} priced at {laptop.price}€"
                     for laptop in computer])
                return resp
        else:
            if num[1] is False:
                resp = {
                    "message": f"The {computer.model} is the fastest computer in the market nowadays, it's from the brand {computer.manufacture}, has a price of {computer.price}€ and a speed of {int(computer.ram)}GB."}
                return resp
            else:
                computer = fast_options[:min(int(num[0]), len(fast_options))]
                actual = int(num[0])
                resp = {"message": f"The {num[0]} fastest laptops in the market are:"}
                resp["message"] += " ".join(
                    [f"{int(laptop.ram)}GB -> {laptop.model} from {laptop.manufacture} priced at {laptop.price}€"
                     for laptop in computer])
                return resp

    if any(keyword in tokens for keyword in ['storage', 'memory']):
        print(high_storage[0])
        computer = high_storage[actual]
        if brand[1] is True:
            if num[1] is False:
                resp = {
                    "message": f"The {computer.model} is their computer with the most memory, it has a price of {computer.price}€ and a memory of {int(computer.storage)}GB."}
                return resp
            else:
                computer = high_storage[:min(int(num[0]), len(high_storage))]
                actual = int(num[0])
                resp = {"message": f"The laptops in the market with the most memory are:"}
                resp["message"] += " ".join(
                    [f"{int(laptop.storage)}GB -> {laptop.model} from {laptop.manufacture} priced at {laptop.price}€"
                     for laptop in computer])
                return resp
        else:
            if num[1] is False:
                resp = {
                    "message": f"The {computer.model} is the computer with the most memory in the market nowadays, it's from the brand {computer.manufacture}, has a price of {computer.price}€ and a storage of {int(computer.storage)}GB."}
                return resp
            else:
                computer = high_storage[:min(int(num[0]), len(high_storage))]
                actual = int(num[0])
                resp = {"message": f"The laptops in the market with the most memory are:"}
                resp["message"] += " ".join(
                    [f"{int(laptop.storage)}GB -> {laptop.model} from {laptop.manufacture} priced at {laptop.price}€"
                     for laptop in computer])
                return resp

    if 'gaming' in tokens:
        computer = gaming_opt[actual]
        resp = {
            "message": f"The best computer we have found for gaming is the {computer.model} with {computer.ram}GB of RAM and {computer.storage}GB of storage."}
        return resp

    resp = {"message": "No specific recommendation found based on the given context."}
    return resp