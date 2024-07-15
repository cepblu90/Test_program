import requests

class CountryInfo:
    def __init__(self, api_url="https://restcountries.com/v3.1/all"):
        self.api_url = api_url

    def fetch_data(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()  # Проверка на успешный запрос
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return []

    def get_all_countries_info(self):
        data = self.fetch_data()
        countries_info = []
        for country in data:
            name = country['name']['common']
            capital = country.get('capital', ['No capital'])[0]
            flag_url = country['flags']['png']
            countries_info.append({
                'name': name,
                'capital': capital,
                'flag_url': flag_url
            })
        return countries_info

    def display_all_countries_info(self):
        countries_info = self.get_all_countries_info()
        header = f"{'Country':<30} {'Capital':<30} {'Flag URL':<50}"
        print(header)
        print("=" * len(header))
        for info in countries_info:
            print(f"{info['name']:<30} {info['capital']:<30} {info['flag_url']:<50}")

if __name__ == "__main__":
    country_info = CountryInfo()
    country_info.display_all_countries_info()
