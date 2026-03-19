
from discord.ext import commands
import json
import os

TOKEN = "MTQ3NjY3MTI3NzcwNzE2NTc5Nw.GgHfmV.LIKJrYh5Vex0oPAwOk0Qpjl8kaMfnjRLwXXpq8"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "data.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        message_count = json.load(f)
else:
    message_count = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = str(message.author.id)
    message_count[user_id] = message_count.get(user_id, 0) + 1

    with open(DATA_FILE, "w") as f:
        json.dump(message_count, f)

    await bot.process_commands(message)

@bot.command()
async def top(ctx):
    sorted_users = sorted(message_count.items(), key=lambda x: x[1], reverse=True)[:10]

    if not sorted_users:
        await ctx.send("No data yet.")
        return

    reply = "🏆 Top Message Senders:\n"
    for i, (user_id, count) in enumerate(sorted_users, 1):
        user = await bot.fetch_user(int(user_id))
        reply += f"{i}. {user.name} - {count} messages\n"

    await ctx.send(reply)

bot.run(TOKEN)
