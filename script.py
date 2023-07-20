import requests
from bs4 import BeautifulSoup

max_results = 3
result_max_characters = 2000


def input_modifier(string, state):
    if string.strip().lower().startswith("duckduckgo:"):
        searchstring = string[len("search:") :].strip()
        print(f"Performing duckduckgo search: {searchstring}")

        url = f"https://duckduckgo.com/html?q={searchstring}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        result_urls = []
        for result in soup.select(".result__url"):
            url = result.text.strip()
            if url != "":  # skip any empty urls
                print(f"possible search url: {url}")
                result_urls.append(url)
        texts = string + " "
        count = 0
        for result_url in result_urls:
            try:
                if count <= max_results:
                    print(f"querying url: {result_url}")
                    response = requests.get("https://" + result_url, headers=headers)
                    soup = BeautifulSoup(response.content, "html.parser")
                    text = (
                        soup.get_text()
                        .strip()
                        .replace("\n", " ")
                        .replace("\r", "")
                        .replace("\t", "")
                    )
                    texts = texts + " " + text
                    count += 1
            except:
                continue
        texts = texts[0:result_max_characters]
        print(texts)
        return texts
    else:
        print(f"NOT Performing web search: {string.strip().lower()}")
        return string


def output_modifier(string):
    return string


def bot_prefix_modifier(string):
    return string
