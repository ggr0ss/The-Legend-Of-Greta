import random 
from enum import Enum

class WumpusState(Enum) :
  DEAD = 0
  AWAKE = 1
  ASLEEP = 2 

gameState = {
  "alive" : True,
  "wumpusState": WumpusState.ASLEEP, 
  "currentRoom" : 1,
  "wumpusRoom" : 1,
  "caveMap" : {
    1: [2 ],
    2: [4, 6, 10],
    3: [2, 5, 9 ],
    4: [5, 6],
    5: [3, 7, 8 ],
    6: [12 ],
    7: [9 ],
    8: [5, 7],
    9: [3, 10 ], 
    10: [11, ],
    11: [9, 12, ],
    12: []
  }
}

def numOfRooms(state): 
  count = 0
  for room in state["caveMap"] :
    count += 1
  return count

def safeRandomRoom(state) :
  while True:
    room = random.randint(1,numOfRooms(state))
    roomExits = state["caveMap"] [room]
    if len(roomExits) > 0:
      break
  return room

def newGame(state) :
  if numOfRooms(state) < 2:
    print("A game that only has one room is not supported.")
    raise SystemExit
  while state ["wumpusRoom"] == state["currentRoom"]:
    state["wumpusRoom"] = safeRandomRoom(state)
    state["currentRoom"] = safeRandomRoom(state)

def niceExitList (state):
  currentRoom = state["currentRoom"]
  roomExits = state["caveMap"][currentRoom]
  if len(roomExits) == 0:
    state["alive"] = False
    return "You are trapped! This room has no exits, you have starved."
  if len(roomExits) == 1:
    return f"This room's only exit is to room {roomExits[0]}"
  if len(roomExits) == 2:
    return f"This room has exits to rooms {roomExits[0]} and {roomExits[1]}."

  niceList= "This room has exits to rooms: "
  for exitNum in range(len(roomExits)-1):
   niceList += f"{roomExits[exitNum]}, "
  niceList += f"and {roomExits [-1]}."

  return niceList

def look(state):
  currentRoom = state["currentRoom"]
  print(f"You are in room {currentRoom}")
  if currentRoom == state["wumpusRoom"] :
    if state["wumpusState"] == WumpusState.ASLEEP: 
      print("You stumble upon a sleeping wumpus.")
    else: 
      print("The wumpus stares back at you.")
  print(niceExitList(state))

def move(state) :
  currentRoom = state["currentRoom"]
  nextRoom = int(input("Where would you like to go?"))
  if nextRoom not in state["caveMap"][currentRoom]: 
    print(f"I'm sorry, you cannot get to room {nextRoom} from here.")
    return
  if nextRoom not in state["caveMap"]:
   print(f"Uh oh! Room {nextRoom} doesn't exist")
   return
  state["currentRoom"] = nextRoom

def encounter(state) :
  if state["currentRoom"] == state["wumpusRoom"] :
    if state["wumpusState"] == WumpusState.ASLEEP:
      print("You have awoken the wumpus!")
      state["wumpusState"] == WumpusState.AWAKE 
    else: 
      print("Nom nom nom. You have been eaten by the wumpus!")
      state["alive"] = False

newGame(gameState)
print("The Legend Of Greta")
print("Hint: The wumpus is in room {wumpusRoom}".format_map(gameState))
while gameState ["alive"]:
  look(gameState)
  if not gameState["alive"]:
    break
  nextAction = input("\nWhat's next?").lower()[0]
  if nextAction.lower()[0] == "m":
    move(gameState)
    continue
  if nextAction.lower()[0] == "q":
   break
  print(f"I'm sorry, I don't know how to do '{nextAction}'.")
  print('I know how to quit.')