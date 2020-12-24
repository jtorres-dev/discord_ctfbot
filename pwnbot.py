import discord
import ctftime
import random
from discord.ext import commands, tasks
from datetime import datetime

# Token generated from https://discord.com/developers/applications
# Keep this private, if exposed generate new one 
TOKEN = "INSERT TOKEN HERE"
# Bot channel ID was grabbed from Settings > Appearance > Developer Mode (On). Afterwards, right click on desired channel to copy ID
BOT_CHANNEL = 0

# previous jsons for commands !events {all|next|past}
prev_events = ""
prev_events_all = ""
prev_events_next = ""
prev_events_past = ""

# previous embeds update used for !events if update happened
prev_embed = []
prev_embed_update = []
prev_embed_all = []
prev_embed_next = []
prev_embed_past = []

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
	global prev_events_all, prev_embed_all
	global prev_events_next, prev_embed_next
	global prev_events_past, prev_embed_past
	global prev_embed
	
	if arg == "all":
		SEVEN_DAYS = ctftime.days_to_secs(7)
		start = int(datetime.now().timestamp()) - SEVEN_DAYS
		finish = int(datetime.now().timestamp()) + SEVEN_DAYS

		# checks prev events to see if its the same as the new events	
		new_events = get_new_events(start, finish, prev_events_all)

		# if there are new events, embed the new events and send to current channel
		if new_events != "":
			embed_msgs = ctftime.embed_events(new_events)
			if len(embed_msgs) == 0:
				await ctx.send(":robot:  *There are no events happening from last week to next week.*")
			else:
				for embed in embed_msgs:
					await ctx.send(embed=embed)
			
				prev_events_all = new_events
				prev_embed_all = embed_msgs
		else:
			for embed in prev_embed_all:
				await ctx.send(embed=embed)

	elif arg == "next":
		start = int(datetime.now().timestamp())
		finish = int(datetime.now().timestamp()) + ctftime.days_to_secs(7)
		
		new_events = get_new_events(start, finish, prev_events_next)
		
		if new_events != "":
			embed_msgs = ctftime.embed_events(new_events, status="upcoming")
			if len(embed_msgs) == 0:
				await ctx.send(":robot:  *There are no upcoming events next week.*")
			else:
				for embed in embed_msgs:
					await ctx.send(embed=embed)
			
				prev_events_next = new_events
				prev_embed_next = embed_msgs
		
		else:
			for embed in prev_embed_next:
				await ctx.send(embed=embed)

	elif arg == "past":
		start = int(datetime.now().timestamp()) - ctftime.days_to_secs(7)
		finish = int(datetime.now().timestamp())
		
		new_events = get_new_events(start, finish, prev_events_past)
		
		if new_events != "":
			embed_msgs = ctftime.embed_events(new_events, status="finished")
			if len(embed_msgs) == 0:
				await ctx.send(":robot:  *There are no finished events from last week.*")
			else:
				for embed in embed_msgs:
					await ctx.send(embed=embed)
			
				prev_events_past = new_events
				prev_embed_past = embed_msgs
		
		else:
			for embed in prev_embed_past:
				await ctx.send(embed=embed)

	else:
		SEVEN_DAYS = ctftime.days_to_secs(7)
		start = int(datetime.now().timestamp()) - SEVEN_DAYS
		finish = int(datetime.now().timestamp()) + SEVEN_DAYS

		new_events = get_new_events(start, finish, prev_events_all)

		if len(prev_embed) <= 1:
			embed_msgs = ctftime.embed_events(new_events, status="ongoing")
			if len(embed_msgs) == 0:
				await ctx.send(":robot:  **There are no ongoing events.**")
			else:
				for embed in embed_msgs:
					await ctx.send(embed=embed)
			
				prev_embed = embed_msgs
		
		else:
			for embed in prev_embed:
				await ctx.send(embed=embed)




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
@tasks.loop(seconds=10)
async def update_channel():
	# prev_events is used to self check bot for new events
	# prev_embed_all is used for the `!event all` command (same as events used here)
	global prev_events, prev_embed_update, prev_embed_all

	channel = bot.get_channel(BOT_CHANNEL)
	SEVEN_DAYS = ctftime.days_to_secs(7)

	start = int(datetime.now().timestamp()) - SEVEN_DAYS
	finish = int(datetime.now().timestamp()) + SEVEN_DAYS
	
	new_events = get_new_events(start, finish, prev_events)
	
	if new_events != "":
		embed_msgs = ctftime.embed_events(new_events, status="ongoing")
		embed_msgs += ctftime.embed_events(new_events, status="upcoming")

		if len(embed_msgs) == 0:
			await channel.send(":robot:  *There are no ongoing/upcoming events. I will update this channel when I see new events.*")
		
		else:
			# double check for same embeds
			if diff_embeds(prev_embed_update, embed_msgs):
				for embed in embed_msgs:
					await channel.send(embed=embed)
			
				prev_embed = embed_msgs
				prev_embed_update = embed_msgs
				prev_events = new_events



def get_new_events(start, finish, prev_events):
	curr_events = ctftime.get_events(start, finish)
	if curr_events == prev_events:
		return ""

	return curr_events


def diff_embeds(prev_embeds, curr_embeds):
	if len(prev_embeds) != len(curr_embeds):
		return True
	else:
		for prev, curr in zip(prev_embeds, curr_embeds):
			if prev.title != curr.title:
				return True

		return False



bot.run(TOKEN)
