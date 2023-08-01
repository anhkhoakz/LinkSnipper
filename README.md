# LinkSnipper

This project provides a Python script that takes a list of URLs from a file and uses a URL shortener API to generate shortened URLs for each of them. It then writes the shortened URLs to a file, prints them to the console, and generates QR codes for each shortened URL.

## Requirements

To use this project, you need to have the following installed on your machine:

- Python 3.5 or higher

- requests

- qrcode

- Pillow

## Installation

1. Clone this repository or download the script.

2. Install the required packages by running 
```python
python3 ./setup.py
```
 in your terminal or command prompt.

## Usage

1. Create a file called input.txt and enter each URL that you want to shorten on a new line.
```python
touch input.txt
```

2. Run the script by executing python main.py in your terminal or command prompt.
```python
python3 ./main.py
```
or
```python
python ./main.py
```

3. The script will generate a file called shorted_urls.txt with the shortened URLs and print them to the console.

4. The script will also generate a folder called QR_codes with a QR code for each shortened URL.

## Contributing

If you find any issues or have suggestions for improvement, please feel free to open an issue or pull request in the GitHub repository.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more information.