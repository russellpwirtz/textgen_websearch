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
load_dotenv()
import requests
from bs4 import BeautifulSoup
import modules.shared as shared

chars_per_token = 4
system_instruction_tokens = 50
tokens_per_result = 2000
max_search_results = 10
max_characters_per_result = tokens_per_result * chars_per_token

GOOGLE_STRING = "google:"
DUCKDUCKGO_STRING = "ddg:"
BING_STRING = "bing:"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

def input_modifier(input, state):
    truncation_length = state['truncation_length']
    max_seq_len = state['max_seq_len'] # exllama
    max_new_tokens = state['max_new_tokens']

    context_length = int(truncation_length) if int(max_seq_len) > int(truncation_length) else int(max_seq_len)
    max_tokens = int(context_length) - int(max_new_tokens) - system_instruction_tokens

    print(f'''
          truncation_length:{truncation_length} 
          max_seq_len:{max_seq_len} 
          max_new_tokens:{max_new_tokens}; 
          max_characters_per_result: {max_characters_per_result}
          -> context_length: {context_length}
          -> max_tokens:{max_tokens} 
          ''')

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

    if start_search == 0:
      initial_prompt = inputstring[len(serp_string):]
    else:
      initial_prompt = inputstring[0:start_search]

    print(f"Performing web search: {searchstring}")

    params = {
        "q": searchstring,
        "num": max_search_results,
        "api_key": os.getenv("SERPAPI_API_KEY")
    }

    search = searchTool(params)
    results = search.get_dict()

    if 'organic_results' not in results:
        print(f"Can't find organic_results. Raw results: {str(results)}")
        return inputstring
    
    links = [result['link'] for result in results['organic_results']]
    print(f"Found links from web search: {str(links)}")

    web_context = ''

    for result_url in links:
      print(f"Calling url: {result_url}")
      response = requests.get(result_url, headers=headers)
      soup = BeautifulSoup(response.content, 'html.parser')
      web_raw = soup.get_text().strip().replace('\n', ' ').replace('\r', '').replace('\t', '')
      web_raw = ' '.join(web_raw.split()) 
      web_context += web_raw[0:max_characters_per_result] + '\n'

      token_count = get_token_count(web_context)
      print(f"Ongoing token count: {token_count}")
      if token_count >= max_tokens: 
        print(f"breaking out early from web searches; token count: {token_count}, max_tokens: {max_tokens}")
        break

    trim_index = len(web_context)-1
    while (get_token_count(web_context) >= max_tokens):
       trim_index -= 100
       print(f"Trimming result to fit in context; trim_index: {trim_index}")
       web_context = web_context[0:trim_index]

    result_text = "Given the following context, answer the user without making up facts.\n"
    result_text += f"<<CONTEXT>>{web_context}<</CONTEXT>>\n"
    result_text += f"<<USER>>{initial_prompt}<</USER>>"

    print(f"->> Input token length: {get_token_count(result_text)}")
    return result_text

def get_token_count(text):
    return int(shared.tokenizer.encode(str(text)).shape[1])