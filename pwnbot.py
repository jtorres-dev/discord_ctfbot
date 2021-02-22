import discord
import ctftime
import random
from discord.ext import commands, tasks
from datetime import datetime

# Token generated from https://discord.com/developers/applications
# Keep this private, if exposed generate new one 
TOKEN = "Nzg5Njc3MzQyMTAzODMwNTQ4.X91iVQ.5SruryxbdvWy_pxFISHZPjaeric"
# Bot channel ID was grabbed from Settings > Appearance > Developer Mode (On). Afterwards, right click on desired channel to copy ID
BOT_CHANNEL = 791460017449598986

# previous jsons for commands !events {all|next|past}
prev_events = ""
prev_events_all = ""
prev_events_next = ""
prev_events_past = ""

prev_update = ""

bot = commands.Bot(command_prefix = '!')



# When bot is ready
@bot.event
async def on_ready():
	print("Starting loop task")
	update_channel.start()
	print("pwnbot is now ready for commands.")



@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.errors.CommandNotFound):
		await ctx.send(":robot:  *That command does not exist.\nTry:* `!help`")
		return
	raise error



# removes default help command
bot.remove_command('help');
# contex is passed in automatically
@bot.command()
async def help(ctx):
	await ctx.send(
		"```\n" +
		"---------------------------------- Help ----------------------------------\n\n" +

		"Usage: !<command>\n\n" +

		"Event Commands:\n" +
		" * !events - Displays ongoing ctf events within the week.\n" +
		" * !events all - Displays ctf events for the past and next week.\n" +
		" * !events next - Displays upcoming ctf events for next week.\n" +
		" * !events past - Displays finished ctf events from the past week.\n\n" +

		"Clear Commands:\n" +
		" * !clear - Clears the last 20 messages from pwnbot in current channel.\n" +
		" * !clear all - Clears all messages from pwnbot in current channel.\n" +
		" * !clear last - Clears last message from pwnbot in current channel.\n\n" +

		"Util Commands:\n" +
		" * !ping - Checks the latency for pwnbot with date/time\n\n" +

		"Misc Commands:\n" +
		" * !celebrate - Celebration!!\n" +
		" * !facepalm - Sometimes you just have to facepalm ...\n\n" +

		"--------------------------------------------------------------------------\n" +
		"```"
	)



@bot.command()
async def events(ctx, arg=None):
	global prev_events_all, prev_events_next, prev_events_past, prev_events
	embed_msgs = []

	current_time = int(datetime.now().timestamp())
	SEVEN_DAYS = ctftime.days_to_secs(7)


	if arg == "all":
		start = current_time - SEVEN_DAYS
		finish = current_time + SEVEN_DAYS

		# checks previous json events to see if its the same as the newly fetched events	
		prev_events_all = fetch_new_events(start, finish, prev_events_all)
		embed_msgs = ctftime.embed_events(prev_events_all)

		# if there are new events, embed the new events and send to current channel
		if len(embed_msgs) == 0:
			await ctx.send(":robot:  *There are no events happening from last week to next week.*")
			return

	elif arg == "next":
		start = current_time
		finish = current_time + SEVEN_DAYS
		
		prev_events_next = fetch_new_events(start, finish, prev_events_next)
		embed_msgs = ctftime.embed_events(prev_events_next, status="upcoming")

		if len(embed_msgs) == 0:
			await ctx.send(":robot:  *There are no upcoming events next week.*")
			return

	elif arg == "past":
		start = current_time - SEVEN_DAYS
		finish = current_time

		prev_events_past = fetch_new_events(start, finish, prev_events_past)
		embed_msgs = ctftime.embed_events(prev_events_past, status="finished")

		if len(embed_msgs) == 0:
			await ctx.send(":robot:  *There are no finished events from last week.*")
			return

	else:
		start = current_time - SEVEN_DAYS
		finish = current_time + SEVEN_DAYS

		prev_events = fetch_new_events(start, finish, prev_events)
		embed_msgs = ctftime.embed_events(prev_events, status="ongoing")

		if len(embed_msgs) == 0:
			await ctx.send(":robot:  **There are no ongoing events.**")
			return


	for embed in embed_msgs:
		await ctx.send(embed=embed)



def fetch_new_events(start, finish, prev_events):
	new_events = ctftime.get_events(start, finish)

	if prev_events == "" or new_events != prev_events:
		return new_events
	
	return prev_events



# checks if message is from bot or a command to bot. helper for clear command
def is_bot(msg):
	return msg.author == bot.user or msg.content[0] == '!' 

@bot.command()
async def clear(ctx, arg=None):
	if arg == "all":
		await ctx.channel.purge(limit=200, check=is_bot)
	if arg == "last":
		await ctx.channel.purge(limit=1, check=is_bot)
	else:
		await ctx.channel.purge(limit=20, check=is_bot)



@bot.command()
async def ping(ctx):
	await ctx.send(f"Pong!\n[**{round(bot.latency * 1000)}ms**]: *Current date/time: {datetime.now()}*")



@bot.command()
async def celebrate(ctx):
	await ctx.send("\o/ :confetti_ball: :tada:")



@bot.command()
async def facepalm(ctx):
	await ctx.send(":man_facepalming:")



@bot.command()
async def pwnbot(ctx):
	#-5 removes #0000 at the end of username for discord
	user = str(ctx.author)[:-5]

	# base64 easteregg lol 
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
		f"*How can this be? a hidden command?!*",
		f'*"UNO is the best"* -pwnbot 2020',
		f":robot: ||*NTk2Zjc1MjA2ZDc1NzM3NDIwNjI2NTIwNzY2NTcyNzkyMDYzNmM2NTc2NjU3MjJlMjA0ZDc5MjA2ZTYxNmQ2NTIwNjk3MzIwNzA3NzZlNjI2Zjc0MjEyMDNhMjkK*||",
		f"*Beware of this command!! :robot:*",
		f"*Ah yes, some human interaction. How can I assist you?*"
	]

	await ctx.send(random.choice(responses))


# sends update to #bot-channel with embedded new events. if events are the same as the old update,
# dont update. checks every 1 hour for new content
@tasks.loop(hours=1)
async def update_channel():
	# prev_events is used to self check bot for new events
	# prev_embed_all is used for the `!event all` command (same as events used here)
	global prev_update

	channel = bot.get_channel(BOT_CHANNEL)
	SEVEN_DAYS = ctftime.days_to_secs(7)
	current_time = int(datetime.now().timestamp())

	start = current_time - SEVEN_DAYS
	finish = current_time + SEVEN_DAYS

	curr_events = ctftime.get_events(start, finish)

	if prev_update == "" or curr_events != prev_update:
		embed_msgs = ctftime.embed_events(curr_events, status="update")

		for embed in embed_msgs:
			await channel.send(embed=embed)

		prev_update = curr_events

		if len(embed_msgs) == 0:
			await channel.send(":robot:  *There are no ongoing/upcoming events. I will update this channel when I see new events.*")


bot.run(TOKEN)
