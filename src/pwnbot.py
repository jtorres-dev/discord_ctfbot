import discord
import ctftime
import random
from discord.ext import commands, tasks
from datetime import datetime

# pwnbotsecrets.py is imported from the same directory as a configuration file
from pwnbotsecrets import token, bot_channel, roles, welcomemsg

# Token generated from https://discord.com/developers/applications
# Keep this private, if exposed generate new one 
TOKEN = token

# List of roles
ROLES = roles

# Bot channel ID was grabbed from Settings > Appearance > Developer Mode (On). Afterwards, right click on desired channel to copy ID
BOT_CHANNEL = bot_channel ##### Add bot channel in config
# Prepare required Intents object 
if len(welcomemsg) > 0:
  intents = discord.Intents.default()
  intents.members = True
else:
  intents = discord.Intents.default()
  intents.members = False
bot = commands.Bot(command_prefix = '!', intents=intents)

# When bot is ready
@bot.event
async def on_ready():
  if BOT_CHANNEL > 0:
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
    ' * !ping - Checks the latency for pwnbot with date/time\n' +
    # Not sure if there should be a 'Role Commands:\n' category or if they should go here.
    ' * !roles - See a list of roles available for you to add to yourself with !role\n' +
    ' * !role - Add role to yourself to make the channels visible that were used for that past CTF\n\n' +

    'Misc Commands:\n' +
    ' * !celebrate - Celebration!!\n' +
    ' * !facepalm - Sometimes you just have to facepalm ...\n\n' +

    '--------------------------------------------------------------------------\n' +
    '```'
  )

@bot.event
async def on_member_join(member):
  if not member.bot:
    if len(welcomemsg) > 0:
      await member.send(welcomemsg)

@bot.command(name="roles")
async def _roles(ctx):
  if not len(ROLES) > 0:
    return
  s = "```Roles available, add one to make it's category visible.\n\n"
  # newlines = [roles[x] for x in range(len(roles)) if x % 5 == 0]
  for ele in ROLES:
    # if ele in newlines and ele != roles[0]:
    #     s += "\n"
    #     s += "🚩 "
    s += "🚩 %s 🚩 \n" % ele
  s += f"```\nExample usage: `{bot.command_prefix}role {ROLES[random.randint(0, len(ROLES)-1)]}`" 
  await ctx.send(s)

@bot.command(name="role")
async def _role(ctx, role: discord.Role):
  if role.name not in ROLES:
    return
  if role in ctx.author.roles:
    await ctx.author.remove_roles(role)
  else:
    await ctx.author.add_roles(role)

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

    if curr_events != None:
      for embed in curr_events:
        await channel.send(embed=embed)
        bot_msg = ''


bot.run(TOKEN)
