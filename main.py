import discord
import os
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

def update_list(new_title): 
  if("title" in db.keys()):
    title = db["title"]
    title.append(new_title)
    db["title"] = title
  else:
    db["title"] = [new_title]

def delete_title(index):
  title = db["title"]
  
  if(len(title) > index):
    movie_title = title[index]
    del title[index]
    db["title"] = title

  return movie_title

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  await client.change_presence(status=discord.Status.dnd)

@client.event
async def on_message(message):
  if(message.author == client.user) :
    return
  
  if(client.user.mentioned_in(message)):

    await message.channel.send("yo")

  if(message.content.startswith("!add")):
    new_title = message.content.split("!add ", 1)[1]
    #print(new_title)
    update_list(new_title)
    await message.channel.send(new_title + " has been added to the list.")

  if(message.content.startswith("!delete")):
    title = []
    
    if("title" in db.keys()):
      index = int(message.content.split("!delete ", 1)[1])
      movie_title = delete_title(index - 1)
      await message.channel.send(movie_title + " has been deleted.")
      title = db["title"]
      

    #await message.channel.send(title)
  
  if(message.content.startswith("!list")):

    #msg = ""
    msg = "```\n"

    if("title" in db.keys()):
      line_numb = 1

      for i in db["title"]:
        #msg = msg + ("`" + i + "`" + "\n")
        msg = msg + str(line_numb) + " " + i + "\n"
        line_numb += 1

    msg = msg + "```" 

    await message.channel.send(msg)

  if(message.content.startswith("!empty")):
    numbOfKeys = 0

    if("title" in db.keys()):
      for i in db["title"]:
        numbOfKeys += 1
      
      for i in range(numbOfKeys):
        delete_title(i-i)

  if(message.content.startswith("!rand")):
    if("title" in db.keys()):
      #title = db["title"]
      await message.channel.send(random.choice(db["title"]))

  if(message.content.startswith("!command-list")):
    msg = "```\n!add - adds movie to the list\n!list - list all the movies\n!empty - clears the list\n!rand - randoms a movie\n!delete [n] - deletes [n]-th movie from the list```"

    await message.channel.send(msg)

  if(message.content.startswith("!flip")):
    coin = ["heads", "tails"]
    name = str(message.author)
    name = name.split("#")[0]
    await message.channel.send(name + " flipped a coin and got " + random.choice(coin))


keep_alive()
client.run(os.getenv("TOKEN"))
