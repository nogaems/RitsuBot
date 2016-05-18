# -*-coding:utf-8 -*-
import xmpp, time
from ritsu_api import *

# TODO: Clean wait_ping for those who didn't reply for long time

wait_ping = {}

def command_ping(bot, room, nick, access_level, parameters, message):
  if parameters:
    target = parameters
    if not target in bot.roster[room]:
      return '%s is unreachable.'%(target)
    if target == bot.self_nick[room]:
      return u'Пинг до %s - 0.0000 s.'%(target)
  else: target = nick
  target = '%s/%s'%(room, target)
  iq = xmpp.Iq('get', None, {'id': 'ping1xtc'}, target)
  iq.setTag('ping', namespace='urn:xmpp:ping')
  bot.client.send(iq)
  wait_ping[target] = (time.time(), message.getType(), nick)

def event_room_iq(bot, (iq, room, nick)):
  if iq.getID() == 'ping1xtc' and iq.getFrom() in wait_ping:
    pinged = wait_ping[iq.getFrom()]
    if pinged[1] == 'groupchat':
      target = room
    else:
      target = room+'/'+pinged[2]
    delay = round(time.time()-pinged[0], 4)
    bot.send_room_message(target, u'Пинг до %s  %0.4f s.'%(nick, delay))

def load(bot):
  bot.add_command('ping', command_ping, LEVEL_GUEST, 'ping')
  bot.add_command(u'пинг', command_ping, LEVEL_GUEST, 'ping')
  bot.add_command(u'зштп', command_ping, LEVEL_GUEST, 'ping')
  bot.add_command('gbyu', command_ping, LEVEL_GUEST, 'ping')
# All praise the Colemak
  bot.add_command(u'кдое', command_ping, LEVEL_GUEST, 'ping')
  bot.add_command('dbjl', command_ping, LEVEL_GUEST, 'ping')

def unload(bot):
  pass

def info(bot):
  return 'Ping plugin v1.0.1'
