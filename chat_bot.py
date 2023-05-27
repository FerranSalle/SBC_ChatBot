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
    print(previous_recommendations)
    if len(previous_recommendations) > 0:
        previous_recommendations = filterStopWords(getTokens(previous_recommendations), stop_words=stopwords.words(
            'english'))  # Preprocess previous recommendations (e.g., remove stopwords, tokenize)
    context.extend(previous_recommendations)  # Combine with previous recommendations
    # Apply recommendation algorithm based on the updated context
    contextual_recommendations = recommendation_algorithm(context)

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


def get_sorted_laptops(laptops, key, reverse=False, brand=""):
    if brand:
        laptops = [x for x in laptops if x.manufacture.lower() == brand]
    return sorted(laptops, key=key, reverse=reverse)


def highPrice(laptops, n, brand=""):
    highest_sorted = get_sorted_laptops(laptops, key=lambda x: x.price, reverse=True, brand=brand)
    return highest_sorted[:min(n, len(highest_sorted))]


def lowPrice(laptops, n, brand=""):
    lowest_sorted = get_sorted_laptops(laptops, key=lambda l: l.price, brand=brand)
    return lowest_sorted[:min(n, len(lowest_sorted))]


def lightWeight(laptops, brand):
    if brand == "":
        computer = min(laptops, key=lambda l: l.weight)
    else:
        filter_brand = listBrandLaptops(laptops, brand)
        computer = min(filter_brand, key=lambda l: l.weight)
    return computer


def ramCapacity(laptops, n, brand):
    if brand == "":
        highest_ram = laptops
    else:
        highest_ram = listBrandLaptops(laptops, brand)

    return heapq.nlargest(n, highest_ram, key=lambda x: x.ram)



def highStorage(laptops, n, brand):
    if brand == "":
        highest_storage = sorted(laptops, key=lambda x: x.storage, reverse=True)
    else:
        filter_brand = listBrandLaptops(laptops, brand)
        highest_storage = sorted(filter_brand, key=lambda x: x.storage, reverse=True)

    return highest_storage[:n]


def gaming(laptops):
    gaming_laptops = [l for l in laptops if 'Gaming' in l.category]
    highest_ram = sorted(gaming_laptops, key=lambda x: (x.category != 'Gaming', x.ram), reverse=True)
    return highest_ram[:1]


# Search in tokens
def searchBrand(tokens):
    for i, x in enumerate(tokens):
        if x == "brand" and i > 0:
            return tokens[i - 1]
    return ""


def searchNum(tokens):
    i = 0
    for x in tokens:
        if x.isnumeric():
            return [x, True]
    return ["1", False]


def user_input(message):
    previous_recommendations = retrieve_previous_recommendations(message)
    print("Previous recommendations: ")
    print(previous_recommendations)
    recommendations = generate_contextual_recommendations(message, previous_recommendations)
    print("Recommendations: ")
    print(recommendations)
    if recommendations:
        update_conversation_history(message, recommendations)
    else:
        recommendations["message"] = "Sorry, I don't understand. Could you please rephrase?"
    return recommendations


def recommendation_algorithm(context):
    tokens = context
    print(tokens)

    if any(keyword in tokens for keyword in ['light', 'weight']):
        brand = searchBrand(tokens)
        computer = lightWeight(Laptop.laptops, brand) if brand else lightWeight(Laptop.laptops, "")
        resp = {
            "message": f"The {'lightest' if brand else 'lightest'} computer on the market {'from ' + computer.manufacture if brand else ''} weighs {computer.weight}kg."
        }
        return resp

    if any(keyword in tokens for keyword in ['cheap', 'cheapest']):
        num = searchNum(tokens)
        brand = searchBrand(tokens)
        computer = lowPrice(Laptop.laptops, int(num[0]), brand)
        if brand:
            if num[1] == False:
                resp = {"message": f"The {computer[0].model} is their cheapest computer and has a price of {computer[0].price}€."}
                return resp
            else:
                resp = {"message": f"The {num[0]} cheapest laptops in the market are:"}
                resp["message"] += " ".join([f"{laptop.price}€ -> {laptop.model} from {laptop.manufacture}" for laptop in computer])
                return resp
        else:
            if num[1] == False:
                resp = {"message": f"The {computer[0].model} is the cheapest computer in the market, it is from the brand {computer[0].manufacture} and has a price of {computer[0].price}€."}
                return resp
            else:
                resp = {"message": f"The cheapest {num[0]} laptops in the market are:"}
                resp["message"] += " ".join([f"{laptop.model} from {laptop.manufacture} -> {laptop.price}€" for laptop in computer])
                return resp

    if 'expensive' in tokens:
        num = searchNum(tokens)
        brand = searchBrand(tokens)
        computer = highPrice(Laptop.laptops, int(num[0]), brand)
        if brand:
            if num[1] == False:
                resp = {"message": f"The {computer[0].model} is their most expensive computer and has a price of {computer[0].price}€."}
                return resp
            else:
                resp = {"message": f"The {num[0]} most expensive laptops in the market are:"}
                resp["message"] += " ".join([f"{laptop.price}€ -> {laptop.model} from {laptop.manufacture}" for laptop in computer])
                return resp
        else:
            if num[1] == False:
                resp = {"message": f"The {computer[0].model} is the most expensive computer in the market nowadays, it is from the brand {computer[0].manufacture} and has a price of {computer[0].price}€."}
                return resp
            else:
                resp = {"message": f"The {num[0]} most expensive laptops in the market are:"}
                resp["message"] += " ".join([f"{laptop.price}€ -> {laptop.model} from {laptop.manufacture}" for laptop in computer])
                return resp

    if any(keyword in tokens for keyword in ['ram', 'fast']):
        num = searchNum(tokens)
        brand = searchBrand(tokens)
        computer = ramCapacity(Laptop.laptops, int(num[0]), brand)
        if len(computer) > 0:
            if brand:
                if num[1] == False:
                    resp = {"message": f"The {computer[0].model} is their fastest computer, it has a price of {computer[0].price}€ and a speed of {int(computer[0].ram)}GB."}
                    return resp
                else:
                    resp = {"message": f"The {num[0]} fastest laptops in the market are:"}
                    resp["message"] += " ".join([f"{int(laptop.ram)}GB -> {laptop.model} from {laptop.manufacture} priced at {laptop.price}€" for laptop in computer])
                    return resp
            else:
                if num[1] == False:
                    resp = {"message": f"The {computer[0].model} is the fastest computer in the market nowadays, it's from the brand {computer[0].manufacture}, has a price of {computer[0].price}€ and a speed of {int(computer[0].ram)}GB."}
                    return resp
                else:
                    resp = {"message": f"The {num[0]} fastest laptops in the market are:"}
                    resp["message"] += " ".join([f"{int(laptop.ram)}GB -> {laptop.model} from {laptop.manufacture} priced at {laptop.price}€" for laptop in computer])
                    return resp
        else:
            resp = {"message": "Sorry, I could not find any laptops."}
            return resp

    if any(keyword in tokens for keyword in ['storage', 'memory']):
        num = searchNum(tokens)
        brand = searchBrand(tokens)
        computer = highStorage(Laptop.laptops, int(num[0]), brand)
        if brand:
            if num[1] == False:
                resp = {"message": f"The {computer[0].model} is their computer with the most memory, it has a price of {computer[0].price}€ and a memory of {int(computer[0].storage)}GB."}
                return resp
            else:
                resp = {"message": f"The laptops in the market with the most memory are:"}
                resp["message"] += " ".join([f"{int(laptop.storage)}GB -> {laptop.model} from {laptop.manufacture} priced at {laptop.price}€" for laptop in computer])
                return resp
        else:
            if num[1] == False:
                resp = {"message": f"The {computer[0].model} is the computer with the most memory in the market nowadays, it's from the brand {computer[0].manufacture}, has a price of {computer[0].price}€ and a storage of {int(computer[0].storage)}GB."}
                return resp
            else:
                resp = {"message": f"The laptops in the market with the most memory are:"}
                resp["message"] += " ".join([f"{int(laptop.storage)}GB -> {laptop.model} from {laptop.manufacture} priced at {laptop.price}€" for laptop in computer])
                return resp

    if 'gaming' in tokens:
        computer = gaming(Laptop.laptops)
        resp = {"message": f"The best computer we have found for gaming is the {computer[0].model} with {computer[0].ram}GB of RAM and {computer[0].storage}GB of storage."}
        return resp

    resp = {"message": "No specific recommendation found based on the given context."}
    return resp
