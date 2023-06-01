# Laptopinator


## Description

The Laptopinator is a laptop recommendation chatbot developed using Python, JavaScript, HTML, and CSS. The project is designed to provide the user with laptop recommendations based on their input. The chatbot uses Natural Language Processing (NLP) techniques to understand the user's input and then generate suitable laptop recommendations accordingly.

## Technologies Used

- Python
- JavaScript
- HTML
- CSS

## Implementation

The implementation of the chatbot involves several steps:

1. Importing necessary libraries and packages like nltk, pandas, and heapq.
2. Loading a laptop dataset from a CSV file available at a specified URL.
3. Creating a list of Laptop objects from the loaded dataset.
4. Initializing a conversation history to keep track of the user's inputs and the chatbot's recommendations.
5. Generating contextual recommendations based on the user's input and the previous recommendations provided by the chatbot.

The chatbot tokenizes user input and previous recommendations, filters out stop words, and then combines the current user input with the previous recommendations to create a context for the recommendation algorithm.

The chatbot uses various constants to filter the recommendations based on parameters such as 'best', 'cheap', 'expensive', 'ram', 'fast', 'storage', 'screen', 'big', 'medium', 'light', 'brand', and 'gaming'.

## Laptop Class

The chatbot uses a Laptop class to represent individual laptops from the dataset. The Laptop class contains properties such as manufacture, model, category, price, processor, ram, screen size, storage, graphics, OS, and weight.

## Installation

1. Clone the repository
2. Install the required packages using the following command:

```bash
pip install -r requirements.txt
```
3. Run the following command to start the chatbot:

```bash
flask --app main run --host=0.0.0.0 --debug 
```