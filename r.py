#!/usr/bin/python
# -*- coding:utf-8 -*-
import os, sys, textwrap, time, re
import praw
reddit = praw.Reddit(client_id='YOUR', client_secret='KEYS', password='GO', user_agent='RIGHT', username='HERE')

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V2
from PIL import Image, ImageDraw, ImageFont

epd = epd2in13_V2.EPD()
epd.init(epd.FULL_UPDATE)
epd.Clear(0xFF)


font15 = ImageFont.truetype(os.path.join(picdir, 'GnuUnifont.ttf'), 15)

def printToDisplay(string):
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)
    draw.text((0, 10), string, font = font15, fill = 0)
    epd.display(epd.getbuffer(image))



sub = reddit.subreddit('wallstreetbets')
piprint = sub.hot(limit=1)

for submissions in piprint:
	if submissions.stickied:
		print('{}'.format(submissions.title))
		title = textwrap.fill(submissions.title, width = 18)
		printToDisplay(f"{title}")

zz = submissions.id

start_time = time.time()

def run():
    for comment in sub.stream.comments(pause_after=None, skip_existing=True):
        while submissions.id == comment.submission:
            ap = 't3_'
            ap += zz

            if ap == comment.parent_id:
                print(30*'_')
                comment.body = textwrap.fill(comment.body, width = 35)
                print(comment.body)
                print(comment.author)
                comment.body = re.sub(r"' ", "'", comment.body)
                printToDisplay(f"{comment.body}\n-{comment.author}")
                run()
            else:
                run()
run()
