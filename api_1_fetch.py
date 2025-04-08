import requests


weatherstack_key = '42f2c4f28194060340e97220c64eb8af'

def get_wstack_data (city):

    # Prints the data of whatever city input into the function
    url = f"https://api.weatherstack.com/current?access_key={weatherstack_key}"
    querystring = {"query" : city}
    response = requests.get(url, params=querystring)

    print(response.json())


def main():
    get_wstack_data('New York')


if __name__ == "__main__":
    main()
