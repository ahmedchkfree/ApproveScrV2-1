import re
import asyncio
from telethon import TelegramClient, events
from config import API_ID, API_HASH, SESSION, SEND_ID
from datetime import datetime
import os
import requests

current_directory = os.path.dirname(os.path.realpath(__file__))

client = TelegramClient(
    session='alterchkbot_alpha',
    api_id=API_ID,
    api_hash=API_HASH
)

async def filter_cards(text):
    regex = r'\d{16}.*\d{3}'
    matches = re.findall(regex, text)
    if matches:
        return ''.join(matches)
    else:
        return None

async def alterchkbot(message):
    try:
        rt = 0
        while rt < 6:
            if 'Checking CC. Please wait.🟥' in message.message or 'Checking CC. Please wait.🟧' in message.message or 'Checking CC. Please wait.🟩' in message.message or 'CHECKING CARD 🔴' in message.message:
                await asyncio.sleep(30)
                message = await client.get_messages(entity=message.chat_id, ids=message.id)
                rt += 1
                continue
            else:
                break

        if re.search(r'Approved', message.message):
            card = await filter_cards(message.message)
            if card is None:
                return

            # Check if the card has been posted before
            if await card_exists_in_alterchkbot_file(card):
                return

            new_text = re.sub(r'Checked by .* User]', '**Checked ву [˹ᴧŁþнᴧ ꭙ˼](tg://user?id=1057412250)** \n━━━━━━━━━━━━━━━━━',
                              message.message)

            new_text = new_text.replace('Bot by --» Tfp0days☃️', '')
            new_text = new_text.replace('———»Details«———', '━━━━━━━━━━━━━━━━━')
            new_text = new_text.replace('———-»Info«-———-', '━━━━━━━━━━━━━━━━━')
            new_text = new_text.replace('-»', '➻')

            cc_match = re.search(r'\d{16}', new_text)
            date_match = re.search(r'\d{2}\|\d{2}', new_text)
            cvv_match = re.search(r'\d{3}', new_text)
            if cc_match is None or date_match is None or cvv_match is None:
                return
            cc = cc_match.group(0)
            date = date_match.group(0)
            cvv = cvv_match.group(0)

            bin = cc[:6]
            gateway = re.search(r'Gateway: (.+?)\n', message.message).group(1)
            result = re.search(r'Result: (.+?)\n', message.message).group(1)
            status = 'Approved ✅'
            gateway = 'Unknown'
            result = 'Unknown'

            response = requests.get(f"https://bins.antipublic.cc/bins/{bin}")
            if response.status_code == 200:
                data = response.json()
                info = data.get('level')
                bank = data.get('bank')
                type = data.get('type')
                country = data.get('country')
                country_flag = data.get('countryInfo').get('emoji')
            else:
                info = 'Unknown'
                bank = 'Unknown'
                country = 'Unknown'

            current_time = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
            new_text = f"""• Card ⌁
   {cc}|{date}|{cvv}

• Status ⌁ {status}
• Gateway ⌁ {gateway}
• Result ⌁ {result}

• Bin  ⌁ ({bin})

• Info ⌁ {info}
• Bank ⌁ {bank}
• Type ⌁ {type}
• Country ⌁ {country} {country_flag}

Check by - ALPHA

• Time : {current_time}"""

            # Post the new credit card to the channel
            await client.send_message(SEND_ID, message=new_text)

            # Write the new credit card to Kurumi.txt
            with open('alterchk.txt', 'a', encoding='utf-8') as f:
                f.write(f"{cc} - Apprroved ✅\n")

    except Exception as e:
        print(e)

async def card_exists_in_alterchkbot_file(card):
    with open('alterchk.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if card in line:
                return True
    return False

@client.on(events.NewMessage())
async def suck(event):
    if event.message:
        await asyncio.create_task(alterchkbot(event.message))

client.start()
client.run_until_disconnected()
