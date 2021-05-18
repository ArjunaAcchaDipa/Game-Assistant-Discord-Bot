import discord
import os
from keep_alive import keep_alive
from replit import db

client = discord.Client()

def show_commands():
  command = """```
  Information
  #info play
  #add <game-name> <number-of-player> <name-1>, ..., <name-n>
  #del <number-in-list>
  #clear
  #join <number-in-list>
  
  Miscellaneous
  #hello
  #you```"""

  return command

def join_play_list(user_name, index):
  user_list = db["user"]
  user_list[(int(index)-1)] += ", " + str(user_name)
  db["user"] = user_list

  player_list = db["player"]
  player_list[(int(index)-1)] = str(int(player_list[(int(index)-1)]) + 1)
  db["player"] = player_list

def update_play_list(game_name, total_player, user_name, tl_name):
  if "game" in db.keys() and "player" in db.keys() and "user" in db.keys() and "team_leader" in db.keys():
    game_list = db["game"]
    game_list.append(game_name.lower().title())
    db["game"] = game_list

    player_list = db["player"]
    player_list.append(total_player)
    db["player"] = player_list

    user_list = db["user"]
    user_list.append(user_name.lower().title())
    db["user"] = user_list

    tl_list = db["team_leader"]
    tl_list.append(tl_name)
    db["team_leader"] = tl_list
  else:
    db["game"] = [game_name.lower().title()]
    db["player"] = [total_player]
    db["user"] = [user_name.lower().title()]
    db["team_leader"] = [tl_name]
  
def delete_play_list(index):
  game_list = db["game"]
  player_list = db["player"]
  user_list = db["user"]
  tl_list = db["team_leader"]

  del game_list[(int(index)-1)]
  db["game"] = game_list
  del player_list[(int(index)-1)]
  db["player"] = player_list
  del user_list[(int(index)-1)]
  db["user"] = user_list
  del tl_list[(int(index)-1)]
  db["team_leader"] = tl_list

@client.event
async def on_ready():
  print("Logged in as:\n{0.user.name}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content.lower()

  if msg.startswith("#hello"):
    await message.channel.send("Hello {}".format(message.author.name))
  
  elif msg.startswith("#you"):
    await message.channel.send(file=discord.File("meme_spiderman.jpg"))

  elif msg.startswith("#commands"):
    command = show_commands()
    await message.channel.send(command)

  elif msg.startswith("#command"):
    await message.channel.send("Don't forget the s ;)")

  elif msg.startswith("#info"):
    options = msg.split("#info ", 1)[1]
    if " " in options:
      await message.channel.send("There is something wrong with the command\nType `#commands` to show all commands")
    else:
      if options == "play":
        #show the user that is currently playing
        info_game = []
        info_player = []
        info_user = []
        if "game" in db.keys() and "player" in db.keys() and "user" in db.keys():
          info_game = db["game"]
          info_player = db["player"]
          info_user = db["user"]
          try:
            output = ""
            for index in range (len(info_game)):
              output += "{}. {} {} ({})\n".format(str(index+1), "".join(info_game[index]), "".join(info_player[index]), "".join(info_user[index]))
            await message.channel.send(output)
          except:
            await message.channel.send("There are no play list(s) for now")

  elif msg.startswith("#add"):
    options = msg.split("#add ", 1)[1]
    game_name = options.split(" ", 1)[0]
    total_player = options.split(" ", 2)[1]
    user_name = options.split(" ", 2)[2]
    comma_count = user_name.count(",")
    user_id = "<@" + str(message.author.id) + ">"

    if int(total_player) != (comma_count+1) or int(total_player) <= 0:
      await message.channel.send("There is something wrong with the command\nType `#commands` to show all commands")
    else:
      update_play_list(game_name, total_player, user_name, user_id)
      await message.channel.send("Play list has been added\nType `#info play` to show the list(s)")
  
  elif msg.startswith("#del"):
    game_list = db["game"]
    options = msg.split("#del ", 1)[1]
    if " " in options:
      await message.channel.send("There is something wrong with the command\nType `#commands` to show all commands")
    else:
      if len(game_list) == 0:
        await message.channel.send("There are no play list(s) for now")
      elif len(game_list) == 1 and options != "1":
        await message.channel.send("Do you mean play list number 1?")
      elif (int(options) <= 0) or ((int(options)-1) >= len(game_list)):
        await message.channel.send("Please choose between 1-{}".format(len(game_list)))
      elif (len(game_list)) > (int(options)-1):
        delete_play_list(options)
        await message.channel.send("Play list number {} has been deleted\nType `#info play` to show the list(s)".format(options))

  elif msg.startswith("#clear"):
    options = msg.split("#clear", 1)[1]
    if options:
      await message.channel.send("There is something wrong with the command\nType `#commands` to show all commands")
    else:
      game_list = db["game"]
      if len(game_list):
        while len(game_list) != 0:
          delete_play_list("1")
          game_list = db["game"]
        await message.channel.send("Play list has been cleared")
      else:
        await message.channel.send("There are no play list(s) for now")

  elif msg.startswith("#join"):
    options = msg.split("#join ", 1)[1]

    if " " in options:
      await message.channel.send("There is something wrong with the command\nType `#commands` to show all commands")
    else:
      if "game" in db.keys() and "player" in db.keys() and "user" in db.keys() and "team_leader" in db.keys():
        join_play_list(message.author.name, options)
        info_tl = db["team_leader"]
        print(info_tl)
        await message.channel.send("{} please chat {} when your game is done".format(info_tl[int(options)-1], message.author.name))
      else:
        await message.channel.send("There are no play list(s) for now")

keep_alive()  # used to keep the bot alive
client.run(os.getenv("TOKEN"))