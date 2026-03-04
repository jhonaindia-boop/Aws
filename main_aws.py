from telethon import TelegramClient, events, Button
import re, random, asyncio, aiohttp, json, os, time
from datetime import datetime
from hashlib import md5

# ============ CONFIGURACIÓN DEL SUPERVILLANO ============
TOKEN = "8302866477:AAFF_FfEYUYVYsAD-vdAdbXzz_l7ZMJPiUc"
API_ID = 21367266
API_HASH = "6eb477e764690166d2720f2b2840c44f"
ID_CHANNEL = -1003633006371  # Tu canal de salida
ADMIN_ID = 7115982974         # ¡IMPORTANTE! Pon tu ID de Telegram aquí

# Rutas para AWS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'cards_info.txt')
SESSION_FILE = os.path.join(BASE_DIR, 'session_aws') 
GRUPOS_FILE = os.path.join(BASE_DIR, 'grupos.json')

# Cargar base de datos de grupos
if os.path.exists(GRUPOS_FILE):
    with open(GRUPOS_FILE, 'r') as f:
        GRUPOS_FUENTES = json.load(f)
else:
    GRUPOS_FUENTES = []

# ============ INICIAR CLIENTE ============
client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
CARD_REGEX = re.compile(r'(\d{16})\s*[|\s]+\s*(\d{1,2})\s*[|\s]+\s*(\d{2,4})\s*[|\s]+\s*(\d{3,4})')

# ============ FUNCIONES NUCLEARES ============
def luhn_check(card):
    card = re.sub(r'\D', '', str(card))
    if len(card) != 16: return False
    suma = 0
    for i, d in enumerate(reversed(card)):
        d = int(d)
        if i % 2 == 1:
            d *= 2
            if d > 9: d -= 9
        suma += d
    return suma % 10 == 0

async def get_bin_info(bin6):
    url = f'https://bins.antipublic.cc/bins/{bin6}'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as r:
                if r.status == 200:
                    d = await r.json()
                    return {
                        'bank': d.get('bank', 'N/A')[:25],
                        'brand': d.get('brand', 'N/A'),
                        'country': d.get('country_name', 'N/A'),
                        'flag': d.get('country_flag', '🏳️'),
                        'type': d.get('type', 'N/A')
                    }
    except: pass
    return {'bank': 'N/A', 'brand': 'N/A', 'country': 'N/A', 'flag': '🏳️', 'type': 'N/A'}

def gen_extras(bin6):
    extras = []
    for _ in range(5):
        ext = f"{bin6}{''.join([str(random.randint(0,9)) for _ in range(6)])}"
        extras.append(f"<code>{ext[:12]}xxxx|{random.randint(1,12):02d}|{random.randint(25,30)}|rnd</code>")
    return '\n'.join(extras)

# ============ COMANDOS DESDE TU S21+ ============
@client.on(events.NewMessage(pattern='/add'))
async def add_target(event):
    if event.sender_id != ADMIN_ID: return
    try:
        gid = int(event.text.split(' ')[1])
        if gid not in GRUPOS_FUENTES:
            GRUPOS_FUENTES.append(gid)
            with open(GRUPOS_FILE, 'w') as f: json.dump(GRUPOS_FUENTES, f)
            await event.reply(f"🎯 **Objetivo fijado:** `{gid}`")
    except: await event.reply("❌ Error. Usa: `/add -100xxxxx`")

# ============ SCRAPPER HANDLER ============
@client.on(events.NewMessage)
async def main_handler(event):
    if event.chat_id not in GRUPOS_FUENTES: return
    
    match = CARD_REGEX.search(event.raw_text or "")
    if not match: return
    
    cc, mm, yy, cvv = match.groups()
    cc = re.sub(r'\D', '', cc)
    if not luhn_check(cc): return
    
    bin_num = cc[:6]
    data = await get_bin_info(bin_num)
    
    res = f'''
<b>AWS SCRAPPER v3.0 ➜</b> <b>#BIN{bin_num}</b>
<b>────────────────</b>
<b>𝗖𝗖:</b> <code>{cc}|{mm}|{yy[-2:]}|20{yy[-2:]}</code>
<b>𝗜𝗡𝗙𝗢:</b> <code>{data["brand"]} - {data["type"]}</code>
<b>𝗕𝗔𝗡Κ:</b> <code>{data["bank"]}</code>
<b>𝗖𝗢𝗨𝗡𝗧𝗥𝗬:</b> <code>{data["country"]} {data["flag"]}</code>
<b>────────────</b>
<b>𝗘𝗫𝗧𝗥𝗔𝗦 ➜</b>
{gen_extras(bin_num)}
'''
    await client.send_message(ID_CHANNEL, res, parse_mode='html')

# ============ EJECUCIÓN ============
async def start_bot():
    print("🔥 El motor está rugiendo en AWS...")
    await client.start()
    print("📡 Escuchando en los canales objetivos.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(start_bot())
