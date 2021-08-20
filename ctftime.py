# used for the logo color processing
# from PIL import Image
# from urllib.request import urlopen, Request
# from io import BytesIO
#
import requests, discord
from datetime import datetime
from pytz import timezone


'''
	requires: time in UTC; The start and finish time in int seconds
	param: limit is optional to choose the amount of events you would like from 1-100
	returns: a json_object containing events in between start and finish inclusively
'''
def get_events(start, finish, status=None, limit=100):
	if limit <= 0 or limit > 100:
		limit = 100

	while True:
		try:
			# header needed to prevent http error
			headers = {'user-agent': 'Mozilla/5.0'}
			json_events = requests.get(f"https://ctftime.org/api/v1/events/?limit={limit}&start={start}&finish={finish}", headers=headers).json()
			break
		
		except Exception as err:
			print(f"\nError getting events from https://ctftime.org/api/v1/events/?limit={limit}&start={start}&finish={finish}: {err}\n")

	if embed:
		return embed_events(json_events, status)
	else:
		return json_events

'''
	takes json format and cleans output to be embedded on discord.
	embed makes the output look pretty with a logo grabbed from
	ctftime.org and with the events descriptions.

	status can be 'finished', 'ongoing', 'upcoming'
'''
def embed_events(json_events, status=None):
	embed_msgs = []
	
	for event in json_events:
		start  = utc_to_cst(event['start'])
		finish = utc_to_cst(event['finish'])

		# datetime.now() is considered to be naive to timezones; forcing cst timezone to be able to compare times
		current_time = datetime.now(tz=timezone('US/Central'))
		if status == 'finished' and current_time < finish:
			continue
		if status == 'upcoming' and current_time >= start:
			continue
		if status == 'update' and current_time >= finish:
			continue
		
		# if event has closed restriction, its probably for highschool
		if event['restrictions'] == 'Open' or event['restrictions'] == 'Prequalified':
			# default discord color
			color = 0x2F3136
			desc = event['description']

			if len(desc) > 1024:
				desc = desc[:1021] + '...'

			# too slow for now, commenting out
			#
			# get logo from url to see what color shows up the most for a custom embed theme
			# note: this is very slow, on avg takes about 30-40 seconds to get all logos and update
			# there are probably enhancements to this that can make the process faster
			# if len(event["logo"]) > 20:
			# 	while True:
			# 		try:
			# 			req = Request(event["logo"], headers={'user-agent':'Mozilla/5.0'})
			# 			img_file = BytesIO(urlopen(req).read())
			# 			# resized to check img faster
			# 			img = Image.open(img_file).resize((25, 25))
			# 			color = most_used_color(img)
			# 			break

			# 		except Exception as err:
			# 			color = 0x2F3136
			# 			print(f"Error getting {event['logo']}: {err}\n")

			if event['restrictions'] == 'Prequalified':
				embed = discord.Embed(
					title = f"{event['title']} (Prequalified)",
					colour = color,
					url = event['url'],
					description = desc
				)

			else:
				embed = discord.Embed(
					title = event['title'],
					colour = color,
					url = event['url'],
					description = desc
				)

			# %B prints full month name, %I prints 12-hour instead of 24-hour, %p is for AM or PM
			start = start.strftime("%B %d, %Y \n@ %I:%M %p")
			finish = finish.strftime("%B %d, %Y \n@ %I:%M %p")

			embed.set_author(name=event['organizers'][0]['name'], icon_url=event['logo'])
			embed.set_thumbnail(url=event['logo'])
			embed.add_field(name='Participants', value=event['participants'], inline=False)
			embed.add_field(name='Start', value=start, inline=True)
			embed.add_field(name='Finish', value=finish, inline=True)
			embed.set_footer(text=event['format'])

			embed_msgs.append(embed)

	return embed_msgs


'''
  helper func to convert timezones and prettify time
  time example from ctftime: 2020-12-19T05:00:00+00:00
                   YYYY-MM-DD HH:MM:SS[+-]Z

  seems like they use ISO 8601 format: datetime.now(tzlocal()).replace(microsecond=0).isoformat()
  more info: https://www.w3resource.com/python/python-date-and-time.php
'''
def utc_to_cst(time):
	if time == None or time == '':
		return ''
	# converts to timezone aware datetime object, then converts UTC to CST
	return datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z").astimezone(timezone('US/Central'))


def days_to_secs(days):
	return days * 86400

# not used, too slow when checking all pixels in all logos
# def most_used_color(img):
# 	width, height = img.size

# 	r_total = 0
# 	g_total = 0
# 	b_total = 0

# 	count = 0

# 	for x in range(0, width):
# 		for y in range(0, height):
# 			if len(img.getpixel((x, y))) == 3:
# 				r, g, b = img.getpixel((x, y))
# 			else:
# 				r, g, b, t = img.getpixel((x, y))

# 			r_total += r
# 			g_total += g
# 			b_total += b 
			
# 			count += 1

# 	r_hex = hex(round(r_total/count))[2:].zfill(2)
# 	g_hex = hex(round(g_total/count))[2:].zfill(2)
# 	b_hex = hex(round(b_total/count))[2:].zfill(2)

# 	hex_color = f"0x{r_hex}{g_hex}{b_hex}"

# 	return int(hex_color, 16)
