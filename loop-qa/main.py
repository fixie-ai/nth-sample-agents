"""A templated Fixie agent!

Fixie docs:
    https://docs.fixie.ai

Fixie agent example:
    https://github.com/fixie-ai/fixie-examples
"""

import fixieai
import requests

base_url = "https://ridewithloop.zendesk.com/api/v2/help_center/en-us/articles.json?page=1"

response = requests.get(base_url)
json_data = response.json()

highest_page = json_data["page_count"]
valid_urls = [f"{base_url}{page}" for page in range(1, highest_page + 1)]

BASE_PROMPT = """I am an agent that helps developers write Fixie agents.
I always respond with a lengthy and accurate answer, and I explain things using an effusive, happy tone."""

CORPORA = [fixieai.DocumentCorpus(urls=valid_urls)]
agent = fixieai.CodeShotAgent(
    BASE_PROMPT,
    [],
    CORPORA,
    conversational=True,
)
