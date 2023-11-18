# LinkSnipper: URL Shortener and QR Code Generator

LinkSnipper is a Python script designed to simplify the process of generating shortened URLs using a URL shortener API and creating QR codes for those URLs. This tool streamlines the task of managing and sharing links, making it ideal for various applications.

## Features

- Converts a list of URLs from a file into shortened URLs using a URL shortener API.
- Saves the shortened URLs to a file and displays them in the console.
- Generates QR codes for each shortened URL, stored in a separate folder.

## Requirements

Ensure your system meets the following prerequisites:

- Python 3.5 or higher
- The `requests` library
- The `qrcode` library
- The `Pillow` library

## Installation

1. Clone this repository or download the script to your local machine.

2. Install the required packages by running the following command in your terminal or command prompt:

```sh
python3 ./setup.py
```

## Usage

1. Create a file named `input.txt` and list the URLs you wish to shorten, each on a new line.

```sh
touch input.txt
```

2. Execute the script by running the following command in your terminal or command prompt:

```sh
python ./main.py
```

3. The script will process the URLs, generate shortened versions, and save them to a file named `shorted_urls.txt`. The shortened URLs will also be displayed in the console.

4. QR codes for each shortened URL will be generated and stored in a folder named `QR_codes`.

## Contributing

We welcome your contributions! If you encounter issues or have suggestions for improvements, please feel free to open an issue or submit a pull request on our [GitHub repository](https://github.com/anhkhoakz/linksnipper). Please follow [Contributing direction](./CONTRIBUTING.md)

## Code of Conduct

To ensure a welcoming and respectful environment, we follow a [Code of Conduct](./CODE_OF_CONDUCT.md) for all interactions within the LinkSnipper community.

## License

This project is licensed under the terms of the [MIT License](./LICENSE). For more details, refer to the [LICENSE](./LICENSE) file.

## Sponsors
[![1Password](/imgs/1Password.svg)](https://1password.com/)

[![Tuta](/imgs/tuta.svg)](https://tuta.com/)

[![Netlify](/imgs/netlify.png)](https://www.netlify.com/)
