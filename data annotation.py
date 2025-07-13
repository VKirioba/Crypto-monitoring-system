import requests
import re

def print_secret_message(url):
    """
    Fetches, parses, and prints a grid of Unicode characters from a Google Doc URL.
    The grid forms a graphic of uppercase letters as a secret message.
    """
    # Step 1: Fetch the document content
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch the document. Check the URL.")
        return
    
    content = response.text
    
    # Step 2: Parse the content using regex to extract x, y, and character
    pattern = re.compile(r'(\d+)\s*\|\s*(.)\s*\|\s*(\d+)')  # Matches "x | char | y"
    matches = pattern.findall(content)
    
    if not matches:
        print("No valid grid data found in the document.")
        return
    
    # Step 3: Determine grid dimensions and initialize the grid
    grid = {}
    max_x, max_y = 0, 0
    
    for x, char, y in matches:
        x, y = int(x), int(y)
        grid[(x, y)] = char
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    
    # Step 4: Print the grid, filling empty spaces with ' '
    for y in range(max_y + 1):
        row = ''
        for x in range(max_x + 1):
            row += grid.get((x, y), ' ')  # Default to space if no character
        print(row)

# Example usage
url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
print_secret_message(url)
