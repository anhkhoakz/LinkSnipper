from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import qrcode
import pathlib
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


def read_text_file(filename):
    with open(filename, "r") as f:
        content = f.read()
    return content


def generate_qr_code(args):
    content, index, foldername = args
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(content)
    qr.make(fit=True)
    filename = f"QR_{index}.png"
    save_qr_code(qr, filename, foldername)


def save_qr_code(qr, filename, foldername):
    path = pathlib.Path(foldername)
    path.mkdir(parents=True, exist_ok=True)
    filepath = path.joinpath(filename)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filepath)
    print(f"{filepath} generated successfully!")


def generate_qr_codes(content, foldername="QR_codes"):
    pool = multiprocessing.Pool()
    args = [(line, i+1, foldername)
            for i, line in enumerate(content.splitlines())]
    pool.imap(generate_qr_code, args)
    pool.close()
    pool.join()


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
