from qrcode import QRCode
from requests import get, RequestException
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from re import compile
from typing import List, Optional

URL_SHORTENER_API = "http://is.gd/create.php"
URL_SHORTENER_FORMAT = "simple"
MAX_WORKERS = 50
DEFAULT_INPUT_FILE = "input.txt"
DEFAULT_OUTPUT_FILE = "shortened_urls.txt"
DEFAULT_QR_FOLDER = "QR_codes"

url_cache: dict[str, str] = {}


def shorten_url(original_url: str) -> str:
    """
    Shortens a given URL using the is.gd API.

    Args:
        original_url (str): The URL to be shortened.

    Returns:
        str: The shortened URL or an error message if the request fails.
    """
    if original_url in url_cache:
        return url_cache[original_url]

    try:
        response = get(
            URL_SHORTENER_API,
            params={"format": URL_SHORTENER_FORMAT, "url": original_url},
        )
        if response.status_code == 200:
            short_url = response.text
            url_cache[original_url] = short_url
            return short_url
        return f"Failed to shorten URL: {original_url}"
    except RequestException:
        return f"Failed to shorten URL: {original_url}"


def read_file(file_path: str) -> List[str]:
    """
    Reads lines from a file and returns them as a list of strings.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[str]: List of lines from the file.
    """
    with open(file_path, "r") as file:
        return [line.strip() for line in file]


def write_file(lines: List[str], file_path: str) -> None:
    """
    Writes a list of strings to a file.

    Args:
        lines (List[str]): List of strings to write.
        file_path (str): Path to the output file.
    """
    with open(file_path, "w") as file:
        file.write("\n".join(lines))


def generate_qr_code(content: str, index: int, folder_name: str) -> None:
    """
    Generates a QR code for the given content and saves it as an image.

    Args:
        content (str): The content to encode in the QR code.
        index (int): Index for naming the QR code file.
        folder_name (str): Folder to save the QR code image.
    """
    qr = QRCode(version=1, box_size=10, border=5)
    qr.add_data(content)
    qr.make(fit=True)
    file_name = f"QR_{index}.png"
    folder_path = Path(folder_name)
    folder_path.mkdir(parents=True, exist_ok=True)
    file_path = folder_path.joinpath(file_name)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)
    print(f"{file_path} generated successfully!")


def validate_url(url: str) -> bool:
    """
    Validates a URL using a regex pattern.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    url_pattern = compile(
        r"^[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
    )
    return bool(url_pattern.match(url))


def process_url(url: str) -> Optional[str]:
    """
    Processes a URL by validating and shortening it.

    Args:
        url (str): The URL to process.

    Returns:
        Optional[str]: The shortened URL if valid, None otherwise.
    """
    if not validate_url(url):
        print(f"Invalid URL: {url}")
        return None
    return shorten_url(url)


def shorten_urls(urls: List[str]) -> List[str]:
    """
    Shortens a list of URLs concurrently.

    Args:
        urls (List[str]): List of URLs to shorten.

    Returns:
        List[str]: List of shortened URLs.
    """
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        shortened_urls = list(executor.map(process_url, urls))
    return [url for url in shortened_urls if url is not None]


def generate_qr_codes(urls: List[str], folder_name: str) -> None:
    """
    Generates QR codes for a list of URLs concurrently.

    Args:
        urls (List[str]): List of URLs to generate QR codes for.
        folder_name (str): Folder to save the QR code images.
    """
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for index, url in enumerate(urls):
            executor.submit(generate_qr_code, url, index + 1, folder_name)


def main() -> None:
    """
    Main function to read URLs, shorten them, write to a file, and generate QR codes.
    """
    input_file_path = DEFAULT_INPUT_FILE
    output_file_path = DEFAULT_OUTPUT_FILE
    qr_folder_name = DEFAULT_QR_FOLDER

    urls = read_file(input_file_path)
    shortened_urls = shorten_urls(urls)
    write_file(shortened_urls, output_file_path)
    print(f"Shortened URLs written to {output_file_path}")
    print("Shortened URLs:")
    print("\n".join(shortened_urls))
    generate_qr_codes(shortened_urls, qr_folder_name)


if __name__ == "__main__":
    main()
