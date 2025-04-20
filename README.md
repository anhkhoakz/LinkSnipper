# 🚀 **LinkSnipper: URL Shortener & QR Code Generator**

> *Easily shorten URLs and generate QR codes with a single Python script!*

---

## ✨ Features

- 🔗 **Batch URL Shortening**: Converts a list of URLs from a file into shortened URLs using a URL shortener API.
- 💾 **Easy Export**: Saves the shortened URLs to a JSON file and displays them in the console.
- 🖼️ **QR Code Generation**: Generates QR codes for each shortened URL, stored in a separate folder.

---

## ⚙️ Requirements

- Python 3.12 or higher
- `requests` library
- `qrcode` library
- `Pillow` library

---

## 📦 Installation

```sh
uv env venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
uv sync
```

---

## 🚦 Usage

1. Create a file named `input.txt` and list the URLs you wish to shorten, each on a new line.
2. Run the script:

   ```sh
   .venv/bin/python main.py
   ```

3. The script will process the URLs, generate shortened versions, and save them to `output.json`. The shortened URLs will also be displayed in the console.
4. QR codes for each shortened URL will be generated and stored in a folder named `QR_codes`.

---

## 🤝 Contributing

We welcome your contributions! If you encounter issues or have suggestions for improvements, please open an issue or submit a pull request on our [GitHub repository](https://github.com/anhkhoakz/linksnipper). Please follow the [Contributing Guidelines](./CONTRIBUTING.md).

---

## 🧑‍💻 Code of Conduct

To ensure a welcoming and respectful environment, we follow a [Code of Conduct](./CODE_OF_CONDUCT.md) for all interactions within the LinkSnipper community.

---

## 📄 License

Licensed under the [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/). See the [LICENSE](./LICENSE.md) file for details.

---

## 💖 Sponsors

<p align="left">
  <a href="https://1password.com/"><img src="https://img.shields.io/badge/1password-white?style=for-the-badge&logo=1password&logoColor=3B66BC" alt="1Password"></a>
  <a href="#"><img src="https://img.shields.io/badge/tuta-white?style=for-the-badge&logo=tuta&logoColor=850122" alt="Tuta"></a>
  <a href="https://www.netlify.com/"><img src="https://img.shields.io/badge/netlify-white?style=for-the-badge&logo=netlify&logoColor=00C7B7" alt="Netlify"></a>
</p>
