import nltk
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer, SnowballStemmer
from nltk.corpus import stopwords

import pandas as pd
import laptop as Laptop

# downloads
nltk.download('punkt')
nltk.download('stopwords')
# load csv file
dataset = pd.read_csv("https://raw.githubusercontent.com/37Degrees/DataSets/master/laptops.csv", encoding="ISO-8859-1")
# create a list of Laptop objects
Laptop.create_list_of_laptops(dataset)


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
    i = 0
    filter_brand = []
    for x in laptops:
        if x.manufacture.lower() == brand:
            filter_brand.append(laptops[i])
        i += 1
    return filter_brand


def highPrice(laptops, n, brand):
    res = []

    if brand == "":
        highest_sorted = sorted(laptops, key=lambda x: x.price, reverse=True)
    else:
        filter_brand = listBrandLaptops(laptops, brand)
        highest_sorted = sorted(filter_brand, key=lambda x: x.price, reverse=True)

    for i in range(0, min(n, len(highest_sorted))):
        res.append(highest_sorted[i])
    return res


def lowPrice(laptops, n, brand):
    res = []

    if brand == "":
        lowest_sorted = sorted(laptops, key=lambda l: l.price, reverse=False)
    else:
        filter_brand = listBrandLaptops(laptops, brand)
        lowest_sorted = sorted(filter_brand, key=lambda l: l.price, reverse=False)

    for i in range(0, min(n, len(lowest_sorted))):
        res.append(lowest_sorted[i])
    return res


def lightWeight(laptops, brand):
    if brand == "":
        computer = sorted(laptops, key=lambda l: l.weight, reverse=False)
    else:
        filter_brand = listBrandLaptops(laptops, brand)
        computer = sorted(filter_brand, key=lambda l: l.weight, reverse=False)
    return computer[0]


def ramCapacity(laptops, n, brand):
    res = []

    if brand == "":
        highest_ram = sorted(laptops, key=lambda x: x.ram, reverse=True)
    else:
        filter_brand = listBrandLaptops(laptops, brand)
        highest_ram = sorted(filter_brand, key=lambda x: x.ram, reverse=True)

    for i in range(0, min(n, len(highest_ram))):
        res.append(highest_ram[i])
    return res


def highStorage(laptops, n, brand):
    res = []

    if brand == "":
        highest_storage = sorted(laptops, key=lambda x: x.storage, reverse=True)
    else:
        filter_brand = listBrandLaptops(laptops, brand)
        highest_storage = sorted(filter_brand, key=lambda x: x.storage, reverse=True)

    for i in range(0, n):
        res.append(highest_storage[i])
    return res


def gaming(laptops):
    res = []
    result = []

    for l in laptops:
        if 'Gaming' in l.category:
            res.append(l)

    highest_ram = sorted(res, key=lambda x: x.ram, reverse=True)

    for i in range(0, min(1, len(highest_ram))):
        result.append(highest_ram[i])
    return result


# Search in tokens
def searchBrand(tokens):
    i = 0
    for x in tokens:
        if x == "brand":
            return tokens[i - 1]
        i += 1
    return ""


def searchNum(tokens):
    i = 0
    for x in tokens:
        if x.isnumeric():
            return [x, True]
    return ["1", False]


def user_input(message):
    tokens = filterStopWords(getTokens(message), stopwords.words('english'))
    # Filter weight
    if FILTER_LIGHT in tokens:
        if "brand" in tokens:
            brand = searchBrand(tokens)
            computer = lightWeight(Laptop.laptops, brand)

            return computer.manufacture + " has the " + computer.model + ", it's their lightest computer and weights " + computer.weight + "kg"
        else:
            computer = lightWeight(Laptop.laptops, "")
            return "The " + computer.model + " is the lightest computer on the market, it's made by " + computer.manufacture + " and weights " + computer.weight + "kg"

    # Filter price (cheapest)
    if FILTER_CHEAP in tokens or FILTER_CHEAP_PLUS in tokens:
        num = searchNum(tokens)
        brand = searchBrand(tokens)
        computer = lowPrice(Laptop.laptops, int(num[0]), brand)

        if "brand" in tokens:
            if num[1] == False:
                return "The " + computer[0].model + " is their cheapest computer and has a price of " + str(
                    computer[0].price) + "€"
            else:
                resp = {"messages": [], "message": "The " + num[0] + " cheapest laptops in the market are:\n"}
                i = 0
                for x in computer:
                    resp["messages"].append(
                        str(computer[i].price) + "€ -> " + computer[i].model + " from " + computer[i].manufacture)
                    i += 1
                return resp
        else:
            if num[1] == False:
                return "The " + computer[
                    0].model + " is the cheapest computer in the market nowdays, it is from the brand " + computer[
                    0].manufacture + " and has a price of " + str(computer[0].price) + "€"
            else:
                resp = {"messages": [], "message": "The cheapest " + num[0] + " laptops in the market are:\n"}

                i = 0
                for x in computer:
                    resp["messages"].append(computer[i].model + " from " + computer[i].manufacture + " -> " + str(
                        computer[i].price) + " €")
                    i += 1
                return resp

    # Filter price (expensive)
    if FILTER_EXPENSIVE in tokens:
        num = searchNum(tokens)
        brand = searchBrand(tokens)
        computer = highPrice(Laptop.laptops, int(num[0]), brand)

        if "brand" in tokens:
            if num[1] == False:
                return "The " + computer[0].model + " is their most expensive computer and has a price of " + str(
                    computer[0].price) + "€"
            else:
                resp = {"messages": [], "message": "The " + num[0] + " most expensive laptops in the market are:\n"}
                i = 0
                for x in computer:
                    resp["messages"].append(str(computer[i].price) + "€ -> " + computer[i].model + " from " + computer[
                        i].manufacture)
                    i += 1
                return resp
        else:
            if num[1] == False:
                return "The " + computer[
                    0].model + " is the most expensive computer in the market nowdays, it is from the brand " + \
                    computer[
                        0].manufacture + " and has a price of " + str(computer[0].price) + "€"
            else:
                resp = {"messages": [], "message": "The " + num[0] + " most expensive laptops in the market are:\n"}
                i = 0
                for x in computer:
                    resp["messages"].append(str(computer[i].price) + " € -> " + computer[i].model + " from " + computer[
                            i].manufacture)
                    i += 1
                return resp

    # Filter RAM
    if FILTER_RAM in tokens or FILTER_RAM_FAST in tokens or FILTER_RAM_FAST_PLUS in tokens:
        num = searchNum(tokens)
        brand = searchBrand(tokens)
        computer = ramCapacity(Laptop.laptops, int(num[0]), brand)

        if len(computer) > 0:
            if "brand" in tokens:
                if num[1] == False:
                    return "The " + computer[0].model + " it's their fastest computer, it has a price of " + str(
                        computer[0].price) + "€ and a speed of " + str(int(computer[0].ram)) + "GB"
                else:
                    resp = {"messages": [], "message": "The " + num[0] + " fastest laptops in the market are:\n"}
                    i = 0
                    for x in computer:
                        resp["messages"].append(str(int(computer[i].ram)) + " GB -> " + computer[i].model + " from " + computer[
                            i].manufacture + " priced in " + str(computer[i].price))
                        i += 1
                    return resp
            else:
                if num[1] == False:
                    return "The " + computer[
                        0].model + " is the fastest computer in the market nowadays, it's from the brand " + computer[
                        0].manufacture + ", has a price of " + str(computer[0].price) + "€ and a speed of " + str(
                        int(computer[0].ram)) + "GB"
                else:
                    resp = {"messages": [], "message": "The " + num[0] + " fastest laptops in the market are:\n"}
                    i = 0
                    for x in computer:
                        resp["messages"].append(str(int(computer[i].ram)) + " GB -> " + computer[i].model + " from " + computer[
                            i].manufacture + " priced in " + str(computer[i].price))
                        i += 1
        else:
            return "Sorry, I could not find any laptops"

    # Filter memory
    if FILTER_STORAGE in tokens or FILTER_MEMORY in tokens:
        num = searchNum(tokens)
        brand = searchBrand(tokens)
        computer = highStorage(Laptop.laptops, int(num[0]), brand)

        if "brand" in tokens:
            if num[1] == False:
                return "The " + computer[
                    0].model + " it's their computer with the most memory, it has a price of " + str(
                    computer[0].price) + "€ and a memory of " + str(int(computer[0].storage)) + "GB"
            else:
                resp = {"messages": [], "message": "The " + num[0] + " are the laptops in the market with the most memory:\n"}
                i = 0
                for x in computer:
                    resp["messages"].append(str(int(computer[i].storage)) + " GB -> " + computer[i].model + " from " + computer[
                        i].manufacture + " priced in " + str(computer[i].price) + "€")
                    i += 1
                return resp
        else:
            if num[1] == False:
                return "The " + computer[
                    0].model + " is the computer with the most memory in the market nowdays, it's from the brand " + \
                    computer[0].manufacture + ", has a price of " + str(
                        computer[0].price) + "€ and a storage of " + str(
                        int(computer[0].storage)) + "GB"
            else:
                resp = {"messages": [], "message": "The " + num[0] + " are the laptops in the market with the most memory:\n"}
                i = 0
                for x in computer:
                    resp["messages"].append(str(int(computer[i].storage)) + " GB -> " + computer[i].model + " from " + computer[
                        i].manufacture + " priced in " + str(computer[i].price) + "€")
                    i += 1
                return resp

    # Filter type gaming
    if FILTER_TYPE in tokens:
        num = searchNum(tokens)
        brand = searchBrand(tokens)
        computer = gaming(Laptop.laptops)

        return "The best computer we have found for gaming is the " + computer[0].model + " with " + str(
            computer[0].ram) + "GB of ram memory and " + str(computer[0].storage) + " GB of storage :)"
