from move import north, south, east, west, up, down, directions, allDirections
import items
from copy import deepcopy
#import roomScripts
roomTimer=0

class room:
    def __init__(self, name, description, allDirections, validDirections={},
    items=[], intrinsicItems=[], door=[], furniture=[], scripts=None, monsters=[], enterScript=None): 
        self.name=name
        self.description=description
        self.allDirections=deepcopy(allDirections)
        self.validDirections=validDirections
        self.items=deepcopy(items)
        self.intrinsicItems=deepcopy(intrinsicItems)
        self.door=deepcopy(door)
        self.furniture=deepcopy(furniture)
        self.scripts=scripts
        self.monsters=deepcopy(monsters)
        self.enterScript=enterScript

        for direction in validDirections: 
            for directionDescription in self.allDirections[direction]:
                self.allDirections[direction][directionDescription]=validDirections[direction]



def changeIntrinsicDesc(room, itemName, description):
    for item in room.intrinsicItems:
        for name in item.name:
            if itemName==name:
                item.description=description

#ENTER ROOM SCRIPTS(these are initialized the moment the player enters the room)
def restoreIce():  #Makes it so player has to get clothing to solve the puzzle. Intended for northRoom
    for item in currentRoom.items:
        for name in item.name:
            if name =="cluster of icicles":
                if item.hitPoints < 4:
                    item.hitPoints=4
                    print("""You know it's not possible under the normal rules of reality ice to return this quickly,
but since you were last in this frigid room, the cluster of icicles obscuring the plaque has been restored.
The Gods toy with you.""")

def meetMagios(): #Initiates final confrontation in mage room.
    print(
"""As soon as you enter the room.  The door shuts and locks behind you.  Suddenly, a man in a blue, hooded robe appears before
you. 'Welcome, creature. I am gratified to see you've made it through your first trials.' he says. 'I am called the Magios.'""")

def checkIfHave():#for Ninjai room puzzle.  Checking at turn 1 is too late.  May already have changed.
    if items.player.inventory == []:
        ninjaiRoom.haveHad=False
    if items.player.inventory != []:
        ninjaiRoom.haveHad=True
        

#ROOM SCRIPTS(waits 1 turn before kicking in to give player time)
def freezeToDeath(roomTimer):  #for northRoom
    icicleExists=False
    for item in currentRoom.items:
            for name in item.name:
                if "cluster of icicles" == name:
                    icicleExists=True
    if icicleExists==False:
        #plaqueIndex=getItemIndex("plaque", currentRoom.intrinsicItems)
        currentRoom.intrinsicItems[5].description="""Inscribed on the grey marble plaque in the alcove you see the words:
MAY THOSE WHO SAY "AHA!" BE TURNED BACK IN SHAME. - PSALMS 70:3"""
        #alcoveIndex=getItemIndex("alcove", currentRooms.intrinsicItems)
        currentRoom.intrinsicItems[6].description="""The alcove is now freed from the ice and you can clearly
see the grey marble plaque within it."""
        currentRoom.description="""The walls are made of ice that shines glacial blue.  It's freezing in here. There's a steel door to the south.
In the north wall you see an alcove with a grey marble plaque mounted inside of it."""
        currentRoom.enterScript=None
        
    if items.player.clothesDescription != "You are naked.": #wearing clothes helps you stay warm longer (duh)
        for part in items.player.partOf:
            if part.inventory != []:
                for item in part.inventory:
                    if item.isClothing==True:
                        if item.warmth is not None:
                            roomTimer-=item.warmth

    if roomTimer == 1:  #grace period of 1 turn before it starts hurting you
        return print("Thweehwweeew!  Whistling winter winds freeze you to the bone.",
        "You won't be able to stay here very long.")
    
    if roomTimer > 1:
        if items.player.hitPoints == 3:
            print("Thweeeeehwweeew! The cold cuts through you like a steel blade.")
        if items.player.hitPoints == 2:
            print ("Thweeeeeeeiieieiew! As your body grows numb you start no longer to feel the cold",
                   "\nso acutely.  You feel suddenly warm, as if you could nod off and take a nap.")
        if items.player.hitPoints == 1:
            print ("Thwiiiiewweweiiiieiwww! With one more gust the icy gales lull you into\n"
            "eternal slumber.  Your corpse stands there as if dumbfounded wide open",
            "\nfrozen eyes staring.  You have died.  THE END.")
            input()
            items.player.isAlive=False
        items.player.hitPoints -= 1

def provokedMagios(magios):
    print("""The magios abruptly disappears from the room but you still hear his voice: "So that's how you want
it to be!" he sneers. "You aren't the only one who can be nasty.  Hmmm, what's the most annoying way in the world
to die?  I know.  I know just the thing for you.  Double your health and leave you with a few of my pets.  I hope
you enjoy their company." Suddenly three flabberghasts appear out of thin air and immediately attack you.""")
    items.player.hitPoints=6
    items.player.dodge = 1
    mageRoom.monsters.append(deepcopy(items.flabberGhast))
    mageRoom.monsters.append(deepcopy(items.flabberGhast))
    mageRoom.monsters.append(deepcopy(items.flabberGhast))
    if mageRoom.monsters[1].name[0]=="greater imp":
        del(mageRoom.monsters[1])
    del(mageRoom.monsters[0])
    mageRoom.scripts=[]

def magiosScript(roomTimer): #for mageRoom
        
    if roomTimer == 1:
        items.player.dodge=2
        items.player.hitPoints=4
        print(
"""I can see your challenges here have successfully drawn out the potential we wanted in you.  Let me help you
realize it in full.  A look of deep concentration passes over the magios' face and you feel something
start to change within you.  You feel your skin hardening, your muscles growing bigger.  Time seems to slow down
as your reflexes improve.  You recoil in shock.  'There.' says the Magios.  That should endow you with the reward
you've earned through your struggles.  Now I shall put you through one more trial to test your new gifts.""")
    if roomTimer==2:
        mageRoom.monsters.append(items.greaterImp)
        print(
"""The magios makes a gesture with one hand and a strangely human creature with scales and spikes on its skin materializes
out of thin air. "This is a greater imp of the trickster god." says the Magios and if you meet expectations, that is the rank
you now hold.  Now..fight for your place.  Without hesitation the greater imp growls low in its chest and despite its human form
lunges at you like an animal.""")
    if roomTimer > 3:
        impAlive=False
        for monster in currentRoom.monsters:
            if monster.name[0]=="greater imp":
                impAlive=True
        if impAlive==False:
            print("""
"Very impressive, creature."  says the magios.  You may look on the surface just like a normal human but you are a
construct of chaos, a weapon made to blend in.  We have been through been through very many prototypes but I think
in you we may finally have what we're looking for.  On to the next challenges, then."  You feel yourself shifting
as the magios teleports away, taking you with him,. THE END""")
            items.player.isAlive=False

def openSteelDoor(roomTimer): #for ninjaiRoom
    if ninjaiRoom.door[0].isOpen==False:
        #if roomTimer==1:
        #    if items.player.inventory==[]:
        #        ninjaiRoom.haveHad=False
        if ninjaiRoom.haveHad==True:
            if items.player.inventory==[]:
                print("""With a grating sound of metal on stone, the steel door slowly opens upward.
""")
                ninjaiRoom.door[0].isOpen=True
    if ninjaiRoom.door[0].isOpen==True:
        if items.player.inventory!=[]:
            print("""In a moment, the metal door falls shut with crash.
""")
            ninjaiRoom.door[0].isOpen=False

def unlockCage(roomTimer): #for puzzleRoom
    solved=False
    if currentRoom.items != []:
        if puzzleRoomCage.isLocked==True:
            puzzleRoomCage.isLocked=False
            print("You hear a loud click from the cage's lock.")
        
        

    
#Intrinsic Item names: player, wall, floor, ceiling
#CREATING ROOMS

#STARTING ROOM
startingRoom=room("startingRoom","""The walls are made of moldy gray bricks.  There's an obelisk of healing in the
center of the room. On the floor in one corner you see a trap door.  Along the wall you see
a wooden table.  There's a door to the north and open passages to the east, south, and west.""",
allDirections,{'east': "You go east", 'north': "You go north", 'down': "You go down",
"west": """As you go west uneven gray bricks give way to natural walls of limestone.""", "south":"You go south"},
[items.pebble, items.woodenBox] , items.intrinsicItems)

startWoodenTable=deepcopy(items.woodenTable)
#startWoodenTable.surface.append()
startingRoom.furniture.append(startWoodenTable)
startingRoom.furniture.append(deepcopy(items.healingObelisk))


changeIntrinsicDesc(startingRoom, "wall", "The walls are made of moldy gray bricks.") #wall
changeIntrinsicDesc(startingRoom, "floor", "The floor is made of uneven grey stone. In one corner you see a trap door.") #floor
changeIntrinsicDesc(startingRoom, "roof", "The ceiling is made of damp grey bricks of crudely ancient construction.\n"
"You see the occasional patch of moss.")
#Door to north Room
startingRoom.door.append(deepcopy(items.steelDoor)) #Add steel door going north
startingRoom.door[0].isOpen=False
startingRoom.door[0].isLocked=False
startingRoom.door[0].goesTo="northRoom"
startingRoom.door[0].direction="north"
#Door to lounge/kitchen
#startingRoomWoodenDoor=deepcopy(items.woodenDoor) #wooden door goes south
#startingRoomWoodenDoor.isOpen=False
#startingRoom.door.append(startingRoomWoodenDoor)
#Trap door to dungeon room
startingRoom.door.append(deepcopy(items.trapDoor))#trap door goes down
trapDoor=startingRoom.door[1]
trapDoor.isOpen=False
trapDoor.goesTo="dungeonRoom"
trapDoor.direction="down"
#Items for testing only: These should be commented out below this point.
#startingRoom.items.append(deepcopy(items.brassKey)) #uncomment out for test runs
#startingRoom.items.append(deepcopy(items.goldenKnife))
#startingRoom.items.append(deepcopy(items.chainMailShirt))
#startingRoom.monsters.append(deepcopy(items.magios))
#startingRoom.monsters.append(deepcopy(items.blowDartNinjai))


#startingRoom.value=[]

#EAST ROOM
eastRoom=room("eastRoom","The walls are Neon pink. There's a door to the West", allDirections, {'west': "You go west"},
              [items.plasticFlamingo, items.pinkBathrobe], items.intrinsicItems)
eastRoom.door=[]
changeIntrinsicDesc(eastRoom, "wall", "The walls are blindingly neon pink.")
changeIntrinsicDesc(eastRoom, "floor", "The floor is blindingly neon pink.\nIt's made of some kind of squishy rubber foam.")
changeIntrinsicDesc(eastRoom, "roof", "The ceiling is blindingly neon pink.\nJust trying to look at it makes your eyes water profusely.")
eastRoom.monsters.append(deepcopy(items.peptoBismolGlop))

#NORTH ROOM
northRoom=room("northRoom",
"""The walls are made of ice that shines glacial blue.  It's freezing in here. There's a steel door to the south.
In the north wall you see an alcove that has accumulated ice deposits from the constantly whistling winter winds that
tear through the room.""",
               allDirections, {'south':"You go south.", 'north':"You're blocked by a solid wall of ice",
               'east': "You're blocked by a solid wall of ice.", 'west': "You're blocked by a solid wall of ice."},
               [items.icicles], items.intrinsicItems)
northRoom.enterScript=restoreIce #this prevents player from using a cheap strategy to solve the puzzle.
northRoom.intrinsicItems.append(items.marblePlaque)
northRoom.intrinsicItems.append(items.alcove)
northRoom.door.append(deepcopy(items.steelDoor))
northRoom.door[0].goesTo="startingRoom"
northRoom.door[0].direction="south"
northRoom.door[0].isOpen=True
northRoom.door[0].isLocked=False
northRoom.door[0].description=northRoom.door[0].description + " The steel door is open."

changeIntrinsicDesc(northRoom, "wall", "The walls are made of solid ice that imparts a pale blue glow to the room.")
changeIntrinsicDesc(northRoom, "floor", "The ground beneath your feet is a solid sheet of ice.")
northRoom.scripts=[]
northRoom.scripts.append(freezeToDeath)
#These are separate from instantion because they're all interdependent.  StartingRoom couldn't refer to a northRoom that
#doesn't exist yet.

#GHAST CHAMBER
ghastRoom=room("dungeonRoom", """The walls are made uniform grey bricks. The light here gives everything
a dim grey cast. There is a passageway to the east.""",
            allDirections, {'east':"You go east."})
#Trap door upwards
ghastRoom.intrinsicItems=deepcopy(items.intrinsicItems)
ghastRoom.monsters.append(deepcopy(items.flabberGhast))
ghastRoom.items.append(deepcopy(items.brassKey)) #have to kill ghast to get the key to magios room)

#DUNGEON ROOM
dungeonRoom=room("dungeonRoom", """The walls are made of uniform grey bricks. The light here gives everything a dim grey cast.
There are passageways east and west. A steel ladder leads upwards.""",
            allDirections, {'up':"You go up.", "west":"You go west", "east":"You go east"})
#Trap door upwards
dungeonRoom.intrinsicItems=deepcopy(items.intrinsicItems)
dungeonRoom.intrinsicItems.append(deepcopy(items.steelLadder))
dungeonRoom.door.append(deepcopy(items.trapDoor))
trapDoor2=dungeonRoom.door[0]
trapDoor2.goesTo="startingRoom"
trapDoor2.direction="up"
trapDoor2.isOpen=True
trapDoor2.description+= " The trap door is open."

#NINJAI ROOM
ninjaiRoom=room("dungeonRoom", """The walls are made of uniform grey bricks. The light here gives everything
a dim grey cast. There is a passageway to the west. To the east is a thick, featureless metal door on the east wall
that looks like it opens upwards like a portcullis.  There is a grey marble plaque set into the wall next to the metal
door.""",
            allDirections, {'west':"You go west.", 'east':"You go east"})
ninjaiRoom.intrinsicItems=deepcopy(items.intrinsicItems)
ninjaiRoom.intrinsicItems[3].outOfReach=True #can't reach ceiling here
ninjaiRoom.monsters.append(deepcopy(items.blowDartNinjai))
#create steel gate
ninjaiRoomSteelDoor=deepcopy(items.steelDoor)
ninjaiRoomSteelDoor.description="""It's a thick, featureless metal door on the east wall that looks like it opens upwards like
a portcullis.  There's definitely no lock or handle.  You'll have to find another way to get it open.
"""
ninjaiRoomSteelDoor.isOpen=False
ninjaiRoomSteelDoor.isLocked=True
ninjaiRoomSteelDoor.goesTo="puzzleRoom"
ninjaiRoomSteelDoor.direction="east"
ninjaiRoom.door.append(ninjaiRoomSteelDoor)
ninjaiRoom.haveHad=True

ninjaiRoomPlaque=deepcopy(items.marblePlaque)
ninjaiRoomPlaque.description="""It's a grey marble plaque set into the wall engraved with the words:
TO KNOW LOSS YOU MUST ONCE HAVE HAD. LEAVE EVERYTHING BEHIND AND GO FORWARD.
"""
ninjaiRoom.intrinsicItems.append(ninjaiRoomPlaque)
ninjaiRoom.scripts=[]
ninjaiRoom.scripts.append(openSteelDoor)
ninjaiRoom.enterScript=checkIfHave

#PUZZLE ROOM
puzzleRoom=room("puzzleRoom", """The walls are made of uniform grey bricks. The light here gives everything
a dim grey cast. There is an open steel door to the west.  In the center of the room is a heavy steel cage.  Through the
narrow slats of its bars you can see a shirt of chainmail inside it.  Set into the east wall is a grey marble plaque.""",
            allDirections, {'west':"You go west."}, [], items.intrinsicItems)
#puzzleRoom.intrinsicItems=deepcopy(items.intrinsicItems)
puzzleRoomPlaque=deepcopy(items.marblePlaque)
puzzleRoomPlaque.description="""It's a grey marble plaque inscribed with the words:
WHAT MORE CAN YOU GIVE?
"""
puzzleRoom.door.append(ninjaiRoomSteelDoor)
puzzleRoom.scripts=[]
puzzleRoom.scripts.append(unlockCage)
puzzleRoomChainMail=deepcopy(items.chainMailShirt)
puzzleRoomCage=deepcopy(items.steelCage)
puzzleRoomCage.inventory.append(puzzleRoomChainMail)
puzzleRoomCage.isLocked=True
puzzleRoom.intrinsicItems.append(puzzleRoomCage)
puzzleRoom.intrinsicItems.append(puzzleRoomPlaque)

#WEST ROOM
westRoom=room("westRoom", """"You are in a room with cave-like stone walls.  There is a passageway to the east
and a door to the west.""", allDirections,
{"east":"You go east","west":"You go west"}, [], items.intrinsicItems)  #Have the giggler, food, bathrobe?
westRoomWoodenDoor=deepcopy(items.woodenDoor)
westRoomWoodenDoor.isLocked=True
westRoomWoodenDoor.isOpen=False
westRoomWoodenDoor.direction="west"
westRoomWoodenDoor.goesTo="mageRoom"
westRoomWoodenDoor.lockedBy="brass key"
westRoom.door.append(westRoomWoodenDoor)

westRoom.monsters.append(deepcopy(items.giggler))

#MAGIOS CHAMBER
mageRoom=room("mageRoom","You are in a room with cave-like stone walls.  There is a door to the east.", allDirections,
{"east":"You go east"}, [], items.intrinsicItems)
mageRoom.monsters.append(deepcopy(items.magios)) #magios in room
#mageRoom.monsters.append(deepcopy(items.flabberGhast))
#mageRoom.monsters.append(deepcopy(items.flabberGhast))
mageRoomWoodenDoor=deepcopy(items.woodenDoor)
mageRoomWoodenDoor.isLocked=True
mageRoomWoodenDoor.isOpen=False
mageRoomWoodenDoor.goesTo="westRoom"
mageRoomWoodenDoor.lockedBy=""
mageRoom.door.append(mageRoomWoodenDoor)
#scripts
mageRoom.enterScript=meetMagios
mageRoom.scripts=[]
mageRoom.scripts.append(magiosScript)



#SOUTHROOM
southRoom=room("southRoom", """You find yourself in a cozy room that with a bar counter, a bar stool, and a lounge chair.
There is a stone brick passageway to the north.""", allDirections, {"north":"You go north"}, [], items.intrinsicItems)
southRoomItems=[items.loungeChair, items.barStool]
for furniture in southRoomItems:
    southRoom.items.append(deepcopy(furniture))
southRoom.furniture.append(deepcopy(items.servingBar))
southRoom.furniture[0].surface.append(deepcopy(items.liverWurstSandwich))



#SETTING ROOM DIRECTIONS                       
startingRoom.nextRoom={eastRoom: east,  northRoom: north, dungeonRoom: down, westRoom: west, southRoom: south}
eastRoom.nextRoom={startingRoom: west}
northRoom.nextRoom={startingRoom: south}
dungeonRoom.nextRoom={startingRoom: up, ghastRoom: west, ninjaiRoom: east}
ghastRoom.nextRoom={dungeonRoom: east}
ninjaiRoom.nextRoom={dungeonRoom: west, puzzleRoom: east}
puzzleRoom.nextRoom={ninjaiRoom: west}
westRoom.nextRoom={startingRoom: east, mageRoom: west}
mageRoom.nextRoom={westRoom: east}
southRoom.nextRoom={startingRoom: north}


currentRoom=startingRoom
