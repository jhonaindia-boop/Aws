from telethon import TelegramClient
import asyncio
import sys

# Tus datos
API_ID = 21367266
API_HASH = "6eb477e764690166d2720f2b2840c44f"
SESSION_NAME = 'session_aws'

async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    print("--- CONECTANDO A TELEGRAM DESDE AWS ---")
    try:
        await client.connect()
        if not await client.is_user_authorized():
            phone = input("Introduce tu número (ej: +549...): ")
            print(f"Enviando código a {phone}...")
            await client.send_code_request(phone)
            
            code = input("Introduce el código que te llegó a Telegram: ")
            try:
                await client.sign_in(phone, code)
            except Exception as e:
                # Si tienes verificación en dos pasos (password)
                password = input("Introduce tu contraseña de 2 pasos: ")
                await client.sign_in(password=password)
        
        print("\n✅ SESIÓN CREADA EXITOSAMENTE")
        print("Ya puedes ver el archivo 'session_aws.session' en tu carpeta.")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
