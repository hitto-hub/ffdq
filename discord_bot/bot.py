import os
import random
# Pycordを読み込む
import discord
import dotenv
import requests
from discord.ext import commands,tasks
import time
import json
num_results = 0
# アクセストークンを設定
dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

# Botの大元となるオブジェクトを生成する
bot = discord.Bot(
        intents=discord.Intents.all(),  # 全てのインテンツを利用できるようにする
        activity=discord.Game("va"),  # "〇〇をプレイ中"の"〇〇"を設定,
)

# 起動時に自動的に動くメソッド
@bot.event
async def on_ready():
    # num_resultsをグローバル変数として扱う
    global num_results
    # num_resultsを取得
    url = "http://192.168.10.2/api/count"
    while True:
        try:
            response = requests.get(url)
            break
        except:
            print()
            time.sleep(5)
    data = response.json()
    num_results = data["num_results"]
    # 起動すると、実行したターミナルに"Hello!"と表示される
    print("Hello!")


# pingコマンドを実装
@bot.command(name="ping", description="pingを返します")
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond(f"pong to {ctx.author.mention}")

@tasks.loop(seconds=10)
# 192.168.20.2/api/countにGETリクエストを送信
async def get_ippai():
    global num_results
    url = "http://192.168.20.2/api/count"
#     return {
#     "status": "success",
#     "num_results": f"{len(question)}",
# }
    try:
        response = requests.get(url)
    except:
        return
    data = response.json()
    if num_results != data["num_results"]:
        num_results = data["num_results"]
        await bot.get_channel(1216655400418545734).send(f"新しい質問が追加されました！\n現在の質問数：{num_results}")
    else:
        return
                
get_ippai.start()

# Botを起動
bot.run(token)