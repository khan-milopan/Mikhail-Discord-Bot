import discord
from discord.ext import commands

class botSay(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot
    
    async def recentCtx(self, ctx:discord.Message):
        twoCtx = [msg async for msg in ctx.channel.history(limit=2)]
        if len(twoCtx) > 1:
            return f"{twoCtx[1].content}"
        else:
            return " "

    @commands.cog.listener()
    async def on_message(self, ctx:discord.Message):
        sayInfo = f"\n-# Request by <@{ctx.author.id}>."
        if not ctx.author.bot and ctx.content.lower().startswith("m:"):
            if ctx.reference:
                ctxReply = await ctx.channel.fetch_message(ctx.reference.message_id)
                if ctx.content == "m:":
                    if ctxReply.reference:
                        ctxReply2 = await ctx.channel.fetch_message(ctxReply.reference.message_id)
                        await ctxReply2.reply(f"{ctxReply.content}{sayInfo}")
                    else:
                        await ctxReply.channel.send(f"{ctxReply.content}{sayInfo}")
                    await ctx.delete()
                else:
                    await ctxReply.reply(f"{ctx.content[2:]}{sayInfo}")
            else:
                if ctx.content == "m:":
                    previousCtx = await self.recentCtx(ctx)
                    if previousCtx != " ":
                        await ctx.channel.send(f"{previousCtx}{sayInfo}")
                        await ctx.delete()
                else:
                    await ctx.channel.send(f"{ctx.content[2:]}{sayInfo}")


def setup(bot):
    bot.add_cog(botSay(bot))
