import discord
import ctftime
import random
from discord.ext import commands, tasks
from datetime import datetime

# Token generated from https://discord.com/developers/applications
# Keep this private, if exposed generate new one 
TOKEN = ''
# Bot channel ID was grabbed from Settings > Appearance > Developer Mode (On). Afterwards, right click on desired channel to copy ID
BOT_CHANNEL = 0
bot = commands.Bot(command_prefix = '!')

# When bot is ready
@bot.event
async def on_ready():
	print('Starting loop task')
	update_channel.start()
	print('pwnbot is now ready for commands.')


@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.errors.CommandNotFound):
		await ctx.send(':robot:  *That command does not exist.\nTry:* `!help`')
		return
	raise error


# removes default help command
bot.remove_command('help');
# contex is passed in automatically
@bot.command()
async def help(ctx):
	await ctx.send(
		'```\n' +
		'---------------------------------- Help ----------------------------------\n\n' +

		'Usage: !<command>\n\n' +

		'Event Commands:\n' +
		' * !events - Displays ongoing ctf events within the week.\n' +
		' * !events all - Displays ctf events for the past and next week.\n' +
		' * !events next - Displays upcoming ctf events for next week.\n' +
		' * !events past - Displays finished ctf events from the past week.\n\n' +

		'Clear Commands:\n' +
		' * !clear - Clears the last 20 messages from pwnbot in current channel.\n' +
		' * !clear all - Clears all messages from pwnbot in current channel.\n' +
		' * !clear last - Clears last message from pwnbot in current channel.\n\n' +

		'Util Commands:\n' +
		' * !ping - Checks the latency for pwnbot with date/time\n\n' +

		'Misc Commands:\n' +
		' * !celebrate - Celebration!!\n' +
		' * !facepalm - Sometimes you just have to facepalm ...\n\n' +

		'--------------------------------------------------------------------------\n' +
		'```'
	)


@bot.command()
async def events(ctx, arg=None):
	embed_msgs = []

	current_time = int(datetime.now().timestamp())
	SEVEN_DAYS = ctftime.days_to_secs(7)

	if arg == 'all':
		start = current_time - SEVEN_DAYS
		finish = current_time + SEVEN_DAYS
		# checks previous json events to see if its the same as the newly fetched events
		embed_msgs = ctftime.get_events(start, finish)

		# if there are new events, embed the new events and send to current channel
		if len(embed_msgs) == 0:
			await ctx.send(':robot:  *There are no events happening from last week to next week.*')
			return

	elif arg == 'next':
		start = current_time
		finish = current_time + SEVEN_DAYS
		embed_msgs = ctftime.get_events(start, finish, status='upcoming')

		if len(embed_msgs) == 0:
			await ctx.send(':robot:  *There are no upcoming events next week.*')
			return

	elif arg == 'past':
		start = current_time - SEVEN_DAYS
		finish = current_time
		embed_msgs = ctftime.get_events(start, finish, status='finished')

		if len(embed_msgs) == 0:
			await ctx.send(':robot:  *There are no finished events from last week.*')
			return

	else:
		start = current_time - SEVEN_DAYS
		finish = current_time + SEVEN_DAYS
		embed_msgs = ctftime.get_events(start, finish, status='update')

		if len(embed_msgs) == 0:
			await ctx.send(':robot:  **There are no ongoing events.**')
			return

	for embed in embed_msgs:
		await ctx.send(embed=embed)


@bot.command()
async def clear(ctx, arg=None):
	if arg == 'all':
		await ctx.channel.purge(limit=200, check=is_bot)
	if arg == 'last':
		await ctx.channel.purge(limit=1, check=is_bot)
	else:
		await ctx.channel.purge(limit=20, check=is_bot)


@bot.command()
async def ping(ctx):
	await ctx.send(f"Pong!\n[**{round(bot.latency * 1000)}ms**]: *Current date/time: {datetime.now()}*")


@bot.command()
async def celebrate(ctx):
	await ctx.send('\o/ :confetti_ball: :tada:')


@bot.command()
async def facepalm(ctx):
	await ctx.send(':man_facepalming:')


@bot.command()
async def pwnbot(ctx):
	#-5 removes #0000 at the end of username for discord
	user = str(ctx.author)[:-5]

	responses = [
		f"*Oh my! You caught me by surprise! How can I help, {user}?*",
		f"**BRUTEFORCE!**",
		f"*get pwned {user}* :computer:",
		f"*You must be bored. Check out: `!events` for current ctf events :robot:*",
		f"*pwnbot at your service!*",
		f"!{user}",
		f"*-thinks of a quirky comment-*",
		f"*What do you want?*",
		f"*-currently sleeping-*",
		f"*At your service, {user}!*",
		f"*'UNO is the best'* -pwnbot 2020",
		f":robot: ||*NTk2Zjc1MjA2ZDc1NzM3NDIwNjI2NTIwNzY2NTcyNzkyMDYzNmM2NTc2NjU3MjJlMjA0ZDc5MjA2ZTYxNmQ2NTIwNjk3MzIwNzA3NzZlNjI2Zjc0MjEyMDNhMjkK*||",
		f"*Beware of this command!! :robot:*",
		f"*Ah yes, some human interaction. How can I assist you?*"
	]

	await ctx.send(random.choice(responses))


# checks if message is from bot or a command to bot. helper for clear command
def is_bot(msg):
	return msg.author == bot.user or msg.content[0] == '!' 


def diff_events(curr, prev):
	if len(curr) != len(prev):
		return True

	for curr_event, prev_event in zip(curr, prev):
		if curr_event.title != prev_event.title:
			return True
	
	return False


# sends update to #bot-channel with embedded new events. if events are the same as the old update,
# dont update. checks every 30 minutes for new content
prev_update = ''
bot_msg = ''
@tasks.loop(minutes=30)
async def update_channel():
	global curr_events
	channel = bot.get_channel(BOT_CHANNEL)
	SEVEN_DAYS = ctftime.days_to_secs(7)
	current_time = int(datetime.now().timestamp())

	start = current_time - SEVEN_DAYS
	finish = current_time + SEVEN_DAYS

	curr_events = ctftime.get_events(start, finish, status='update')

	# prev_events is used to self check bot for new events
	global prev_update, bot_msg

	if prev_update == '' or diff_events(curr_events, prev_update):
		prev_update = curr_events

		if len(curr_events) == 0 and bot_msg == '':
			bot_msg = ':robot:  *There are no ongoing/upcoming events. I will update this channel when I see new events.*'
			await channel.send(bot_msg)
		
		for embed in curr_events:
			await channel.send(embed=embed)
			bot_msg = ''


bot.run(TOKEN)