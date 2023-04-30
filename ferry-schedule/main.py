"""A templated Fixie agent!

Fixie docs:
    https://docs.fixie.ai

Fixie agent example:
    https://github.com/fixie-ai/fixie-examples
"""

import fixieai
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz


BASE_PROMPT = """I am an agent that looks up ferry schedules."""

FEW_SHOTS = """
Q: When does the next ferry leave Edmonds?
Ask Func[schedule]:
Func[schedule] says: '\n\t\t\tLeave Edmonds (Daily)\n\t\t\n\t\t\t  5:35 1 11:55 1  6:15 111:45 1\n\t\t\n\t\t\t  6:10 2 12:40 2  7:00 2 \n\t\t\n\t\t\t  7:10 1  1:35 1  7:40 1 \n\t\t\n\t\t\t  7:55 2  2:25 2  8:30 2 \n\t\t\n\t\t\t  8:50 1  3:15 1  9:05 1 \n\t\t\n\t\t\t  9:35 2  3:55 2  9:50 2  \n\t\t\n\t\t\t10:20 1  4:45 110:25 1 \n\t\t\n\t\t\t11:05 2  5:25 211:10 2  \n\t\t\n\t\t\tLeave Kingston (Daily)\n\t\t\n\t\t\t  4:45 1 11:05 1  5:30 111:10 1\n\t\t\n\t\t\t  5:30 2 11:55 2  6:10 2 \n\t\t\n\t\t\t  6:25 112:45 1  7:00 1 \n\t\t\n\t\t\t  7:00 2  1:30 2  7:45 2 \n\t\t\n\t\t\t  7:55 1  2:30 1  8:20 1 \n\t\t\n\t\t\t  8:40 2  3:10 2  9:10 2  \n\t\t\n\t\t\t  9:35 1  4:00 1  9:40 1 \n\t\t\n\t\t\t10:20 2  4:40 210:30 2  \n\t\t\n\t'
Ask Func[time_in_seattle]:
Func[time_in_seattle] says: 10:25 AM
A: The next Ferry leaving Edmonds is 11:05 AM.

Q: When does the next ferry leave Kingston?
Ask Func[schedule]:
Func[schedule] says: '\n\t\t\tLeave Edmonds (Daily)\n\t\t\n\t\t\t  5:35 1 11:55 1  6:15 111:45 1\n\t\t\n\t\t\t  6:10 2 12:40 2  7:00 2 \n\t\t\n\t\t\t  7:10 1  1:35 1  7:40 1 \n\t\t\n\t\t\t  7:55 2  2:25 2  8:30 2 \n\t\t\n\t\t\t  8:50 1  3:15 1  9:05 1 \n\t\t\n\t\t\t  9:35 2  3:55 2  9:50 2  \n\t\t\n\t\t\t10:20 1  4:45 110:25 1 \n\t\t\n\t\t\t11:05 2  5:25 211:10 2  \n\t\t\n\t\t\tLeave Kingston (Daily)\n\t\t\n\t\t\t  4:45 1 11:05 1  5:30 111:10 1\n\t\t\n\t\t\t  5:30 2 11:55 2  6:10 2 \n\t\t\n\t\t\t  6:25 112:45 1  7:00 1 \n\t\t\n\t\t\t  7:00 2  1:30 2  7:45 2 \n\t\t\n\t\t\t  7:55 1  2:30 1  8:20 1 \n\t\t\n\t\t\t  8:40 2  3:10 2  9:10 2  \n\t\t\n\t\t\t  9:35 1  4:00 1  9:40 1 \n\t\t\n\t\t\t10:20 2  4:40 210:30 2  \n\t\t\n\t'
Ask Func[time_in_seattle]:
Func[time_in_seattle] says: 4:37 PM
A: The next Ferry leaving Kingston is 4:40 PM.
"""
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS, llm_settings=fixieai.LlmSettings(temperature=0.0, model="openai/gpt4"))

@agent.register_func
def time_in_seattle(query: fixieai.Message) -> str:
    """There's a built-in Fixie function for getting the "user's local time", but I'm not sure how that's generated. And there's a UTC time, but it seems silly to make a separate LLM call to get that when we can just compute it directly."""
    seattle_tz = pytz.timezone('America/Los_Angeles')
    return datetime.now(seattle_tz).strftime("%I:%M %p")

@agent.register_func
def schedule(query: fixieai.Message) -> str:
    url = "https://wsdot.com/ferries/schedule/scheduledetailbyroute.aspx?route=ed-king"
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')
    element = soup.find(id="cphPageTemplate_rprSailings_gvSailing_0")

    if element:
        return element.text
    else:
        return 'Unexpected HTML structure'
