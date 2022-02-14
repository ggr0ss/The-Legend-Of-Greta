alive = True
currentRoom = 1
caveMap = { 
  1: [2 ],
  2: [10, 4, 6],
  3: [2, 5, 9 ],
  4: [6, 5],
  5: [3, 7, 8 ],
  6: [12 ],
  7: [9 ],
  8: [7, 5],
  9: [3, 10 ], 
  10: [11, ],
  11: [9, 12, ],
  12: []
  }

def niceExitList (roomExits):
  global alive
  if len(roomExits) == 0:
    alive = False
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

def look():
  print(f"You are in room {currentRoom}")
  print(niceExitList(caveMap[currentRoom]))

def move() :
  global currentRoom
  nextRoom = int(input("Where would you like to go?"))
  if nextRoom not in caveMap[currentRoom]: 
    print(f"I'm sorry, you cannot get to room {nextRoom} from here.")
    return
  if nextRoom not in caveMap:
   print(f"Uh oh! Room {nextRoom} doesn't exist")
   return
  currentRoom = nextRoom

print("The Legend Of Greta")
print()
while alive:
  look()
  if not alive:
    break
  nextAction = input("\nWhat's next?").lower()[0]
  if nextAction.lower()[0] == "m":
    move()
    continue
  if nextAction.lower()[0] == "q":
   break
  print(f"I'm sorry, I don't know how to do '{nextAction}'.")
  print('I know how to quit.')