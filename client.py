import requests
from termcolor import colored

BASE_LINK_GET_DATA = 'https://api.kanye.rest/'
BASE_LINK_POST_DATA = 'https://sentim-api.herokuapp.com/api/v1/'
MAX_USER_DEFINE_NUMBER = 20
MIN_USER_DEFINE_NUMBER = 5


# Method for connecting with api and get Kanye's random quotes.
def get_data(base_link):
    try:
        response = requests.get(base_link)
        parse_to_json = response.json()
        data = parse_to_json['quote']
        return data

    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)


# Method for connecting with sentim-api and post Kanye's quotes for analysis and define polarity.
def post_quotes(data):
    try:
        request = requests.post(BASE_LINK_POST_DATA, json=data)
        answer = request.json()
        return answer

    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)


# Method for getting range of random Kanye's quotes
def user_input():
    try:
        user_choice = int(input("Please enter the number of random Kanye's quotes, "
                                f"number must be between {MIN_USER_DEFINE_NUMBER} "
                                f"and {MAX_USER_DEFINE_NUMBER} :) \n"))
    except ValueError:
        print("Please enter only numbers :)\n")
        return user_input()
    else:
        if MIN_USER_DEFINE_NUMBER <= user_choice <= MAX_USER_DEFINE_NUMBER:
            return user_choice
        else:
            print(f"Please enter only numbers between {MIN_USER_DEFINE_NUMBER} and {MAX_USER_DEFINE_NUMBER} :)\n")
            return user_input()


# Method pulls quotes into one list and prepares for validation by sentim-api.
def pulled_quotes():
    quote = set()
    int_range = user_input()

    while len(quote) != int_range:
        quote.add(get_data(BASE_LINK_GET_DATA))

    return quote


# Method post quotes to sentim-api, count all positive, negative and neutral quotes.
# Method shows user all quotes with polarity. In the end the method shows the most extreme quote.
# If extreme quote is red it means that quote is extremely negative, but if quote is green it means extremely positive.
# When in extreme quote max or min polarity = [0.0] it means that in random quotes took from users range dont
# exist positive or negative quotes. 
def count_polarities():
    quotes = pulled_quotes()
    quotes_polarities = []
    positive, negative, neutral = [], [], []

    print("**The first number is a polarity of quote, then are quotes**")

    for quote in quotes:
        post = post_quotes({"text": quote})
        quotes_polarities.append([post["result"]["polarity"], quote])

    for x in quotes_polarities:
        if x[0] > 0.0:
            positive.append(x)
        if x[0] < 0.0:
            negative.append(x)
        if x[0] == 0.0:
            neutral.append(x)

    print("\nThe Number of positive quotes is: ", len(positive))
    print("All positive quotes Kanye: ")
    for x in positive:
        print(f"Polarity: [{x[0]}]", f"Quote: '{x[1]}'")
    print("\nThe Number of negative quotes is: ", len(negative))
    print("All negative quotes Kanye: ")
    for x in negative:
        print(f"Polarity: [{x[0]}]", f"Quote: '{x[1]}'")
    print("\nThe Number of neutral quotes is: ", len(neutral))
    print("All neutral quotes Kanye: ")
    for x in neutral:
        print(f"Polarity: [{x[0]}]", f"Quote: '{x[1]}'")

    print("-------------------------------------")

    polarity_max_value = max(quotes_polarities)
    polarity_min_value = min(quotes_polarities)

    print("The quote with max polarity", f"[{polarity_max_value[0]}] Quote: '{polarity_max_value[1]}'")
    print("The quote with min polarity", f"[{polarity_min_value[0]}] Quote: '{polarity_min_value[1]}'")

    print("-------------------------------------")

    # Define most extreme quote
    if polarity_max_value[0] > abs(polarity_min_value[0]):
        print(colored(f"Most extreme Kanye's quote with polarity [{polarity_max_value[0]}] is: "
                      f"'{polarity_max_value[1]}'", 'green'))
    else:
        print(colored(f"Most extreme Kanye's quote with polarity [{polarity_min_value[0]}] is: "
                      f"'{polarity_min_value[1]}'", 'red'))


if __name__ == '__main__':
    count_polarities()
