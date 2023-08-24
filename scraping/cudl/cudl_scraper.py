import requests
import os
import json
import concurrent.futures as cf
import logging

def setup_logger():
    """
    Sets up and returns a logger with a specific format.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger

def get_all_items():
    logger = setup_logger()
    site_map_url = "https://cudl.lib.cam.ac.uk/sitemap.xml"
    logger.info("Getting sitemap")
    response = requests.get(site_map_url)
    if response.status_code == 200:
        urls = response.text.split("<loc>")[1:]
        urls = [url.split("</loc>")[0] for url in urls]
        urls = [url.strip() for url in urls]
    else:
        logger.error("Could not get sitemap")
        raise requests.exceptions.HTTPError("Could not get sitemap")

    ids = [url.split("/")[-1] for url in urls]

    return ids

def get_item_json_data(item_id):
    logger = setup_logger()
    base_url = f"https://cudl.lib.cam.ac.uk/view/{item_id}.json"
    logger.info(f"Getting item json data for {item_id}")
    response = requests.get(base_url)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        logger.error(f"Could not get item json data for {item_id}")
        raise requests.exceptions.HTTPError("Could not get item json data")

def get_item_images_urls(item_id):
    base_url = "https://images.lib.cam.ac.uk/"
    data = get_item_json_data(item_id)
    pages = data["pages"]
    urls = [base_url + page["downloadImageURL"] for page in pages]
    return urls

def save_image(url, save_dir):
    logger = setup_logger()
    response = requests.get(url)
    if response.status_code == 200:
        image = response.content
        filename = url.split("/")[-1]
        filepath = os.path.join(save_dir, filename)
        with open(filepath, "wb") as f:
            f.write(image)
    else:
        logger.error(f"Could not get image from {url}")
        raise requests.exceptions.HTTPError("Could not get image")

def main():
    logger = setup_logger()
    item_ids = get_all_items()
    image_urls = []
    with cf.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(get_item_images_urls, item_id): item_id for item_id in item_ids}
        for future in cf.as_completed(future_to_url):
            item_id = future_to_url[future]
            try:
                data = future.result()
                image_urls.extend(data)
            except Exception as exc:
                logger.error(f"{item_id} generated an exception: {exc}")

    save_dir = "/scratch/gpfs/RUSTOW/cudl_images"
    os.makedirs(save_dir, exist_ok=True)
    with cf.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda x: save_image(x, save_dir), image_urls)

if __name__ == "__main__":
    main()

