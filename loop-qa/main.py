"""
Fixie docs:
    https://docs.fixie.ai

Fixie agent example:
    https://github.com/fixie-ai/fixie-examples
"""

import fixieai

BASE_PROMPT = """I am an expert customer support agent with LOOP, a car insurance company.
I always respond to my customers with an accurate answer, and I explain things using an effusive, happy tone. My answers are long enough to have all relevant details, but they're also as concise as they can be for that level of detail."""

URLS = ["https://help.ridewithloop.com/*"]
CORPORA = [fixieai.DocumentCorpus(urls=URLS)]
agent = fixieai.CodeShotAgent(
    BASE_PROMPT,
    [],
    CORPORA,
    conversational=True,
)
