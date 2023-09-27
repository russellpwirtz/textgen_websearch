# textgen_websearch
An extension for text-generation-webui to provide web searches as context

## Setup
- rename .env.example to .env and update the api key value. For your key: https://serpapi.com/manage-api-key
- update dependencies: `pip install -r requirements.txt`

## Available search engines:
- `google:`
- `bing:`
- `ddg:` (DuckDuckGo)
## Examples:
Ask a question based on the search result:
> What should I wear? bing: Antartica weather tomorrow

>Based on the current weather conditions in Antarctica, it seems that it is quite chilly, with temperatures ranging from -4°F to -62°F (-20°C to -52°C) and windchill temperatures dropping as low as -9°F (-23°C). It is recommended to dress warmly, layering up with thermal underwear, insulated jackets, gloves, hats, scarves, and warm socks to counter the biting cold. Additionally, consider wearing waterproof boots with good grip to navigate snowy and icy terrain.

Ask the same question to the search engine and the LLM:
> google: what is the best godfather movie?

> The best Godfather movie is subjective and depends on individual opinions and preferences. However, here are the rankings of the Godfather movies according to various sources:
>Every Godfather Movie, Ranked by Critics:
The Godfather (1972) - 98.5/10
The Godfather Part II - 93
The Godfather Part III - 63.5
