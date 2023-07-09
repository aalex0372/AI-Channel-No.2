

from telethon import TelegramClient
from bs4 import BeautifulSoup
import requests
import Creds
import openai
import time
client = TelegramClient('session_name', Creds.tg_api_id, Creds.tg_hash, proxy=None)
# ----------------------------------------------------------------------------------------------------------------------

links = ["https://graymirror.substack.com/p/62-extreme-arms-control",
         "https://graymirror.substack.com/p/the-historical-guilt-of-the-old-regime",
         "https://graymirror.substack.com/p/reading-in-la-518"]
# Not a complete list
# ----------------------------------------------------------------------------------------------------------------------
for i in links:

    url_post = i
    response = requests.get(url_post)
    # ------------------------------------------------------------------------------------------------------------------
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find("h1", class_="post-title unpublished")
    # ------------------------------------------------------------------------------------------------------------------
    soup = BeautifulSoup(response.text, "html.parser")
    element = soup.find("div", class_="body markup", dir="auto")
    text_parts = []
    # ------------------------------------------------------------------------------------------------------------------
    for content in element.contents:
        if content.name == "a":
            text_parts.append(content.get_text(strip=True))
            text_parts.append(content["href"])
        else:
            text_parts.append(str(content).strip())
    text = " ".join(text_parts)
    # ------------------------------------------------------------------------------------------------------------------
    openai.api_key = Creds.key_il
    completion = openai.ChatCompletion.create(
        temperature=0.5,
        model="gpt-3.5-turbo",  # this is "ChatGPT" $0.002 per 1k tokens
        messages=[{"role": "system", "content": "You only translate title into russian"},
                  {"role": "user", "content": title.text}])
    title = completion.choices[0].message.content
    # ------------------------------------------------------------------------------------------------------------------
    openai.api_key = Creds.key_il
    completion = openai.ChatCompletion.create(
        temperature=0.5,
        model="gpt-3.5-turbo",  # this is "ChatGPT" $0.002 per 1k tokens
        messages=[{"role": "system", "content": "You only translate text into russian, there's html text - be careful"},
                  {"role": "user", "content": text}])
    text = completion.choices[0].message.content.strip()
    # ------------------------------------------------------------------------------------------------------------------

    async def send_message_to_channel():
        channel_username = '@aigraymirror'
        await client.send_message(channel_username, f"{title}\n\n{text}", link_preview=True, parse_mode="HTML")
    time.sleep(30)  # 86400 = 24h
# ----------------------------------------------------------------------------------------------------------------------
    with client:
        client.loop.run_until_complete(send_message_to_channel())