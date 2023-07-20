from serpapi import DuckDuckGoSearch

from dotenv import load_dotenv
import os
from modules.text_generation import generate_reply
load_dotenv()
import requests
from bs4 import BeautifulSoup

max_results = 3
max_characters_per_result = 20000

SERP_STRING = "serpapi:"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

def input_modifier(inputstring, state):
    if SERP_STRING in inputstring.strip().lower():
      start_search = inputstring.find(SERP_STRING)
      searchstring = inputstring[start_search+len(SERP_STRING):].strip()
      initial_prompt = inputstring[0:start_search]

      print(f"Performing SERP web search: {searchstring}")

      params = {
          "q": searchstring,
          "num": max_results,
          "api_key": os.getenv("SERPAPI_API_KEY")
      }

      search = DuckDuckGoSearch(params)
      results = search.get_dict()
      links = [result['link'] for result in results['organic_results']]
      print(f"Found links from google search: {str(links)}")

      count = 0
      texts = ''
      web_context = ''

      for result_url in links:
        print(f"Calling url: {result_url}")
        response = requests.get(result_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        web_raw = soup.get_text().strip().replace('\n', ' ').replace('\r', '').replace('\t', '')
        web_clean = call_llm(get_clean_prompt(web_raw), state)
        web_context = web_context + web_clean + '\n'
        count += 1

        if count > max_results: 
          break

      # for snippet in snippets:
      #     try:
      #         if count <= max_results:
      #             texts += f"\n{snippet[0:max_characters_per_result]}"
      #             count += 1
      #     except:
      #         continue
          
      texts += f"Given the following context, answer the user without making up facts.\n"
      texts += f"Context: {web_context}\n"
      texts += f"### User: {initial_prompt}"
      # print(texts)

      return texts
    else:
        # print(f"NOT Performing web search: {inputstring.strip().lower()}")
        return inputstring

def get_clean_prompt(webpage_content: str) -> str:
    webpage_content = webpage_content[0:max_characters_per_result]
    review_prompt = f'''
### Instruction: You are a summarization bot.
### Content: {webpage_content}
### User: The above is content scraped from a webpage using serpapi. 
Please provide the important content, removing the additional cruft associated with webpage content?
### Response: '''
    return review_prompt

def call_llm(input_prompt: str, state: dict) -> str:
    generator = generate_reply(input_prompt, state, is_chat=False)
    final_answer = ''
    for answer in generator:
        final_answer = answer
    return final_answer
