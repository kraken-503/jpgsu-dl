import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def html_source(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise RuntimeError(f"Requested site {url} is down")


def scraper(html_content, base_url):
    soup = BeautifulSoup(html_content, "html.parser")
    images = soup.find_all("img")
    img_urls = [urljoin(base_url, img.get("src")) for img in images if img.get("src")]
    return img_urls


def downloader(img_urls, folder="./downloads/"):
    os.makedirs(folder, exist_ok=True)
    for i, url in enumerate(tqdm(img_urls, desc="Downloading...")):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                ext = os.path.splitext(url)[1] or ".jpg"
                filename = os.path.join(folder, f"image_{i}{ext}")
                with open(filename, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
        except Exception as e:
            print(f"Failed to download {url}: {e}")


def main():
    user_url = input("Enter a valid URL : ")
    html = html_source(user_url)
    image_urls = scraper(html, user_url)
    print(f"Found {len(image_urls)} images.")
    downloader(image_urls)
    print(f"Downloaded {len(image_urls)} images.")


if __name__ == "__main__":
    main()
