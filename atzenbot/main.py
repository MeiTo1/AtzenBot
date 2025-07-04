import discord
from discord.ext import commands
import os
import random
from collections import defaultdict

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

fight_stats = defaultdict(int)

@bot.event
async def on_ready():
    print(f"✅ Der AtzenBot ist online als {bot.user}")

@bot.command()
async def zocken(ctx, *, spielname: str):
    embed = discord.Embed(
        title=f"🎮 Wer hat Bock auf {spielname}?",
        description="✅ = dabei  |  ⏰ = später  |  ❌ = kein Bock",
        color=discord.Color.green()
    )
    nachricht = await ctx.send(embed=embed)
    await nachricht.add_reaction("✅")
    await nachricht.add_reaction("⏰")
    await nachricht.add_reaction("❌")

@bot.command()
async def fight(ctx, gegner: discord.Member):
    kämpfer1 = ctx.author
    kämpfer2 = gegner

    name1 = kämpfer1.display_name
    name2 = kämpfer2.display_name

    if kämpfer2 == bot.user:
        await ctx.send(f"🥊 {name1} will gegen **AtzenBot** kämpfen...")
        await ctx.send("🤖 AtzenBot weicht aus, kontert... und schlägt brutal zu!")
        await ctx.send("☠️ **AtzenBot ist unbesiegbar.**")
        fight_stats[str(bot.user)] += 1
        return

    if kämpfer1.name.lower() == "meito":
        gewinner = name1 if random.random() < 0.6 else name2
    elif kämpfer2.name.lower() == "meito":
        gewinner = name2 if random.random() < 0.6 else name1
    else:
        gewinner = random.choice([name1, name2])

    verlierer = name2 if gewinner == name1 else name1
    fight_stats[gewinner] += 1

    eröffnungen = [
        f"🥊 {name1} fordert {name2} heraus!",
        f"🥊 {name2} wird von {name1} zum Kampf gezwungen!",
        f"🥊 Zwischen {name1} und {name2} knallt’s gleich richtig!"
    ]

    ausgänge = [
        f"💥 {gewinner} schlägt {verlierer} K.O. – Fight vorbei!",
        f"🩸 {gewinner} sticht {verlierer} ein Auge aus – eskaliert komplett!",
        f"🦴 {gewinner} bricht {verlierer} den Kiefer – keine Chance mehr!",
        f"🚑 {verlierer} bleibt regungslos liegen – Sieg für {gewinner}!",
        f"🔪 {gewinner} rammt ein Messer – {verlierer} hat nichts mehr entgegenzusetzen!"
    ]

    await ctx.send(random.choice(eröffnungen))
    await ctx.send(random.choice(ausgänge))

@bot.command()
async def fightstats(ctx):
    if not fight_stats:
        await ctx.send("Noch keine Fights aufgezeichnet.")
        return

    sorted_stats = sorted(fight_stats.items(), key=lambda x: x[1], reverse=True)
    lines = [f"🏆 **Fight-Stats:**"]
    for name, wins in sorted_stats:
        lines.append(f"🥇 {name}: {wins} Siege")

    await ctx.send("\n".join(lines))

token = os.environ["TOKEN"]
bot.run(token)
