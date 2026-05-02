import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv
from datetime import date, datetime
from agenda import agenda_van_morgen

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
USER_ID = int(os.getenv("DISCORD_USER_ID"))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

dm_teller = 0
laatste_dag = date.today()
MAX_DMS_PER_DAG = 20
LOG_BESTAND = "dm_log.txt"

def schrijf_log(bericht, teller):
    tijdstip = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_BESTAND, "a", encoding="utf-8") as f:
        f.write(f"[{tijdstip}] DM verzonden ({teller}/{MAX_DMS_PER_DAG})\n")
        f.write(bericht + "\n")
        f.write("-" * 40 + "\n")

@client.event
async def on_ready():
    print(f"✅ Bot online als {client.user}")

    user = await client.fetch_user(USER_ID)
    await user.send("✅ Test: ik kan je DM’en!")

    check_morgen.start()

@tasks.loop(minutes=30)
async def check_morgen():
    global dm_teller, laatste_dag
    print("📅 Items voor morgen:", items)


    vandaag = date.today()

    # 🔄 Reset bij nieuwe dag
    if vandaag != laatste_dag:
        dm_teller = 0
        laatste_dag = vandaag

    if dm_teller >= MAX_DMS_PER_DAG:
        return

    items = agenda_van_morgen()
    if not items:
        return

    user = await client.fetch_user(USER_ID)

    bericht = "📅 **Je agenda voor morgen:**\n\n"
    for item in items:
        bericht += f"• {item}\n"

    await user.send(bericht)

    dm_teller += 1
    schrijf_log(bericht, dm_teller)

    print(f"📨 DM verzonden ({dm_teller}/{MAX_DMS_PER_DAG})")
@client.event
async def on_message(message):
    # Negeer andere bots
    if message.author.bot:
        return

    if message.content.lower() == "/checknu":
        await message.channel.send("🔍 Ik check nu je agenda voor morgen...")

        items = agenda_van_morgen()

        if not items:
            await message.channel.send(
                "✅ Ik zie **geen items** in je agenda voor morgen."
            )
            return

        antwoord = "📅 **Agenda voor morgen (live check):**\n\n"
        for item in items:
            antwoord += f"• {item}\n"

        await message.channel.send(antwoord)
client.run(TOKEN)
