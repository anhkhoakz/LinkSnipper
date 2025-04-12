from qrcode import QRCode
from requests import get, RequestException
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from re import compile
from typing import List, Optional
from itertools import islice
import json

URL_SHORTENER_API: str = "https://is.gd/create.php"
URL_SHORTENER_FORMAT: str = "simple"
MAX_WORKERS: int = 50
DEFAULT_INPUT_FILE: str = "input.txt"
DEFAULT_OUTPUT_FILE: str = "shortened_urls.txt"
DEFAULT_QR_FOLDER: str = "QR_codes"

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


def write_json(data: List[dict], file_path: str) -> None:
    """
    Writes a list of dictionaries to a JSON file.

    Args:
        data (List[dict]): List of dictionaries to write.
        file_path (str): Path to the output JSON file.
    """
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


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

    domain: str = content.split("//")[-1].split("/")[0].replace(".", "_")
    file_name: str = f"QR_{domain}.png"

    folder_path: Path = Path(folder_name)
    folder_path.mkdir(parents=True, exist_ok=True)
    file_path: Path = folder_path.joinpath(file_name)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)


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


def batch_iterable(iterable: List[str], batch_size: int) -> List[List[str]]:
    """
    Splits an iterable into batches of a given size.

    Args:
        iterable (List[str]): The iterable to split.
        batch_size (int): The size of each batch.

    Returns:
        List[List[str]]: Batches of the iterable.
    """
    iterator = iter(iterable)
    while batch := list(islice(iterator, batch_size)):
        yield batch


def shorten_urls(urls: List[str]) -> List[tuple[str, str]]:
    """
    Shortens a list of URLs concurrently.

    Args:
        urls (List[str]): List of URLs to shorten.

    Returns:
        List[tuple[str, str]]: List of tuples containing original and shortened URLs.
    """
    results: List[tuple[str, str]] = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url: dict = {
            executor.submit(process_url, url): url for url in urls
        }
        for future in as_completed(future_to_url):
            original_url: str = future_to_url[future]
            shortened_url: Optional[str] = future.result()
            if shortened_url:
                results.append((original_url, shortened_url))
    return results


def generate_qr_codes(urls: List[str], folder_name: str) -> None:
    """
    Generates QR codes for a list of URLs concurrently.

    Args:
        urls (List[str]): List of URLs to generate QR codes for.
        folder_name (str): Folder to save the QR code images.
    """
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(generate_qr_code, url, index + 1, folder_name)
            for index, url in enumerate(urls)
        ]
        for future in as_completed(futures):
            future.result()


def main() -> None:
    """
    Main function to read URLs, shorten them, write to a JSON file, and generate QR codes.
    """
    input_file_path: str = DEFAULT_INPUT_FILE
    output_file_path: str = "output.json"
    qr_folder_name: str = DEFAULT_QR_FOLDER

    urls: List[str] = read_file(input_file_path)
    valid_urls: List[tuple[str, str]] = []

    for batch in batch_iterable(urls, MAX_WORKERS):
        valid_urls.extend(shorten_urls(batch))

    output_data: List[dict[str, str]] = []
    for index, (original_url, shortened_url) in enumerate(valid_urls):
        qr_code_path: str = str(
            Path(qr_folder_name).joinpath(f"QR_{index + 1}.png")
        )
        output_data.append({
            "origin": original_url,
            "shortened": shortened_url,
            "qr_code": qr_code_path,
        })

    write_json(output_data, output_file_path)
    print(f"Shortened URLs written to {output_file_path}")
    generate_qr_codes(
        [shortened for _, shortened in valid_urls], qr_folder_name
    )


if __name__ == "__main__":
    main()
