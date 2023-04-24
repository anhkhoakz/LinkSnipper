from concurrent.futures import ThreadPoolExecutor
from utils.url_shortener import shorten_url, read_urls_from_file, write_shortened_urls_to_file, print_shortened_urls
from utils.qr_code_generator import generate_qr_codes


def process_url(url):
    short_url = shorten_url(url)
    if short_url:
        return short_url


def main():
    input_file_path = "input.txt"
    shortened_output_file_path = "shorted_urls.txt"
    shortened_urls = []
    urls = read_urls_from_file(input_file_path)
    with ThreadPoolExecutor(max_workers=50) as executor:
        shortened_urls = list(executor.map(process_url, urls))
    shortened_urls = [url for url in shortened_urls if url is not None]
    write_shortened_urls_to_file(shortened_urls, shortened_output_file_path)
    print(f"Shortened URLs written to {shortened_output_file_path}")
    print_shortened_urls(shortened_urls)
    generate_qr_codes("\n".join(shortened_urls))


if __name__ == "__main__":
    main()
