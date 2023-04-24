import multiprocessing
import qrcode
import pathlib


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
