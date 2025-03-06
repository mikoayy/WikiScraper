import requests
from bs4 import BeautifulSoup
from pathlib import Path

def create_folder(path_to_folder):
    path = Path(path_to_folder)
    if not path.is_file():
        path.mkdir(parents=True, exist_ok=True)
    return path


def get_text(response, all_data=False):
    data = []
    if all_data:
        soup = BeautifulSoup(response.text, "lxml")
        title = soup.find("span", class_="mw-page-title-main").text
        return soup.get_text(), title

    soup = BeautifulSoup(response.text, "html.parser")
    specific_div = soup.find("div", class_="mw-content-ltr mw-parser-output")
    title = soup.find("span", class_="mw-page-title-main").text

    for element in specific_div.descendants:
        tag_name = element.name
        if tag_name == "None":
            continue
        elif tag_name == "p":
            is_valid = True
            for parent in element.parents:
                if parent.name == "tbody":
                    is_valid = False
                    break
            if is_valid:
                data.append(element.text)

        elif tag_name == "h1" or tag_name == "h2" or tag_name == "h3":
            data.append(f"-{element.text.upper()}")

        elif tag_name == "li":
            if element.text.startswith("^"):
                data.append(element.text)
            else:
                data.append(f"-{element.text}")
    return " ".join(data), title


def save_txt(data, title, path):
    try:
        with open(f"{path}/{title}.txt", "w", encoding="utf-8") as file:
            file.writelines(f"{element}\n" for element in data)
    except Exception as e:
        print(f"Something went wrong: {e}")


def wiki_scrapper(urls, folder_path=None, return_as_list=True, all_data=False):
    if type(urls) == str:
        urls = [urls]
    articles = []
    if folder_path is None and return_as_list is False:
        raise ValueError("If return_as_list is False, folder_path must be provided.")
    if folder_path:
        path = create_folder(folder_path)
    for url in urls:
        try:
            print("getting response")
            response = requests.get(url)
            print("done")
        except:
            print("error")

        data, title = get_text(response, all_data)

        if return_as_list:
            articles.append(data)
        else:
            save_txt(data, title, path)
    if articles:
        return articles

