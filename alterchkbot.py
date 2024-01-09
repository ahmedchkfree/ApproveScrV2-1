import re
import asyncio
from pyrogram import Client, filters
from config import API_ID, API_HASH, SESSION, SEND_ID
from datetime import datetime
import os
import requests

current_directory = os.path.dirname(os.path.realpath(__file__))

app = Client(
     name='ahmedchkccfreebot_alpha',
     api_id=API_ID,
     api_hash=API_HASH,
     session_string=str(SESSION),
     in_memory=True,
     workdir=current_directory
)


def filter_cards(text):
    regex = r'\d{16}.*\d{3}'
    matches = re.findall(regex, text)
    if matches:
        return ''.join(matches)
    else:
        return None

async def alterchkbot(app, message):
    try:
        rt = 0
        while rt < 6:
            if 'Checking CC. Please wait.🟥' in message.text or 'Checking CC. Please wait.🟧' in message.text or 'Checking CC. Please wait.🟩' in message.text or 'CHECKING CARD 🔴' in message.text:
                await asyncio.sleep(30)
                message = await app.get_messages(chat_id=message.chat.id, message_ids=message.id)
                rt += 1
                continue
            else:
                break

        if re.search(r'Approved', message.text):
            card = filter_cards(message.text)
            if card is None:
                return

            # Check if the card has been posted before
            if card_exists_in_alterchkbot_file(card):
                return

            new_text = re.sub(r'Checked by .* User]', '**Checked ву [˹ᴧŁþнᴧ ꭙ˼](tg://user?id=1057412250)** \n━━━━━━━━━━━━━━━━━',
                              message.text)

            new_text = new_text.replace('Bot by --» Tfp0days☃️', '')
            new_text = new_text.replace('———»Details«———', '━━━━━━━━━━━━━━━━━')
            new_text = new_text.replace('———-»Info«-———-', '━━━━━━━━━━━━━━━━━')
            new_text = new_text.replace('-»', '➻')

            cc = re.search(r'\d{16}', new_text).group(0)
            date = re.search(r'\d{2}\|\d{2}', new_text).group(0)
            cvv = re.search(r'\d{3}', new_text).group(0)
            bin = cc[:6]
            gateway_search = re.search(r'Gateway: (.+?)\n', message.text)
            gateway = gateway_search.group(1) if gateway_search else 'Unknown'

            result_search = re.search(r'Result: (.+?)\n', message.text)
            result = result_search.group(1) if result_search else 'Unknown'
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
            await app.send_message(SEND_ID, text=new_text)

            # Write the new credit card to Kurumi.txt
            with open('alterchk.txt', 'a', encoding='utf-8') as f:
                f.write(f"{cc} - Apprroved ✅\n")

    except Exception as e:
        print(e)

def card_exists_in_alterchkbot_file(card):
    with open('alterchk.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if card in line:
                return True
    return False

@app.on_message(filters.text)
async def suck(Client, message):
    if message.text:
        await asyncio.create_task(alterchkbot(app, message))

app.run()
