import requests


weatherstack_key = '42f2c4f28194060340e97220c64eb8af'

def get_summer_data (city_str):

    # Prints the data of whatever city input into the function
    url = f"https://api.weatherstack.com/current?access_key={weatherstack_key}"
    query = {"query":city_str, "historical_date_start":"2023-06-01", "historical_date_end":"2023-07-31"}
    summer = requests.get(url, params=query)

    print(summer.json())

def get_winter_data(city_str):
    url = f"https://api.weatherstack.com/current?access_key={weatherstack_key}"
    query = {"query":city_str, "historical_date_start":"2023-11-01", "historical_date_end":"2023-12-31"}
    winter = requests.get(url, params=query)

    print(winter.json())

def main():
    summer_info = 
    # print("ANN ARBOR")
    # get_wstack_data('Ann Arbor')

    # print("DETROIT")
    # get_wstack_data('Detroit')

    # print("MARQUETTE")
    # get_wstack_data("Marquette")

    # print("LANSING")
    # get_wstack_data("Lansing")

    # print("GRAND RAPIDS")
    # get_wstack_data("Grand Rapids")

    # print("TRAVERSE CITY")
    # get_wstack_data("Traverse City")

if __name__ == "__main__":
    main()
