"""
This script downloads images from Pixabay API and saves them to the local directory.
"""
import os
import requests
from tqdm import tqdm
import time


PIXABAY_API_KEY = "48852727-e5821f070038a88779fad911e"
BASE_URL = "https://pixabay.com/api/"
CATEGORIES = ['nature', 'human', 'animal', 'car', 'food']  # type of images to download
DOWNLOAD_DIR = "photo-gallery"
TOTAL_IMAGES_PER_CATEGORY = 500  # number of images to download per category
PER_PAGE = 200  # number of images per page
MAX_REQUESTS_PER_MINUTE = 100  # API limit: 100 requests per minute

# ensure the download directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def fetch_images(query, page):
    """
    param: 
        query: search query
        page: page number
    return: list of image objects
    exception: None
    description: Fetch images from Pixabay API
    """
    params = {
        "key": PIXABAY_API_KEY,
        "q": query,
        "image_type": "photo",
        "per_page": PER_PAGE,
        "page": page
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 429:
        print("API 速率限制達到，暫停 60 秒...")
        time.sleep(60)
        return fetch_images(query, page)  # resend request after waiting
    
    response.raise_for_status()  
    return response.json().get("hits", [])

def download_image(url, save_path):
    """
    param: 
        url: image URL
        save_path: path to save the image
    return: None
    exception: None
    description: Download image from URL 
    """
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

def download_images_for_category(category):
    """
    param: category: image category
    return: None
    exception: None
    description: Download images for a given category
    """
    downloaded = 0
    page = 1
    request_count = 0
    category_dir = os.path.join(DOWNLOAD_DIR, category)
    os.makedirs(category_dir, exist_ok=True)
    
    print(f"開始下載 {category} 類別的 {TOTAL_IMAGES_PER_CATEGORY} 張圖片...")
    
    while downloaded < TOTAL_IMAGES_PER_CATEGORY:
        images = fetch_images(category, page)
        if not images:
            print(f"{category} 類別未取得更多圖片，下載結束。")
            break

        for img in images:
            if downloaded >= TOTAL_IMAGES_PER_CATEGORY:
                break

            img_url = img.get("largeImageURL") or img.get("webformatURL")
            if not img_url:
                continue 

            img_id = img["id"]
            img_extension = img_url.split(".")[-1]
            img_path = os.path.join(category_dir, f"{img_id}.{img_extension}")

            if os.path.exists(img_path):
                continue # skip if image already exists

            try:
                download_image(img_url, img_path)
                downloaded += 1
                request_count += 1
                tqdm.write(f"[{downloaded}/{TOTAL_IMAGES_PER_CATEGORY}] {category} 下載完成: {img_path}")
            except Exception as e:
                print(f"下載失敗: {img_url}，錯誤: {e}")

            if request_count >= MAX_REQUESTS_PER_MINUTE:
                print("已達 API 速率限制，暫停 60 秒...")
                time.sleep(60)
                request_count = 0

        page += 1  # move to the next page
    
    print(f"{category} 類別所有圖片下載完成！")

def main():
    for category in CATEGORIES:
        download_images_for_category(category)
    print("所有類別的圖片下載完成！")

if __name__ == "__main__":
    main()
