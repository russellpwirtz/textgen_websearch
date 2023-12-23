# textgen_websearch
An extension for text-generation-webui to provide web searches as context. The web search results are provided as context for the LLM query. 

Possible seaerch engines:
- `google:`
- `bing:`
- `ddg:` (DuckDuckGo)

Syntax:
### Web search to LLM query
> `<search engine>: <web query>`

example:
> `google: what is an LLM`

### Web search with separate LLM query
> `<llm query> <search engine>: <web query>`

example:
> `Who is the most reasonable senator from each side? google: current U.S. senator profiles`

# Setup (Linux instructions)

## Install and install Text Generation WebUI, and download model(s)
https://github.com/oobabooga/text-generation-webui

## Download search extension
- In the Textgen Web UI, click the "Session" tab at the top right
- Paste the github url of this project and and press enter

## Update search configuration
- Open a command terminal, and change directory to the extension 
> `cd text-generation-webui/extensions/textgen_websearch/`)
- rename .env.example to .env and update the API key value with your own. To generate your API key visit: https://serpapi.com/manage-api-key
> `mv .env.example .env`\
> `vim .env`

## Download dependencies: 
- Activate Conda environment:
> `../../cmd_linux.sh`
- Install dependencies: 
> `pip install -r requirements.txt`
- Exit Conda environment: 
> `exit`

## Enable extension at startup:
- Add startup flag for websearch extension:
> `vim ../../CMD_FLAGS.txt` 
- Include this: 
> `--extension textgen_websearch`

## Start extension
- Restart textgen-webui to enable extension

## Examples:
`What should I wear for a short hike? google: Antartica weather tomorrow`
```
Antarctica is currently foggy and quite cold, with a temperature of -23 °F (-30 °C). Therefore, it's essential to dress warmly and protect yourself from the wind. Here's what you should consider wearing for a short hike:

1. Thermal base layers: Moisture-wicking thermal tops and bottoms to keep your skin dry and insulated.
2. Insulating mid-layers: A fleece jacket or down vest would provide additional warmth.
3. Waterproof and windproof outer layer: A Gore-Tex or similar breathable, waterproof parka and pants to shield against wind and snow.
...
```

`bing: Who is the CEO of Twitter?`
```
Linda Yaccarino is the current CEO of Twitter, replacing Elon Musk who remains in a senior role focused on product design and new technology.
```

`ddg: what was the most recent supernova discovery?`
```
The most recent discovery by the James Webb Space Telescope was the observation of a nearby exoplanet named K2-18 b, which has abundant life-supporting molecules such as methane and carbon dioxide in its atmosphere. This discovery was announced in September 2023.
```

## Tested with:
### Exllama
- Mixtral 8x7B instruct / ExLlamav2_HF: https://huggingface.co/turboderp/Mixtral-8x7B-instruct-exl2
- Llama 2 70B / ExLlama: https://huggingface.co/TheBloke/Llama-2-70B-GPTQ

### Llama.cpp
- Mistral 7B / GGUF: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF
