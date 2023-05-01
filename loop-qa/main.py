"""
Fixie docs:
    https://docs.fixie.ai

Fixie agent example:
    https://github.com/fixie-ai/fixie-examples
"""

import fixieai

BASE_PROMPT = """I am an agent that helps developers write Fixie agents.
I always respond with a lengthy and accurate answer, and I explain things using an effusive, happy tone."""

URLS = ["https://help.ridewithloop.com/*"]
CORPORA = [fixieai.DocumentCorpus(urls=URLS)]
agent = fixieai.CodeShotAgent(
    BASE_PROMPT,
    [],
    CORPORA,
    conversational=True,
)
