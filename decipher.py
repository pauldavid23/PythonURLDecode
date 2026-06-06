import requests
from bs4 import BeautifulSoup


url = input("Enter URL: ")

def fetch_and_plot_from_pub_url(url):

    print("Fetching data from Google Doc...")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch document. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')
    if not table:
        print("No table found in the document.")
        return

    parsed_data = []

    rows = table.find_all('tr')[1:]

    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 3:
            try:

                x_str = cols[0].get_text(strip=True)
                char = cols[1].get_text(strip=True)
                y_str = cols[2].get_text(strip=True)

                x = int(x_str)
                y = int(y_str)

                if not char:
                    char = ' '

                parsed_data.append((x, char, y))
            except ValueError:
                continue

    if not parsed_data:
        print("No valid coordinate data found in the table.")
        return

    max_x = max(item[0] for item in parsed_data)
    max_y = max(item[2] for item in parsed_data)

    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for x, char, y in parsed_data:
        grid[y][x] = char

    print("\n--- PLOTTED OUTPUT ---\n")
    for y in range(max_y, -1, -1):
        print("".join(grid[y]))


doc_url = url
fetch_and_plot_from_pub_url(doc_url)