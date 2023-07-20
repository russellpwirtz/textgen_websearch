from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()

max_results = 10
max_characters_per_result = 2000

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

      snippets = [result['snippet'] for result in results['organic_results']]
      highlights = [result['snippet_highlighted_words'] for result in results['organic_results']]

      count = 0
      texts = "For context: "

      for snippet in snippets:
          try:
              if count <= max_results:
                  texts += f"\n{snippet[0:max_characters_per_result]}"
                  count += 1
          except:
              continue
          
      texts += "\nContext highlights:"
      for highlight in highlights:
          try:
              texts += f"\n{highlight[0:max_characters_per_result]}"
          except:
              continue
          
      texts += f"\nGiven that context, {initial_prompt}"

      # print(texts)

      return texts
    else:
        # print(f"NOT Performing web search: {inputstring.strip().lower()}")
        return inputstring
