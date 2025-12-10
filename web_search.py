from serpapi import GoogleSearch
import urllib.parse

def search_google(query, api_key, num_results=5):
    """Search Google using SerpAPI"""
    results = []
    
    try:
        # Setup SerpAPI parameters
        params = {
            "q": query,
            "api_key": api_key,
            "num": num_results,
            "engine": "google"
        }
        
        # Execute the search
        search = GoogleSearch(params)
        result = search.get_dict()
        
        # Extract organic results
        if "organic_results" in result:
            for item in result["organic_results"][:num_results]:
                results.append({
                    'title': item.get('title', 'No title'),
                    'url': item.get('link', ''),
                    'snippet': item.get('snippet', 'No snippet')
                })
        else:
            if "error" in result:
                pass
        
    except Exception as e:
        # Fallback: provide Google Search link
        results.append({
            'title': 'Google Search',
            'url': f'https://www.google.com/search?q={urllib.parse.quote(query)}',
            'snippet': 'Click to search on Google'
        })
    
    return results[:num_results]
