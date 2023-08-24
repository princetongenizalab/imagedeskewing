import requests
import os
import json
import concurrent.futures as cf


def get_all_items():
    """
    Get all the items from the CUDL website. Each item can have multiple images associated
    with it. This function will get the item name for each item and return a list of all
    the items.

    Returns
    -------
    list of str
    """
    site_map_url = "https://cudl.lib.cam.ac.uk/sitemap.xml"
    response = requests.get(site_map_url)
    if response.status_code == 200:
        # get all the urls
        urls = response.text.split("<loc>")[1:]
        urls = [url.split("</loc>")[0] for url in urls]
        urls = [url.strip() for url in urls]
    else:
        raise requests.exceptions.HTTPError("Could not get sitemap")

    ids = [url.split("/")[-1] for url in urls]

    return ids


def get_item_json_data(item_id):
    """
    Get the json data for a specific item.

    Parameters
    ----------
    item_id : str
        The id of the item to get the json data for.

    Returns
    -------
    dict
        The json data for the item.
    """
    base_url = f"https://cudl.lib.cam.ac.uk/view/{item_id}.json"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        raise requests.exceptions.HTTPError("Could not get item json data")


def get_item_images_urls(item_id):
    """
    Get the urls for all the images associated with an item.

    Parameters
    ----------
    item_id : str
        The id of the item to get the image urls for.

    Returns
    -------
    list of str
        The urls for all the images associated with the item.
    """
    base_url = "https://images.lib.cam.ac.uk/"
    data = get_item_json_data(item_id)
    pages = data["pages"]
    urls = []
    for page in pages:
        url = base_url + page["downloadImageURL"]
        urls.append(url)

    return urls


def save_image(url, save_dir):
    """
    Save an image to a local directory.

    Parameters
    ----------
    url : str
        The url of the image to save.
    save_dir : str
        The directory to save the image to.
    """
    response = requests.get(url)
    if response.status_code == 200:
        image = response.content
        filename = url.split("/")[-1]
        filepath = os.path.join(save_dir, filename)
        with open(filepath, "wb") as f:
            f.write(image)
    else:
        raise requests.exceptions.HTTPError("Could not get image")


def main():
    """
    Main function for the CUDL scraper. This will get all the images from the CUDL website
    and save them to a local directory.
    """
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
                print(f"{item_id} generated an exception: {exc}")

    print(image_urls)
    save_dir = "/scratch/gpfs/RUSTOW/cudl_images"
    os.makedirs(save_dir, exist_ok=True)
    with cf.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda x: save_image(x, save_dir), image_urls)


if __name__ == "__main__":
    main()
