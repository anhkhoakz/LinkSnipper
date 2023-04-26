import subprocess


def has_pip() -> bool:
    """
    Checks if pip is installed in the system.

    Returns:
        bool: True if pip is installed, False otherwise.
    """
    try:
        result = subprocess.run(
            ['pip', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def check_and_install_dependency(dependency: str) -> None:
    """
    Checks if a given dependency is installed and installs it if not.

    Args:
        dependency (str): The name of the dependency to check and install.
    """
    try:
        subprocess.check_output(['pip', 'show', dependency])
    except subprocess.CalledProcessError:
        subprocess.call(['pip', 'install', dependency])


def install_dependencies() -> None:
    """
    Installs the required dependencies for the script.
    """
    if not has_pip():
        print('pip is not installed')
        return

    check_and_install_dependency('requests')
    check_and_install_dependency('qrcode')
    check_and_install_dependency('Pillow')


if __name__ == '__main__':
    install_dependencies()
