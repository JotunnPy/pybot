from ast import arg
from email import message
import threading
import discord

from discord.ext import commands

def check(usr):
    for role in usr.roles:
        if "mod" in role.name.lower():
            return True

class Moderation(commands.Cog):
    restrictedWords = []
    userHistory = {}
    userMPS = {}
    def __init__(self, client) -> None:
        self.client = client
    
    #Event Listener
    @commands.Cog.listener()
    async def on_message(self, msg):

        #Anti Banned Words
        for word in self.restrictedWords:
            if word in msg.content.lower():
                await msg.delete()

        #Anti Spam
        if not msg.author in self.userHistory:
            self.userHistory[msg.author] = msg.content
        else:
            if self.userHistory[msg.author] == msg.content:
                await msg.delete()

        if not msg.author in self.userMPS:
            self.userMPS[msg.author] = 1
            def resetMPS():
                self.userMPS[msg.author] = 0
                threading.Timer(1.0, resetMPS).start()
            resetMPS()
        else:
            self.userMPS[msg.author] += 1
            if self.userMPS[msg.author] > 2:
                await msg.delete()
                print(self.userMPS[msg.author])
        

    #Commands
 
    @commands.command()
    async def restrict(self, ctx, arg1):
        isMod = check(ctx.author)

        if not isMod:
            return
        self.restrictedWords.append(arg1.lower())

    @commands.command()
    async def purge(self, ctx, amm = 10):
        await ctx.channel.purge(limit = amm) 

    @commands.command()
    async def lockdown(self, ctx):
        isMod = check(ctx.author)
        if not isMod:
            return
        await ctx.channel.set_permissions(ctx.guild.default_role,send_messages=False)

        embed = discord.Embed()
        embed.title = "*CHANNEL LOCKED!*"
        embed.description = "This chennel is on lockdown."
        embed.set_image(url='https://media1.giphy.com/media/3og0IUslmf25k8Ea7C/giphy.gif')
        await ctx.channel.send(embed=embed)
    
    @commands.command()
    async def unlock(self, ctx):
        isMod = check(ctx.author)
        if not isMod:
            return
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)

        embed = discord.Embed()
        embed.title = "*CHANNEL UNLOCKED!*"
        embed.description = "Channel finally unlocked!"
        embed.set_image(url='https://cdn140.picsart.com/235961749015201.gif')

        await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(Moderation(client))