import requests

# Cache for frequently accessed URLs
url_cache = {}


def shorten_url(url):
    if url in url_cache:
        return url_cache[url]

    try:
        response = requests.get("http://is.gd/create.php",
                                params={"format": "simple", "url": url})
        if response.status_code == 200:
            short_url = response.text
            url_cache[url] = short_url
            return short_url
    except requests.exceptions.RequestException:
        pass

    return None


def read_urls_from_file(file_path):
    with open(file_path, "r") as f:
        return [url.strip() for url in f]


def write_shortened_urls_to_file(shortened_urls, file_path):
    with open(file_path, "w") as f:
        f.write("\n".join(shortened_urls))


def print_shortened_urls(shortened_urls):
    print("Shortened URLs:")
    print("\n".join(shortened_urls))
