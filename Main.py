import os
import discord
from discord.ext import commands
from twitchio.ext import commands as twitch_commands
from flask import Flask
import threading

# =======================
# CONFIG (pega do Railway ou coloca direto para testar)
# =======================
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN") or "COLOQUE_SEU_TOKEN_DO_DISCORD"
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID") or 123456789012345678)
TWITCH_TOKEN = os.getenv("TWITCH_TOKEN") or "COLOQUE_SEU_TOKEN_TWITCH"
TWITCH_CHANNEL = os.getenv("TWITCH_CHANNEL") or "nomedocanal"

# =======================
# BOT DISCORD
# =======================
intents = discord.Intents.default()
intents.messages = True
bot_discord = commands.Bot(command_prefix="!", intents=intents)

@bot_discord.event
async def on_ready():
    print(f"✅ Logado no Discord como {bot_discord.user}")

# =======================
# BOT TWITCH
# =======================
class TwitchBot(twitch_commands.Bot):
    def __init__(self):
        super().__init__(
            token=TWITCH_TOKEN,
            prefix="!",
            initial_channels=[TWITCH_CHANNEL]
        )

    async def event_ready(self):
        print(f"✅ Logado na Twitch como {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return
        print(f"[Twitch] {message.author.name}: {message.content}")
        channel = bot_discord.get_channel(DISCORD_CHANNEL_ID)
        if channel:
            await channel.send(f"🎮 **{message.author.name}**: {message.content}")

twitch_bot = TwitchBot()

# =======================
# FLASK + KEEP ALIVE
# =======================
app = Flask("")

@app.route("/")
def home():
    return "Bot está rodando!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# =======================
# INICIAR TUDO
# =======================
if __name__ == "__main__":
    keep_alive()
    threading.Thread(target=lambda: twitch_bot.run()).start()
    bot_discord.run(DISCORD_TOKEN)
