import discord
from discord.ext import commands
import random
import json
import os

import os
TOKEN = os.environ["MTQwNjY2ODUwODI3NTgwNjQ1MA.G40Drk.LjiXC6S77ibtuOglTCcrPKJJbrBCr8wASFWPyk"]

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Balance file
BALANCE_FILE = "balances.json"

def load_balances():
    if os.path.exists(BALANCE_FILE):
        with open(BALANCE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_balances(data):
    with open(BALANCE_FILE, "w") as f:
        json.dump(data, f)

balances = load_balances()

# Balance helpers
def get_balance(user_id):
    return balances.get(str(user_id), 100)  # new users start with 100

def set_balance(user_id, amount):
    balances[str(user_id)] = amount
    save_balances(balances)

@bot.command()
async def balance(ctx):
    bal = get_balance(ctx.author.id)
    await ctx.send(f"💰 {ctx.author.mention}, your current balance is **{bal}** credits.")

@bot.command()
async def slot(ctx, bet: int):
    if bet < 10:
        await ctx.send("❌ Minimum bet is **10**!")
        return
    
    bal = get_balance(ctx.author.id)
    if bal < bet:
        await ctx.send("❌ You don't have enough credits to play!")
        return
    
    # Slot symbols
    symbols = ["🍒", "🍋", "🍇", "7️⃣", "⭐"]
    result = [random.choice(symbols) for _ in range(3)]

    # Payout logic
    if result[0] == result[1] == result[2]:
        win = bet * 5
        message = f"🎉 JACKPOT!!! You won **{win}** credits! 🎉"
    elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
        win = bet * 2
        message = f"✨ Nice! You matched two symbols and won **{win}** credits!"
    else:
        win = 0
        message = f"😢 You lost your bet of **{bet}** credits. Better luck next time!"

    # Update balance
    new_balance = bal - bet + win
    set_balance(ctx.author.id, new_balance)

    # Output
    await ctx.send(
        f"🎰 | {' | '.join(result)} |\n"
        f"{message}\n"
        f"💰 Your new balance: **{new_balance}** credits."
    )

bot.run(TOKEN)

