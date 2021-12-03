import random

#var
win = False
dead = False
y = random.randrange(0,4)
x = 3
turn = 1
inv = []
troll = True
health = 2
dev = False

possible_locations_game = [[0,0],[0,1],[0,2],[0,3],
                           [1,0],[1,1],[1,2],[1,3],
                           [2,0],[2,1],[2,2],[2,3],
                           [3,0],[3,1],[3,2],[3,3]]
game = [["l","","t",""],
        ["","","l",""],
        ["w","","l","n"],
        ["k","","d","l"]]
dic_game = {
  "":"None",
  "n":"Knife",
  "l":"Pit of Lava",
  "t":"There is a troll here. He is standing infront of a chest that requires a key. You cannot fight the troll without a weapon.",
  "c":"A locked chest that requires a key stands here. Along with a dead troll.",
  "d":"There is a glowing pile of dirt here. You need a shovel to 'dig' up whatever is under it.",
  "k":"Key",
  "w":"Wall",
  "s":"Shovel"
}

key_list = list(dic_game.keys()) 
val_list = list(dic_game.values())

#functions
def interpreter(action):
  if action in commands:
    commands[commands.index(action)-1]()
  else:
    print("Unknown Command")

#Checks if players move is valid. 
#This is not only for the edge this is also for if there 
#is a gate or a wall you cannot pass. This function 
#also interacts with the troll.
def checkmove(posy,posx):
  global health
  if [posy,posx] in possible_locations_game:
    if [y,x] == [0,2] and game[posy][posx] == "" and game[0][2] != "c" and game[0][2] != "s" and game[y][x] != "":
      health += -2
      print("You tried to run past the troll. He hit you again and you died.")
      return False
    elif game[posy][posx] == "" or game[posy][posx] == "n" or game[posy][posx] == "l" or game[posy][posx] == "s" or game[posy][posx] == "k" or game[posy][posx] == "c" or game[posy][posx] == "d":
      return True
    elif game[posy][posx] == "t" and "Knife" not in inv:
      health += -2
      print("You have entred the trolls cell without a weapon to fight him and he has killed you instantly.")
      return True
    elif game[posy][posx] == "t":
      randomnumb = random.randrange(0,11)
      if randomnumb > 6:
        health += -2
        print("The troll killed you in one blow when you entred his cell.")
        return True
      else:
        health += -1
        print("When you entered the trolls cell he took away a point of health.")
        return True
    else:
      print("You cannot pass through " + dic_game.get(game[posy][posx]))
      return False
  else:
    print("Out of bounds move!")
    return False

#Shows what is around your cell and in your cell. Showed in: N/E/S/W
def visualize():
  print("Health:", health)
  if [y,x] in possible_locations_game:
    print("Cell: " + dic_game.get(game[y][x]))
  if [y-1,x] in possible_locations_game:
    print("Above: " + dic_game.get(game[y-1][x]))
  else:
    print("Above: Outside of World")
  if [y,x+1] in possible_locations_game:
    print("Right: " + dic_game.get(game[y][x+1]))
  else:
    print("Right: Outside of World")
  if [y+1,x] in possible_locations_game:
    print("Below: " + dic_game.get(game[y+1][x]))
  else:
    print("Below: Outside of World")
  if [y,x-1] in possible_locations_game:
    print("Left: " + dic_game.get(game[y][x-1]))
  else:
    print("Left: Outside of World")

#Movment Functions
def left():
  global x
  global y
  if checkmove(y,x-1):
    x += -1

def right():
  global x
  global y
  if checkmove(y,x+1):
    x += 1

def up():
  global y
  global x
  if checkmove(y-1,x):
    y += -1

def down():
  global y
  global x
  if checkmove(y+1,x):
    y += 1

def print_board():
  global dev
  if dev == True:
    print("Player location(y,x):", y,x)
    print("Inventory:",inv)
    print("",game[0],"\n",game[1],"\n",game[2],"\n",game[3])

#Grab Function
def grab():
  if len(inv) < 3:
    if game[y][x] != "" and dic_game.get(game[y][x]) != "it" and dic_game.get(game[y][x]) != "w":
      inv.append(dic_game.get(game[y][x]))
      print(dic_game.get(game[y][x]) + " has been added to your inventory.")
      game[y][x] = ""
    else:
      print("There is nothing in your current location to grab. If you see something around you try moving to that position and 'grab' again.")
  else:
    print("Your inventory is full! Try and drop something and then picking it up again.")

#Drop Function
def drop():
  print("What would you like to drop? Please enter the item exactly how it is in the list.")
  inventory()
  i1 = input(">")
  if i1 in inv:
    inv.remove(i1)
    game[y][x] = key_list[val_list.index(i1)]
    print("You droped your " + i1)
  else:
    print("The item '" + i1 + "' is not in your inventory!")

#Fight Function
def fight():
  if [y,x] == [0,2] and game[y][x] == "t" and "Knife" in inv:
    troll = False
    print("You kill the troll in one hit! All that is left is a locked chest.")
    game[0][2] = "c"

#Open Function
def open():
  if game[y][x] == "c":
    if "Key" in inv:
      inv.remove("Key")
      print("You have opened the chest that the troll once stood by and now here lays a shovel.")
      game[0][2] ="s"
  else:
    print("There is nothing here to open.")

#Dig Function
def dig():
  global win
  if game[y][x] == "d":
      if "Shovel" in inv:
        win = True
      else:
        print("You can't dig without a shovel!")
  else:
    print("There is nothing to dig here.")

#Help Function
def help():
  print("The basic commands you can do to move around/interact with the world are left, right, up, down, grab, fight, help, open, dig and inventory. If you would like to run the game in developer mode please run the command 'developer'.The info below this text is everything in the places directly around you.")

#Turns on developer mode
def developer():
  global dev
  dev = True
  
#Inventory Function
def inventory():
  print("Inventory: ", inv)

#Check Dead Function
def check_dead():
  global dead
  if health < 1:
    dead = True

#Commands
commands = [left,"left",right,"right",up,"up",down,"down",grab,"grab",fight,"fight",help,"help",inventory,"inventory",drop,"drop",dig,"dig",open,"open",developer,"developer"]

#Game Loop
while win == False:
  print_board()
  check_dead()
  if dead or game[y][x] == "l":
    break
  if health < 2 and turn % 4 == 0:
    health += 1
  visualize()
  if turn == 1:
    print("\nWelcome! Your mission is to find the Golden Sword hidden somewhere in this world! If you need help type the 'help' command. You will also gain a health point every 4 turns.")
  i = input(">")
  interpreter(i)
  turn += 1
  
#Death/Win Statements
if win == True:
  print("Congraulations! You have dug up the golden sword and won the game!")
elif game[y][x] == "l" and turn == 1:
  print("Damn, you're unlucky. You spawned in a pit of lava and melted to death.")
elif game[y][x] == "l":
  print("You melted in a pit of lava.")
else:
  print("You died. RIP")