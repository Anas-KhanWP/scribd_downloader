import re
from bs4 import BeautifulSoup

# Define the path to the .js file
js_file_path = "new.js"

# Read the contents of the .js file
with open(js_file_path, "r", encoding='utf-8') as file:
    js_content = file.read()

# Use a regular expression to find HTML snippets within the JavaScript code
html_snippets = re.findall(r'<[^>]+>', js_content, re.DOTALL)

# Join the found snippets into a single HTML content string
html_content = ''.join(html_snippets)

# Print the extracted HTML content
print("Extracted HTML content:")
print(html_content)

# Optionally, parse the extracted HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Print the prettified HTML content
print("Prettified HTML content:")
print(soup.prettify())

# Save the extracted HTML content to a file
with open("extracted_html.html", "w", encoding='utf-8') as file:
    file.write(soup.prettify())

print("Extracted HTML content saved to extracted_html.html")
