from serpapi import DuckDuckGoSearch
from serpapi import BingSearch
from serpapi import GoogleSearch

# Baidu using BaiduSearch class
# Yahoo using YahooSearch class
# eBay using EbaySearch class
# Yandex using YandexSearch class
# GoogleScholar using GoogleScholarSearch class
# Naver using NaverSearch class

from dotenv import load_dotenv
import os
from modules.text_generation import generate_reply
load_dotenv()
import requests
from bs4 import BeautifulSoup

max_results = 5
max_characters_per_result = 20000

GOOGLE_STRING = "google:"
DUCKDUCKGO_STRING = "ddg:"
BING_STRING = "bing:"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

def input_modifier(input, state):
    inputstring = input.strip()

    serp_string = None
    searchTool = None
    if DUCKDUCKGO_STRING in input:
       serp_string = DUCKDUCKGO_STRING
       searchTool = DuckDuckGoSearch
    elif BING_STRING in input:
       serp_string = BING_STRING
       searchTool = BingSearch
    elif GOOGLE_STRING in input:
       serp_string = GOOGLE_STRING
       searchTool = GoogleSearch
    else:
      return input
    
    print(f"Starting web search! Original input string:\n{input}")
    
    start_search = inputstring.find(serp_string)
    searchstring = inputstring[start_search+len(serp_string):].strip()
    initial_prompt = inputstring[0:start_search]

    print(f"Performing web search: {searchstring}")

    params = {
        "q": searchstring,
        "num": max_results,
        "api_key": os.getenv("SERPAPI_API_KEY")
    }

    search = searchTool(params)
    results = search.get_dict()

    if 'organic_results' not in results:
        print(f"Can't find organic_results. Raw results: {str(results)}")
        return inputstring
    
    links = [result['link'] for result in results['organic_results']]
    print(f"Found links from web search: {str(links)}")

    count = 0
    texts = ''
    web_context = ''

    for result_url in links:
      print(f"Calling url: {result_url}")
      response = requests.get(result_url, headers=headers)
      soup = BeautifulSoup(response.content, 'html.parser')
      web_raw = soup.get_text().strip().replace('\n', ' ').replace('\r', '').replace('\t', '')
      web_clean = call_llm(get_clean_prompt(initial_prompt, web_raw), state)
      web_context = web_context + web_clean + '\n'
      count += 1

      if count > max_results: 
        break

    texts += f"Given the following context, answer the user without making up facts.\n"
    texts += f"Context: {web_context}\n"
    texts += f"### User: {initial_prompt}"
    # print(texts)

    return texts

def get_clean_prompt(question: str, webpage_content: str) -> str:
    webpage_content = webpage_content[0:max_characters_per_result]
    review_prompt = f'''
### Instruction: You are a cleaner bot, to prepare content scraped from a website. 
You do NOT answer the question. Simply clean all of the original content.
Keep any and all details, especially ones that may be relevant for follow-up questions.
Provide all important content; simply clean the cruft associated with web page content and remove unnecessary whitespace.
If the input content is nonsensical, just give an empty reply.\n
Website content: {webpage_content}\n
The extra important parts to keep are related to the question: {question}.
### User: Please prepare the website content in full detail?
### Response: '''
    return review_prompt

def call_llm(input_prompt: str, state: dict) -> str:
    generator = generate_reply(input_prompt, state, is_chat=False)
    final_answer = ''
    for answer in generator:
        final_answer = answer
    return final_answer
