import os
import asyncio
import importlib
import glob
import builtins
from pyrogram import Client, errors
from dotenv import load_dotenv

# Load variabel dari file config.env
load_dotenv("config.env")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "my_account").strip()

async def start_bot():
    session_file = f"{SESSION_NAME}.session"
    if os.path.exists(session_file):
        print("📂 Session ditemukan, mencoba login...")
    else:
        print("📂 Session tidak ditemukan, membuat session baru...")

    app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)
    builtins.app = app  # supaya modul bisa akses app

    try:
        await app.start()
        print("✅ Userbot berhasil login")
    except errors.SessionPasswordNeeded:
        password = input("🔑 Masukkan password 2FA: ")
        await app.check_password(password)
    except errors.FloodWait as e:
        print(f"⏳ FloodWait {e.x} detik...")
        await asyncio.sleep(e.x)
        return await start_bot()
    except errors.RPCError as e:
        if "SESSION_REVOKED" in str(e) or "AUTH_KEY_UNREGISTERED" in str(e):
            print("⚠️ Session dicabut/invalid. Menghapus & membuat ulang...")
            if os.path.exists(session_file):
                os.remove(session_file)
            return await start_bot()
        print(f"❌ RPC Error: {e}")
        return
    except Exception as e:
        print(f"❌ Error tidak terduga: {e}")
        if os.path.exists(session_file):
            os.remove(session_file)
        return await start_bot()

    # Load modul dari folder modules/
    module_files = glob.glob("modules/*.py")
    for module_path in module_files:
        module_name = module_path.replace("/", ".").replace(".py", "")
        importlib.import_module(module_name)
        print(f"📦 Module {module_name} dimuat")

    print("🤖 Userbot berjalan...")
    await asyncio.Event().wait()  # supaya tetap jalan

# Jalankan aman di Termux/Acode
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = None

if loop and loop.is_running():
    asyncio.create_task(start_bot())
else:
    asyncio.run(start_bot())