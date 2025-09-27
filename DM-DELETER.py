import discord
from discord.ext import commands
import asyncio
import sys
import os
# ⚠️ DISCLAIMER:
# This is a self-bot script (using your user token), which is against Discord’s ToS.
# Running this may get your account banned. Use at your own risk!

def banner():
    OS = os.name
    if OS == "nt":
        os.system("cls")
    else:
        os.system("clear")
    print("=" * 60)
    print("        Discord Selfbot - Multi-Channel Deleter")
    print("=" * 60)

# Show banner
banner()

# User inputs
TOKEN = input("Enter token: ").strip()
channel_count = int(input("How many channels/DMs do you want to delete from? ").strip())

CHANNEL_IDS = []
for i in range(channel_count):
    cid = int(input(f"Enter channel/DM ID #{i+1}: ").strip())
    CHANNEL_IDS.append(cid)

delete_choice = input("How many messages to delete (or type 'ALL'): ").strip()
delay_input = input("Enter delay between deletes in seconds (default 5): ").strip()

# Decide delete count
DELETE_ALL = delete_choice.lower() == "all"
DELETE_COUNT = int(delete_choice) if not DELETE_ALL else None

# Default delay if none entered
DELAY = float(delay_input) if delay_input else 5.0

# Print summary
print("\nSUMMARY")
print("-" * 60)
print(f"Account Token   : {TOKEN[:10]}... (hidden)")
print(f"Channels/DM IDs : {', '.join(map(str, CHANNEL_IDS))}")
print(f"Messages to Del.: {'ALL' if DELETE_ALL else DELETE_COUNT}")
print(f"Delay (seconds) : {DELAY}")
print("-" * 60)

# Ask confirmation
confirm = input("Proceed with deletion? (Y/N): ").strip().lower()
if confirm != "y":
    print("❌ Cancelled.")
    sys.exit()

# Start bot
bot = commands.Bot(command_prefix="!", self_bot=True)

@bot.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n✅ Logged in as {bot.user} (ID: {bot.user.id})")

    for cid in CHANNEL_IDS:
        channel = bot.get_channel(cid)
        if channel is None:
            print(f"❌ Could not find channel/DM ID {cid}. Skipping...")
            continue

        print(f"\n🔹 Deleting messages in Channel/DM ID: {cid}")
        deleted = 0

        async for msg in channel.history(limit=None):
            if not DELETE_ALL and deleted >= DELETE_COUNT:
                break

            if msg.author.id == bot.user.id:  # only delete own messages
                try:
                    await msg.delete()
                    deleted += 1
                    print(f"🗑️ Deleted {msg.id} ({deleted if not DELETE_ALL else 'ALL mode'})")
                    await asyncio.sleep(DELAY)
                except Exception as e:
                    print(f"⚠️ Failed to delete {msg.id}: {e}")

        print(f"✅ Finished channel/DM ID {cid} (Deleted {deleted if not DELETE_ALL else 'ALL available'} messages)")

    print("\n🎉 All channels processed. Done.")
    await bot.close()

bot.run(TOKEN)
