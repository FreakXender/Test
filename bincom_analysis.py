import re
import random
import psycopg2
import statistics
from collections import Counter
from bs4 import BeautifulSoup


# Load HTML file
def load_html(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


# Extract colors from the table
def extract_colors(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table_rows = soup.find_all("tr")[1:]  # Skip table header
    colors = []
    for row in table_rows:
        cols = row.find_all("td")
        color_list = cols[1].text.upper().split(", ")
        colors.extend(color_list)

    # Correct possible typos
    corrections = {"BLEW": "BLUE", "ARSH": "ASH"}
    colors = [corrections.get(color, color) for color in colors]
    return colors


# Analyze colors
def analyze_colors(colors):
    counter = Counter(colors)
    mean_color = max(counter, key=counter.get)  # Most frequent color
    most_worn = mean_color

    sorted_colors = sorted(colors)  # Sort alphabetically
    median_index = len(sorted_colors) // 2
    median_color = sorted_colors[median_index] if len(sorted_colors) % 2 == 1 else sorted_colors[median_index - 1]

    variance = statistics.variance(counter.values()) if len(counter) > 1 else 0
    probability_red = counter.get('RED', 0) / len(colors)

    return mean_color, most_worn, median_color, variance, probability_red


# Store data in PostgreSQL
def store_in_db(color_counts):
    conn = psycopg2.connect(dbname='testdb', user='postgres', password='', host='localhost')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS color_frequency (color TEXT PRIMARY KEY, count INT)")
    for color, count in color_counts.items():
        cur.execute(
            "INSERT INTO color_frequency (color, count) VALUES (%s, %s) ON CONFLICT (color) DO UPDATE SET count = EXCLUDED.count",
            (color, count))
    conn.commit()
    cur.close()
    conn.close()


# Recursive search function
def recursive_search(arr, target, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    if left > right:
        return -1
    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return recursive_search(arr, target, mid + 1, right)
    else:
        return recursive_search(arr, target, left, mid - 1)


# Generate a random 4-digit binary number and convert to decimal
def generate_binary_and_convert():
    binary_number = ''.join(random.choice('01') for _ in range(4))
    decimal_value = int(binary_number, 2)
    return binary_number, decimal_value


# Sum of first 50 Fibonacci numbers
def sum_fibonacci(n=50):
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total


# Example usage
if __name__ == "__main__":
    filename = "python_class_question.html"
    html_content = load_html(filename)
    colors = extract_colors(html_content)

    mean_color, most_worn, median_color, variance, probability_red = analyze_colors(colors)
    store_in_db(Counter(colors))

    print("Mean Color:", mean_color)
    print("Most Worn Color:", most_worn)
    print("Median Color:", median_color)
    print("Variance:", variance)
    print("Probability of Red:", probability_red)

    binary_number, decimal_value = generate_binary_and_convert()
    print("Generated Binary:", binary_number, "Decimal Equivalent:", decimal_value)

    print("Sum of first 50 Fibonacci numbers:", sum_fibonacci())
