from googletrans import Translator
from currency_converter import CurrencyConverter
import discord
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
from datetime import datetime
import asyncio

red = discord.Colour.from_rgb(0, 100, 0)

translator = Translator()
c = CurrencyConverter()

async def log(bot, command, ctx):
    logs = bot.get_channel(769906608318316594)
    embed_msg = discord.Embed(title=f"Command '{command}' used by {str(ctx.message.author)}.", description=f"**Text:**\n{ctx.message.content}\n\n**User ID:**\n{ctx.author.id}\n\n**Full Details:**\n{str(ctx.message)}", colour=red, timestamp=datetime.utcnow())
    await logs.send(embed=embed_msg)

class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='translates text from one language into another.')
    @commands.cooldown(2, 20, commands.BucketType.member)
    async def translate(self, ctx, source_language, destination_language, *, text):
        await log(self.bot, 'translate', ctx)
        try:
            translation = translator.translate(text, src=source_language, dest=destination_language)
            embed_msg = discord.Embed(title="Translation Result", description=translation.text, colour=red,
                                      timestamp=datetime.utcnow())
            embed_msg.set_footer(text='Powered by Google Translate')
            await ctx.send(embed=embed_msg)
        except ValueError:
            embed_msg = discord.Embed(title="Invalid language!",
                                      description="Please use `,languages` for a list of supported languages.\nCommand usage: `,translate (language 1) (language 2) (text)`",
                                      colour=red,
                                      timestamp=datetime.utcnow())
            embed_msg.set_footer(text='Powered by PCPartPicker')
            await ctx.send(embed=embed_msg)


    @commands.command(description='DMs user a list of supported languages for the ,translate command.')
    async def languages(self, ctx):
        embed_msg = discord.Embed(title="Supported Languages",
                                  description="af: afrikaans\nsq: albanian\nam: amharic\nar: arabic\nhy: armenian\naz: azerbaijani\neu: basque\nbe: belarusian\nbn: bengali\nbs: bosnian\nbg: bulgarian\nca: catalan\nceb: cebuano\nny: chichewa\nzh-cn: chinese (simplified)\nzh-tw: chinese (traditional)\nco: corsican\nhr: croatian\ncs: czech\nda: danish\nnl: dutch\nen: english\neo: esperanto\net: estonian\ntl: filipino\nfi: finnish\nfr: french\nfy: frisian\ngl: galician\nka: georgian\nde: german\nel: greek\ngu: gujarati\nht: haitian creole\nha: hausa\nhaw: hawaiian\niw: hebrew\nhi: hindi\nhmn: hmong\nhu: hungarian\nis: icelandic\nig: igbo\nid: indonesian\nga: irish\nit: italian\nja: japanese\njw: javanese\nkn: kannada\nkk: kazakh\nkm: khmer\nko: korean\nku: kurdish (kurmanji)\nky: kyrgyz\nlo: lao\nla: latin\nlv: latvian\nlt: lithuanian\nlb: luxembourgish\nmk: macedonian\nmg: malagasy\nms: malay\nml: malayalam\nmt: maltese\nmi: maori\nmr: marathi\nmn: mongolian\nmy: myanmar (burmese)\nne: nepali\nno: norwegian\nps: pashto\nfa: persian\npl: polish\npt: portuguese\npa: punjabi\nro: romanian\nru: russian\nsm: samoan\ngd: scots gaelic\nsr: serbian\nst: sesotho\nsn: shona\nsd: sindhi\nsi: sinhala\nsk: slovak\nsl: slovenian\nso: somali\nes: spanish\nsu: sundanese\nsw: swahili\nsv: swedish\ntg: tajik\nta: tamil\nte: telugu\nth: thai\ntr: turkish\nuk: ukrainian\nur: urdu\nuz: uzbek\nvi: vietnamese\ncy: welsh\nxh: xhosa\nyi: yiddish\nyo: yoruba\nzu: zulu\nfil: filipino\nhe: hebrew",
                                  colour=red,
                                  timestamp=datetime.utcnow())
        await ctx.author.send(embed=embed_msg)
        await ctx.message.add_reaction('📨')

    @commands.command(description='converts from one currency to another.')
    @commands.cooldown(2, 20, commands.BucketType.member)
    async def convert(self, ctx, amount, source_curr, destination_curr):
        await log(self.bot, 'convert', ctx)
        try:
            conversion = c.convert(amount, source_curr.upper(), destination_curr.upper())
            embed_msg = discord.Embed(title="Conversion Result",
                                      description=f"**{amount}** {source_curr.upper()} is **{round(conversion, 2)}** {destination_curr.upper()}.",
                                      colour=red, timestamp=datetime.utcnow())
            await ctx.send(embed=embed_msg)
        except ValueError:
            embed_msg = discord.Embed(title="Invalid currency or number!",
                                      description="Please use `,currencies` for a list of supported currencies.\nCommand usage: `,convert (amount) (currency 1) (currency 2)`",
                                      colour=red,
                                      timestamp=datetime.utcnow())
            await ctx.send(embed=embed_msg)


    @commands.command(description='DMs user a list of supported currencies for the ,convert command.')
    async def currencies(self, ctx):
        embed_msg = discord.Embed(title="Supported Currencies",
                                  description="AUD Australian dollar\nBGN Bulgarian lev\nBRL Brazilian real\nCAD Canadian dollar\nCHF Swiss franc\nCNY Chinese yuan renminbi\nCZK Czech koruna\nDKK Danish krone\nGBP Pound sterling\nHKD Hong Kong dollar\nHRK Croatian kuna\nHUF Hungarian forint\nIDR Indonesian rupiah\nILS Israeli shekel\nINR Indian rupee\nISK Icelandic krona\nJPY Japanese yen\nKRW South Korean won\nMXN Mexican peso\nMYR Malaysian ringgit\nNOK Norwegian krone\nNZD New Zealand dollar\nPHP Philippine peso\nPLN Polish zloty\nRON Romanian leu\nRUB Russian rouble\nSEK Swedish krona\nSGD Singapore dollar\nTHB Thai baht\nTRY Turkish lira\nUSD US dollar\nZAR South African rand",
                                  colour=red,
                                  timestamp=datetime.utcnow())
        await ctx.author.send(embed=embed_msg)
        await ctx.message.add_reaction('📨')

def setup(bot):
    bot.add_cog(Utility(bot))