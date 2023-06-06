from qrcode import QRCode
from requests import get
from requests import RequestException
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from re import compile

# Cache for frequently accessed URLs
url_cache = {}


def shorten_url(url):
    if url in url_cache:
        return url_cache[url]

    try:
        response = get(
            "http://is.gd/create.php", params={"format": "simple", "url": url}
        )
        if response.status_code == 200:
            short_url = response.text
            url_cache[url] = short_url
            return short_url
    except RequestException:
        pass

    return None


def read_file(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f]


def write_file(lines, file_path):
    with open(file_path, "w") as f:
        f.write("\n".join(lines))


def generate_qr_code(content, index, foldername):
    qr = QRCode(version=1, box_size=10, border=5)
    qr.add_data(content)
    qr.make(fit=True)
    filename = f"QR_{index}.png"
    path = Path(foldername)
    path.mkdir(parents=True, exist_ok=True)
    filepath = path.joinpath(filename)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filepath)
    print(f"{filepath} generated successfully!")


def process_url(url):
    url_pattern = compile(
        r"^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-zA-Z0-9]+([-.]{1}[a-zA-Z0-9]+)*\.[a-zA-Z]{2,5}(:[0-9]{1,5})?(\/.*)?$"
    )
    if not url_pattern.match(url):
        print(f"Invalid URL: {url}")
        return None

    short_url = shorten_url(url)
    if short_url:
        return short_url


def main():
    input_file_path = "input.txt"
    shortened_output_file_path = "shortened_urls.txt"
    qr_foldername = "QR_codes"
    urls = read_file(input_file_path)

    # Shorten URLs
    with ThreadPoolExecutor(max_workers=50) as executor:
        shortened_urls = list(executor.map(process_url, urls))
    shortened_urls = [url for url in shortened_urls if url is not None]

    # Write shortened URLs to file
    write_file(shortened_urls, shortened_output_file_path)
    print(f"Shortened URLs written to {shortened_output_file_path}")
    print("Shortened URLs:")
    print("\n".join(shortened_urls))

    # Generate QR codes
    with ThreadPoolExecutor(max_workers=50) as executor:
        for i, url in enumerate(shortened_urls):
            executor.submit(generate_qr_code, url, i + 1, qr_foldername)


if __name__ == "__main__":
    main()
