from telethon import TelegramClient
import os

# CONFIGURACIÓN (Tus credenciales de la app)
API_ID = 21367266
API_HASH = "6eb477e764690166d2720f2b2840c44f"
SESSION_NAME = 'session_aws' 

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def main():
    print("=== INICIANDO VINCULACIÓN EN AWS ===")
    print("Introduce tu número con código de país (ej: +549...)")
    await client.start() 
    print("\n✅ ¡ÉXITO! Archivo 'session_aws.session' generado correctamente.")
    print("Ahora puedes borrar este archivo y ejecutar el scrapper principal.")
    await client.disconnect()

import asyncio
if __name__ == '__main__':
    asyncio.run(main())
