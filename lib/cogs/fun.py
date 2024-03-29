import io
import json
import sys
import time
import urllib.request
from random import choice, randint
from typing import Optional

import aiohttp
import discord
import googletrans
import requests
from aiohttp import request
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown

sys.path.append("/Uusi kansio\Lib\site-packages")


class Fun(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="hello", aliases=["hi"])
	async def say_hello(self, ctx):
		await ctx.send(
			f"{choice(('Hi', 'Henlo', 'Sup', 'Heyo', 'Hello', 'Hey', 'Hallo', 'Namaste', 'Hiya', 'Wassah'))} {ctx.author.mention}!")

	@command(name="dice", aliases=["roll"])
	@cooldown(1, 5, BucketType.user)
	async def roll_dice(self, ctx, die_string: str):
		dice, value = (int(term) for term in die_string.split("d"))
		if dice <= 25:
			rolls = [randint(1, value) for i in range(dice)]
			await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")
		else:
			await ctx.send("I can't roll that many dices, please try a lower number.")


	@command(name="slap", aliases=['bonk', 'hit'])
	@cooldown(3, 10, BucketType.user)
	async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "no reason"):
		await ctx.send(f"{ctx.author.mention} slapped {member.mention} {reason}!")


	@slap_member.error
	async def slap_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Please mention a member you want to slap.")

	@slap_member.error
	async def slap_error2(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send("I can't find the member mentioned.")


	# @command(name="dog-fact")
	# async def dog_fact(self, ctx):
	# 	URL = "https://some-random-api.ml/facts/dog"

	# 	async with request("GET", URL) as response:
	# 		if response.status == 200:
	# 			data = await response.json()

	# 			await ctx.send(data["fact"])

	# 		else:
	# 			await ctx.send(f"API returned a {response.status} status.")


	# @command(name="cat-fact")
	# async def cat_fact(self, ctx):
	# 	URL = "https://some-random-api.ml/facts/cat"

	# 	async with request("GET", URL) as response:
	# 		if response.status == 200:
	# 			data = await response.json()

	# 			await ctx.send(data["fact"])

	# 		else:
	# 			await ctx.send(f"API returned a {response.status} status.")


	# @command(name="fox-fact")
	# async def fox_fact(self, ctx):
	# 	URL = "https://some-random-api.ml/facts/fox"

	# 	async with request("GET", URL) as response:
	# 		if response.status == 200:
	# 			data = await response.json()

	# 			await ctx.send(data["fact"])

	# 		else:
	# 			await ctx.send(f"API returned a {response.status} status.")

	@command(name="fact")
	async def animal_fact(self, ctx, animal: str):
		if animal in ("dog", "cat", "koala", "panda", "fox", "bird"):
			fact_url = f"https://some-random-api.ml/facts/{animal}"
			image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

			async with request("GET", image_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()
					image_link = data["link"]

				else:
					image_link = None

			async with request("GET", fact_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()

					embed = Embed(title=f"{animal.title()} fact",
								  description=data['fact'],
								  color=ctx.author.color)

					if image_link is not None:
						embed.set_image(url=image_link)
					await ctx.send(embed=embed)

				else:
					await ctx.send(f"API returned a {response.status} status.")

		else:
			await ctx.send("No facts are available for that animal.")


	@command(name="dog")
	async def dog_img(self, ctx):
		URL = "https://some-random-api.ml/img/dog"

		async with request("GET", URL) as response:
			if response.status == 200:
				data = await response.json()

				await ctx.send(data["link"])

			else:
				await ctx.send(f"API returned a {response.status} status.")


	@command(name="gay")
	@cooldown(1, 5, BucketType.user)
	async def gay(self, ctx, *, member: discord.Member = None):
		if not member:
			member = ctx.author
		session = aiohttp.ClientSession()
		async with session.get(f"https://some-random-api.ml/canvas/gay?avatar={member.avatar_url_as(format='jpg')}") as r:
			if r.status != 200:
				return await ctx.send("API is down, please try again later.")
				await session.close()
			else:
				data = io.BytesIO(await r.read())
				await ctx.send(file=discord.File(data, 'gay.jpg'))
				await session.close()


	@gay.error
	async def gay_handler(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Please mention a member to apply the overlay to.")


	@command(name="invert")
	@cooldown(1, 5, BucketType.user)
	async def invert(self, ctx, *, member: discord.Member = None):
		if not member:
			member = ctx.author
		session = aiohttp.ClientSession()
		async with session.get(
				f"https://some-random-api.ml/canvas/invert?avatar={member.avatar_url_as(format='jpg')}") as r:
			if r.status != 200:
				return await ctx.send("API is down, please try again later.")
				await session.close()
			else:
				data = io.BytesIO(await r.read())
				await ctx.send(file=discord.File(data, 'invert.jpg'))
				await session.close()


	@invert.error
	async def invert_handler(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Please mention a member to apply the overlay to.")


	@command(name="joke")
	async def joke(self, ctx):
		URL = 'https://official-joke-api.appspot.com/jokes/random'

		async with request("GET", URL, headers={}) as response:
			if response.status == 200:
				data = await response.json()
				await ctx.send(data['setup'] + '\n' + data['punchline'])

			else:
				await ctx.send(f"API returned a {response.status} status.")



	@command(name="weather")
	async def weather(self, ctx, inputC):
		countr = {
			'AD': 'Andorra',
			'AE': 'United Arab Emirates',
			'AF': 'Afghanistan',
			'AG': 'Antigua & Barbuda',
			'AI': 'Anguilla',
			'AL': 'Albania',
			'AM': 'Armenia',
			'AN': 'Netherlands Antilles',
			'AO': 'Angola',
			'AQ': 'Antarctica',
			'AR': 'Argentina',
			'AS': 'American Samoa',
			'AT': 'Austria',
			'AU': 'Australia',
			'AW': 'Aruba',
			'AZ': 'Azerbaijan',
			'BA': 'Bosnia and Herzegovina',
			'BB': 'Barbados',
			'BD': 'Bangladesh',
			'BE': 'Belgium',
			'BF': 'Burkina Faso',
			'BG': 'Bulgaria',
			'BH': 'Bahrain',
			'BI': 'Burundi',
			'BJ': 'Benin',
			'BM': 'Bermuda',
			'BN': 'Brunei Darussalam',
			'BO': 'Bolivia',
			'BR': 'Brazil',
			'BS': 'Bahama',
			'BT': 'Bhutan',
			'BU': 'Burma (no longer exists)',
			'BV': 'Bouvet Island',
			'BW': 'Botswana',
			'BY': 'Belarus',
			'BZ': 'Belize',
			'CA': 'Canada',
			'CC': 'Cocos (Keeling) Islands',
			'CF': 'Central African Republic',
			'CG': 'Congo',
			'CH': 'Switzerland',
			'CI': 'Côte D\'ivoire (Ivory Coast)',
			'CK': 'Cook Iislands',
			'CL': 'Chile',
			'CM': 'Cameroon',
			'CN': 'China',
			'CO': 'Colombia',
			'CR': 'Costa Rica',
			'CS': 'Czechoslovakia (no longer exists)',
			'CU': 'Cuba',
			'CV': 'Cape Verde',
			'CX': 'Christmas Island',
			'CY': 'Cyprus',
			'CZ': 'Czech Republic',
			'DD': 'German Democratic Republic (no longer exists)',
			'DE': 'Germany',
			'DJ': 'Djibouti',
			'DK': 'Denmark',
			'DM': 'Dominica',
			'DO': 'Dominican Republic',
			'DZ': 'Algeria',
			'EC': 'Ecuador',
			'EE': 'Estonia',
			'EG': 'Egypt',
			'EH': 'Western Sahara',
			'ER': 'Eritrea',
			'ES': 'Spain',
			'ET': 'Ethiopia',
			'FI': 'Finland',
			'FJ': 'Fiji',
			'FK': 'Falkland Islands (Malvinas)',
			'FM': 'Micronesia',
			'FO': 'Faroe Islands',
			'FR': 'France',
			'FX': 'France, Metropolitan',
			'GA': 'Gabon',
			'GB': 'United Kingdom (Great Britain)',
			'GD': 'Grenada',
			'GE': 'Georgia',
			'GF': 'French Guiana',
			'GH': 'Ghana',
			'GI': 'Gibraltar',
			'GL': 'Greenland',
			'GM': 'Gambia',
			'GN': 'Guinea',
			'GP': 'Guadeloupe',
			'GQ': 'Equatorial Guinea',
			'GR': 'Greece',
			'GS': 'South Georgia and the South Sandwich Islands',
			'GT': 'Guatemala',
			'GU': 'Guam',
			'GW': 'Guinea-Bissau',
			'GY': 'Guyana',
			'HK': 'Hong Kong',
			'HM': 'Heard & McDonald Islands',
			'HN': 'Honduras',
			'HR': 'Croatia',
			'HT': 'Haiti',
			'HU': 'Hungary',
			'ID': 'Indonesia',
			'IE': 'Ireland',
			'IL': 'Israel',
			'IN': 'India',
			'IO': 'British Indian Ocean Territory',
			'IQ': 'Iraq',
			'IR': 'Islamic Republic of Iran',
			'IS': 'Iceland',
			'IT': 'Italy',
			'JM': 'Jamaica',
			'JO': 'Jordan',
			'JP': 'Japan',
			'KE': 'Kenya',
			'KG': 'Kyrgyzstan',
			'KH': 'Cambodia',
			'KI': 'Kiribati',
			'KM': 'Comoros',
			'KN': 'St. Kitts and Nevis',
			'KP': 'Korea, Democratic People\'s Republic of',
			'KR': 'Korea, Republic of',
			'KW': 'Kuwait',
			'KY': 'Cayman Islands',
			'KZ': 'Kazakhstan',
			'LA': 'Lao People\'s Democratic Republic',
			'LB': 'Lebanon',
			'LC': 'Saint Lucia',
			'LI': 'Liechtenstein',
			'LK': 'Sri Lanka',
			'LR': 'Liberia',
			'LS': 'Lesotho',
			'LT': 'Lithuania',
			'LU': 'Luxembourg',
			'LV': 'Latvia',
			'LY': 'Libyan Arab Jamahiriya',
			'MA': 'Morocco',
			'MC': 'Monaco',
			'MD': 'Moldova, Republic of',
			'MG': 'Madagascar',
			'MH': 'Marshall Islands',
			'ML': 'Mali',
			'MN': 'Mongolia',
			'MM': 'Myanmar',
			'MO': 'Macau',
			'MP': 'Northern Mariana Islands',
			'MQ': 'Martinique',
			'MR': 'Mauritania',
			'MS': 'Monserrat',
			'MT': 'Malta',
			'MU': 'Mauritius',
			'MV': 'Maldives',
			'MW': 'Malawi',
			'MX': 'Mexico',
			'MY': 'Malaysia',
			'MZ': 'Mozambique',
			'NA': 'Namibia',
			'NC': 'New Caledonia',
			'NE': 'Niger',
			'NF': 'Norfolk Island',
			'NG': 'Nigeria',
			'NI': 'Nicaragua',
			'NL': 'Netherlands',
			'NO': 'Norway',
			'NP': 'Nepal',
			'NR': 'Nauru',
			'NT': 'Neutral Zone (no longer exists)',
			'NU': 'Niue',
			'NZ': 'New Zealand',
			'OM': 'Oman',
			'PA': 'Panama',
			'PE': 'Peru',
			'PF': 'French Polynesia',
			'PG': 'Papua New Guinea',
			'PH': 'Philippines',
			'PK': 'Pakistan',
			'PL': 'Poland',
			'PM': 'St. Pierre & Miquelon',
			'PN': 'Pitcairn',
			'PR': 'Puerto Rico',
			'PT': 'Portugal',
			'PW': 'Palau',
			'PY': 'Paraguay',
			'QA': 'Qatar',
			'RE': 'Réunion',
			'RO': 'Romania',
			'RU': 'Russian Federation',
			'RW': 'Rwanda',
			'SA': 'Saudi Arabia',
			'SB': 'Solomon Islands',
			'SC': 'Seychelles',
			'SD': 'Sudan',
			'SE': 'Sweden',
			'SG': 'Singapore',
			'SH': 'St. Helena',
			'SI': 'Slovenia',
			'SJ': 'Svalbard & Jan Mayen Islands',
			'SK': 'Slovakia',
			'SL': 'Sierra Leone',
			'SM': 'San Marino',
			'SN': 'Senegal',
			'SO': 'Somalia',
			'SR': 'Suriname',
			'ST': 'Sao Tome & Principe',
			'SU': 'Union of Soviet Socialist Republics (no longer exists)',
			'SV': 'El Salvador',
			'SY': 'Syrian Arab Republic',
			'SZ': 'Swaziland',
			'TC': 'Turks & Caicos Islands',
			'TD': 'Chad',
			'TF': 'French Southern Territories',
			'TG': 'Togo',
			'TH': 'Thailand',
			'TJ': 'Tajikistan',
			'TK': 'Tokelau',
			'TM': 'Turkmenistan',
			'TN': 'Tunisia',
			'TO': 'Tonga',
			'TP': 'East Timor',
			'TR': 'Turkey',
			'TT': 'Trinidad & Tobago',
			'TV': 'Tuvalu',
			'TW': 'Taiwan, Province of China',
			'TZ': 'Tanzania, United Republic of',
			'UA': 'Ukraine',
			'UG': 'Uganda',
			'UM': 'United States Minor Outlying Islands',
			'US': 'United States of America',
			'UY': 'Uruguay',
			'UZ': 'Uzbekistan',
			'VA': 'Vatican City State (Holy See)',
			'VC': 'St. Vincent & the Grenadines',
			'VE': 'Venezuela',
			'VG': 'British Virgin Islands',
			'VI': 'United States Virgin Islands',
			'VN': 'Viet Nam',
			'VU': 'Vanuatu',
			'WF': 'Wallis & Futuna Islands',
			'WS': 'Samoa',
			'YD': 'Democratic Yemen (no longer exists)',
			'YE': 'Yemen',
			'YT': 'Mayotte',
			'YU': 'Yugoslavia',
			'ZA': 'South Africa',
			'ZM': 'Zambia',
			'ZR': 'Zaire',
			'ZW': 'Zimbabwe',
			'ZZ': 'Unknown or unspecified country',
		}

		res = requests.get(
			"http://api.openweathermap.org/data/2.5/weather?q=" + inputC + "&appid=ad8c24a502acf15769ead04a4966132b&units=metric")
		resJson = res.json()
		des = resJson["weather"][0]["description"]
		icon = resJson["weather"][0]["icon"]
		iconUrl = "http://openweathermap.org/img/wn/" + str(icon) + "@2x.png"
		temp = resJson["main"]["temp"]
		feelsLike = resJson["main"]["feels_like"]
		hum = resJson["main"]["humidity"]
		wind = resJson["wind"]["speed"]
		sunr = resJson["sys"]["sunrise"]
		suns = resJson["sys"]["sunset"]
		count = resJson["sys"]["country"]
		srtime = time.ctime(sunr)
		sstime = time.ctime(suns)
		lon = resJson["coord"]["lon"]
		lat = resJson["coord"]["lat"]
		mapUrl = "https://www.google.com/maps/search/?api=1&query=" + str(lat) + "," + str(lon)

		em = discord.Embed(title=inputC, description=countr[count], color=0x0000ff)
		em.add_field(name="Description", value=des)
		em.add_field(name="Temperature/Feels like", value=str(temp) + "°C/" + str(feelsLike) + "ºC")
		em.add_field(name="Humidity", value=str(hum) + "%")
		em.add_field(name="Wind Speed", value=str(wind) + "m/s")
		em.add_field(name="Sunrise", value=srtime)
		em.add_field(name="Sunset", value=sstime)
		em.add_field(name="Map", value=mapUrl)
		em.set_thumbnail(url=iconUrl)
		await ctx.send(embed=em)


	@Cog.listener()
	async def on_ready(self):
		print("Fun cog ready!")


	@command(name="say")
	@commands.is_owner()
	async def say(self, ctx, *, msg):
		await ctx.message.delete()
		await ctx.send("{}".format(msg))


	@say.error
	async def say_handler(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Please add a message.")


	@command(name="translate", aliases=['tr'])
	@cooldown(3, 5, BucketType.user)
	async def translate(self, ctx, lang_to, *args):
		lang_to = lang_to.lower()
		if lang_to not in googletrans.LANGUAGES and lang_to not in googletrans.LANGCODES:
			raise commands.BadArgument("Invalid language to translate text to")

		text = ' '.join(args)
		translator = googletrans.Translator()
		text_translated = translator.translate(text, dest=lang_to).text
		await ctx.send(text_translated)


	@command(name="xchange", aliases=['currency'])
	@cooldown(3, 5, BucketType.user)
	async def xchange(self, ctx, newBase="EUR"):
		currencies = ["CAD", "HKD", "ISK", "PHP", "DKK", "HUF", "CZK", "AUD", "RON", "SEK", "IDR", "INR", "BRL", "RUB",
					"HRK", "JPY", "THB", "CHF", "SGD", "PLN", "BGN", "TRY", "CNY", "NOK", "NZD", "ZAR", "USD", "MXN",
					"ILS", "GBP", "KRW", "MYR"]
		url = "https://api.exchangeratesapi.io/latest"
		if (newBase in currencies):
			url += "?base=" + newBase
		req = urllib.request.Request(url)
		r = urllib.request.urlopen(req).read()
		cont = json.loads(r.decode('utf-8'))
		name = "1 " + cont["base"] + " equals:"
		em = discord.Embed(title=name)
		for item in cont["rates"]:
			em.add_field(name=item, value=str(cont["rates"][item]), inline=False)
		await ctx.send(embed=em)


def setup(bot):
	bot.add_cog(Fun(bot))
