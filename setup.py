import os
import subprocess

def install_dependencies():
    os.system('pip install requests')
    os.system('pip install qrcode')
    os.system('pip install Pillow')

if __name__ == '__main__':
    install_dependencies()
