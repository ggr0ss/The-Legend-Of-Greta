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
  "startleChance" : .60,
  "sleepChance": .33,
  "arrows": 4, 
  "caveMap" : { 
    1: [2 ],
    2: [4, 6, 10],
    3: [2, 5, 9 ],
    4: [1, 5, 6],
    5: [3, 7, 8 ],
    6: [12 ],
    7: [9 ],
    8: [5, 7],
    9: [3, 10 ], 
    10: [11, ],
    11: [1, 9, 12, ],
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

def niceArrowList(numArrows):
  if numArrows == 0:
    return "You're out of arrows!"
  if numArrows == 1:
    return "You're down to your last arrow!"
  return f"You have {numArrows} arrows in your quiver."


def niceExitList (state):
  currentRoom = state["currentRoom"]
  roomExits = state["caveMap"][currentRoom]
  if len(roomExits) == 0 and state["alive"]:
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

def sense(state):
  currentRoom = state["currentRoom"]
  print(f"You are in room {currentRoom}")
  print(niceArrowList(state["arrows"]))
  if currentRoom == state["wumpusRoom"] :
    if state["wumpusState"] == WumpusState.ASLEEP: 
      print("You stumble upon Greta taking a nap.")
    else: 
      print("The wumpus stares back at you.")
  for exitNumber in state["caveMap"][state["currentRoom"]]:
    if state["wumpusRoom"] == exitNumber:
      print("The smell of Greta fills your nostrils.")  
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
  if state["currentRoom"] == state["wumpusRoom"] and state["wumpusState"] == WumpusState.ASLEEP:
      print("You have awoken Greta!")
      state["wumpusState"] = WumpusState.AWAKE 
      if (random.random() < state["startleChance"]):
        roomExits = state["caveMap"][state["currentRoom"]]
        if len(roomExits) == 0:
          print("You have startled Greta, but this room has no exits!")
        else:
          print("Lucky for you, you scared Greta and she has run out.")
          state["wumpusRoom"] = random.choice(roomExits)
  if state["currentRoom"] == state["wumpusRoom"] and state["wumpusState"] == WumpusState.AWAKE: 
      print("*Crunch* Oh no! You have been eaten by Greta!")
      state["alive"] = False

def updateHarzards(state) :
  if state["wumpusState"] == WumpusState.AWAKE: 
    roomExits = state["caveMap"][state["currentRoom"]]
    if random.random() < state["sleepChance"]:
      print("Hint: The wumpus has fallen asleep.")
      state["wumpusState"] = WumpusState.ASLEEP
    elif len(roomExits) > 0:
     state["wumpusRoom"] = random.choice(roomExits)

newGame(gameState)
print("The Legend Of Greta")
print("Hint: The wumpus is in room {wumpusRoom}".format_map(gameState))
while gameState ["alive"]:
  sense(gameState)
  encounter(gameState)
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