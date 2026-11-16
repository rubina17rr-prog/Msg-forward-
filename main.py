import os
import asyncio
import random
from threading import Thread
from telethon import TelegramClient, errors
from telethon.sessions import StringSession

try:
    from flask import Flask
    FLASK_INSTALLED = True
except ImportError:
    FLASK_INSTALLED = False

# ================= CONFIGURATION =================
API_ID = int(os.environ.get("API_ID", 32922341))
API_HASH = os.environ.get("API_HASH", "c22e8a72384629d148249a3e501ded82")

# Aapka Generated String Session
SESSION_STRING = os.environ.get(
    "SESSION_STRING",
    "1BVtsOMUBu0zIbRmCKsQk-VJiaWFeBXYZDytrwnI7ts9_W8h945E41_OqdA2zSHmCluxy6A7fSm5VeeBO464RmiIDQkdyrEMQnsYnrg_FPMvmrh4lQV-LLPxndnFk6ZM3hWAgPY5O2hOs3PlYrqqRg_gXyJ6bjTtduXJd_-v1BiC7v6nRMur2hS0y5GA7HmMsCMHihcbSrZ0NTQGAn-W-TiaAkz8GQ-RxxWWMGFfdTlfwnszfaDPrWU4peYYbh4kpjJChHMD_JdPvAZSylx3psd2LThBVSfXPi-4sPmhDmOpG1voePRN9rL1UoMJ1Z7kcaEhv5veeTeellpKNbBrb3eeKMek1-6A="
)

# Aapke Source Channels aur Message IDs
SOURCES = {
    '@cjjg7': [15],
    '@jgitih': [2]
}

# Aapke 7 Target Groups
TARGET_GROUPS = [
    '@instaAccountbuying',
    '@igcustomers',
    '@gmailbuyandsellzeus',
    '@page_marketplace_IG',
    '@USA_Buying_Selling_Pages_Market',
    '@Sell_Buy_accountGroups',
    '@GroupOfSellersandBuyers'
]

# Time Settings
INTERVAL_SECONDS = 1860          # 31 Minutes ka wait har round ke baad
DELAY_BETWEEN_GROUPS = (30, 40)  # Har group ke beech 30 se 40 sec ka gap

DROP_AUTHOR_TAG = False
# =================================================

def keep_alive():
    if not FLASK_INSTALLED:
        return
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "✅ TG SHOP Multi-Channel Auto Forwarder is Running 24/7!"

    def run_flask():
        port = int(os.environ.get("PORT", 8080))
        app.run(host="0.0.0.0", port=port)

    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    print("🌐 Flask Keep-Alive Server Started!")

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def start_forwarding():
    await client.start()
    print("✅ Userbot successfully login ho gaya hai!")
    
    round_count = 1
    while True:
        print(f"\n🔄 --- Forwarding Round {round_count} Shuru ---")
        
        for source_channel, msg_ids in SOURCES.items():
            for msg_id in msg_ids:
                print(f"\n📨 Channel [{source_channel}] ka Message ID [{msg_id}] bhej rahe hain...")
                
                for group in TARGET_GROUPS:
                    try:
                        await client.forward_messages(
                            entity=group,
                            messages=msg_id,
                            from_peer=source_channel,
                            drop_author=DROP_AUTHOR_TAG
                        )
                        print(f"  ✔️ Sent to {group}")
                        
                        sleep_time = random.randint(*DELAY_BETWEEN_GROUPS)
                        await asyncio.sleep(sleep_time)
                        
                    except errors.FloodWaitError as e:
                        print(f"  ⚠️ FloodWait: {e.seconds} seconds rukna padega...")
                        await asyncio.sleep(e.seconds + 5)
                    except errors.SlowModeWaitError as e:
                        print(f"  ⏳ SlowMode in {group}: {e.seconds}s baad hi bhej sakte hain (Skipping)...")
                    except errors.ChatWriteForbiddenError:
                        print(f"  ❌ Error: {group} mein message bhejne ki permission nahi hai (Join check karein).")
                    except Exception as e:
                        print(f"  ❌ Error in {group}: {e}")
                        
        print(f"\n✅ Round {round_count} Complete! Ab {INTERVAL_SECONDS // 60} minutes ka wait...")
        round_count += 1
        await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == '__main__':
    keep_alive()
    with client:
        client.loop.run_until_complete(start_forwarding())
