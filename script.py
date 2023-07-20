from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()

max_results = 10
result_max_characters = 5000

SERP_STRING = "serpapi:"

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

      search = GoogleSearch(params)
      results = search.get_dict()
      # print(f"RAW RESULTS:\n\n{str(results)}\n\n")

      count = 0
      texts = initial_prompt + "\nFor context: "

      for result in results['organic_results']:
          try:
              if count <= max_results:
                  texts += f"\n{result['snippet']}"
                  count += 1
          except:
              continue
      texts = texts[:result_max_characters]
      print(texts)

      return texts
    else:
        # print(f"NOT Performing web search: {inputstring.strip().lower()}")
        return inputstring
