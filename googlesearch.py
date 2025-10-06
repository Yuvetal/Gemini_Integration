import requests

# Replace these with your actual credentials
API_KEY = "AIzaSyCRp2ZBgn-i0tCqg7242jV23EftJuC7R-Y"
CX = "a055bd0eb4fca45a3"  # Your Search Engine ID

def google_search(query, api_key=API_KEY, cx=CX):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "q": query
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return []

    results = response.json()
    output = []

    for item in results.get("items", []):
        output.append({
            "title": item.get("title"),
            "snippet": item.get("snippet"),
            "link": item.get("link")
        })

    return output

# Example usage
if __name__ == "__main__":
    query = input("Enter your search query: ")
    search_results = google_search(query)

    if not search_results:
        print("No results found or an error occurred.")
    else:
        for i, result in enumerate(search_results, start=1):
            print(f"\nResult {i}:")
            print("Title:", result["title"])
            print("Snippet:", result["snippet"])
            print("Link:", result["link"])
