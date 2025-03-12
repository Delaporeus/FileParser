import os

import requests
import re


def extract_https_link(file_path):
    with open(file_path, "rb") as f:
        data = f.read()

    try:
        decoded_text = data.decode("utf-8", errors="ignore")
    except UnicodeDecodeError:
        print("Error decoding file as UTF-8")
        return None

    # Regex to find HTTPS URLs
    url_pattern = re.compile(r'https://[^\s"<>]*?avif')
    match = url_pattern.search(decoded_text)

    if match:
        return match.group(0)
    else:
        print("No HTTPS link found in the file. " + file_path)
        return None


# Example usage
file_path = "5117d07a0187c5dbf4c4c117a9e2495a0b827483d1d885d3d4ff17975546431a.0"  # Change this to your file path
link = extract_https_link(file_path)
if link:
    print("Extracted HTTPS link:", link)


def download_file(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"File downloaded successfully: {save_path}")
    except requests.RequestException as e:
        print(f"Error downloading file: {e}")


cur_dir = [i for i in os.listdir() if i[-1] == '0' ]
for i in cur_dir:
    link = extract_https_link(i)
    if link:
        download_file(link, str(i) + '.avif')
