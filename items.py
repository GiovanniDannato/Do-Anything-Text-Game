import random
from copy import deepcopy
#Attribute names: damage, withVerbs,

 #everything that needs this has items.py in its scope

class item:
    isHeal=False
    isClothing=False
    isSurface=False
    isAlive=False
    understands=None
    canSeeInside=False
    outOfReach=False
    def __init__(self, description, name=[],  partOf=[], inventory=[], isContainer=False,
    isOpen=False, hitPoints=None, withVerbs=None, damage=None, size=None, containerSize=None,
    isLocked=False, lockedBy=None, surfaceSize=None, surface=None, smell=None, taste=None, texture=None,
    isEdible=False, weight=None): #,isHeal=False):   #make class members for  Weight?
        self.description=description
        self.name=name
        self.partOf=deepcopy(partOf)
        self.inventory=deepcopy(inventory)
        self.isContainer=isContainer
        self.isOpen=isOpen
        self.hitPoints=hitPoints
        self.withVerbs=withVerbs
        self.damage=None
        self.size=None
        self.containerSize=None
        self.isLocked=isLocked
        self.lockedBy=lockedBy
        self.surfaceSize=surfaceSize
        self.surface=surface
        self.smell=smell
        self.taste=taste
        self.texture=texture
        self.isEdible=isEdible
        self.weight=weight

class gameClock(item):
    gameCount=0

#TYPES OF ITEMS
class door(item):
    goesTo=""
    lockedBy=""
    otherSide=[]
    #isLocked="False" #Need a container inherited class or if condition will derail open command for things that don't have locks.
    def blockPlayer(self):
        if self.isOpen == False:
            print(self.name)
            return False
        elif self.isOpen == True:
            return True

woodenDoor=door("It's a sturdy door made of thick oak planks.",["wooden door", "wood door", "sturdy door", "oak door", "oaken door", "door"])
woodenDoor.goesTo=""
woodenDoor.direction=""
woodenDoor.lockedBy="brass key"
woodenDoor.isContainer=True
woodenDoor.isOpen=True

trapDoor=door("It's a square wooden door in the floor with a metal handle",["trap door", "door on floor", "door on ground"])
trapDoor.isContainer=True

steelDoor=door("It's a thick door of solid steel.",["steel door", "metal door", "door"])
steelDoor.isContainer=True

class key(item):
    unlocks=[]
    unlockName=""
    def unlock(self, door):
        door.isOpen=True

brassKey=key("It's an old brass key.",["brass key", "metal key", "key"])
brassKey.unlocks=woodenDoor
brassKey.unlockName="wooden door"
brassKey.size=1

#PLAYER CHARACTER (IN PRINCIPLE AN ITEM SO FAR)

hands=item("Your hands are delicate and slender like those of an artist or musician."
           "\nThey are soft and uncalloused.", ["hands", "hand", "my hands"])
leftHand=item("Your left hand is distinguished by a small freckle.", ["left hand", "my left hand"])
eyes=item("You can't see your own eyes, moron.\nAnd don't count on me, the narrator, to tell you.", ['eyes', 'eye', 'my eyes'])
penis=item("You look down and see a long-ish, thin member dangling between your legs resting upon your hairy scrotum.",
["my dick", "my weiner", "my schlong", 'my penis', "my member", 'dick', 'penis', 'schlong', 'member'])
torso=item("Your body is slight pudgy but more or less slender.",["torso", "body", "my body", "my torso"])
legs=item("Your legs are thin and somewhat hairy but not disgustingly so.",["legs", "my legs"])
head=item("""Your head is a typical human head topped with some hair that could use a haircut.  Human heads are
vulnerable to attack so you'd do well to protect it""", ["head", "my head", "noggin"])

playerBodyParts=[hands, leftHand, eyes, penis, torso, legs, head]
player=item("You are a man with an ordinary frame.", ["yourself", "player", "me", "myself", "person"],
deepcopy(playerBodyParts), isContainer=True)
player.clothesDescription="You are naked."
player.equippedWeapon=None
player.hitPoints=3
player.isAlive=True #causes game to quit when changed to False
player.size=5
player.armor=None
player.dodge=1
player.texture="You feel like flesh and slick, salty sweat."
player.smell="You smell like strong body odor, in other words, musk, pheromones, and a bit of onions"
player.taste="You taste like soot and poo."
player.emptyStomach=True
player.poopTimer=0
player.weight=5
player.isAwake=True
player.isPoisoned=False
player.poisonCount=None
player.hurtByFists=True
#inventory= [] #I'm using the one in commands for convenience

#THE NARRATOR
narrator=item("""You can't see the narrator but you can almost feel a tingling by your right ear where his voice
comes from.  My voice is powerful, commanding, soothing, and melodious.  Ok, ok maybe not but I try.""",
["narrator", "speaker", "storyteller", "dm", "story teller", "voice"])


#INTRINSIC PARTS OF A ROOM

wall=item("The walls are bare and gray.", ["wall", "walls"])
floor=item("The floor is bare and gray.", ["floor", "ground", "floors"])
floor.isSurface=True
floor.surfaceSize=1000
floor.surface=[]
ceiling=item("The ceiling is bare and gray.", ["ceiling", "up", "roof"])
#intrinsicItems= {'player':player, 'wall':wall, "floor":floor, "ceiling":ceiling}
intrinsicItems= [player, wall, floor, ceiling, narrator]
#FURNITURE

#SURFACES
#heavy wooden table
woodenTable=item("It's a sturdy oaken table worn down by time and the elements.",["table", "wood table", "wooden table"])
woodenTable.isSurface=True
woodenTable.surfaceSize=6
woodenTable.surface=[]
woodenTable.weight=7

#bar (for serving food and drinks
servingBar=item("It's a wooden bar for serving food and drink.  It's in the typical L-shape.",
["bar", "counter", "bar counter"])
servingBar.isSurface=True
servingBar.surfaceSize=15
servingBar.surface=[]

#CHAIRS

#lounge chair
loungeChair=item("It's a lounge chair with a red cushion that's pleasant to sink into.",["lounge chair", "chair"])
loungeChair.hitPoints=3
loungeChair.size=5
loungeChair.isSurface=True
loungeChair.surface=[]
loungeChair.surfaceSize=5
loungeChair.weight=3

#bar stool
barStool=item("It's a bar stool elevated so that a bar is at elbow-height.",["stool", "bar stool", "barstool"])
barStool.hitPoints=3
barStool.size=5
barStool.isSurface=True
barStool.surface=[]
barStool.surfaceSize=5
barStool.weight=3

#LADDERS

#steel ladder
steelLadder=item("It's a steel ladder welded into place.",["ladder","steel ladder", "metal ladder"])



#write method that blocks user from going to other room while door is closed.

##ROOM ITEMS##

#STARTING ROOM ITEMS

turd=item("It's brown, squishy, and smells like shit.", ["turd", "poop", "shit", "piece of crap"])
turd.hitPoints=1
turd.size=1
turd.weight=1

pebble=item("It's a perfectly round pebble.",["pebble", "rock", "stone"])
pebble.size=1
pebble.weight=1

#part of goldenknife first
handle=item("The handle has a grip but is otherwise unadorned", ["knife handle", "handle of knife", "handle on knife"])
goldenKnife=item("It is a flawless pure gold butter knife that shines even in dim lighting.  It's completely plain with no words or decoration carved on it.",
["knife", "golden knife", "gold knife", "butter knife", "gold butter knife"], [handle])
goldenKnife.damage=1 #Damage = damage+1.  hit.action() takes 1 hp by default.
goldenKnife.size=1
goldenKnife.weight=1

woodenBox=item("It's a wooden box that has a lid.", ['box', 'wooden box', 'wood box', 'the box', 'the wooden box'], [] ,[], isContainer=True)
woodenBox.hitPoints=3
woodenBox.size=4
woodenBox.containerSize=3
woodenBox.weight=3


#NORTH ROOM ITEMS
icicles=item(
"""It's a sheet of icicles and frozen frost covering what appears to be a grey marble plaque set in
an alcove in the north wall of ice.  You think there may be something written on the plaque but
you are unable to read it through all the ice.  The whistling winter winds sweeping through the room
constantly deposit even more ice.  With considerable effort you may be able to clear away the ice.""",
["cluster of icicles","icicles","ice", "frost", "sheet of ice","frost sheet", "ice sheet", "frozen frost"])
icicles.hitPoints=4
icicles.size=6
marblePlaque=item(
"""The plaque is set in an alcove in the north wall.  The winter winds scouring the chamber constantly
leave deposits of icicles that obscure the plaque.  You can't make out any details.""",
["plaque", "marble plaque", "marble", "stone placque"])
marblePlaque.size=5
alcove=item(
"""There is an indentation carved out of the north ice wall with a grey marble plaque set in it.  The
plaque is almost completely obscured by icicles and sheets of ice.""",["alcove", "indentation"])

#EAST ROOM ITEMS

plasticFlamingo=item("It's a blindingly neon pink plastic flamingo used for decorating lawns.",
                 ["plastic flamingo","flamingo", "bird", "plastic bird"])
plasticFlamingo.hitPoints=2
plasticFlamingo.size=2
plasticFlamingo.weight=2

#SOUTH ROOM ITEMS
liverWurstSandwich=item("The sandwich appears to be made from liverwurst and cream cheese.",["sandwich"])
liverWurstSandwich.hitPoints=1
liverWurstSandwich.size=1
liverWurstSandwich.isEdible=True
liverWurstSandwich.weight=1

#PUZZLE ROOM ITEMS
steelCage=item("""The steel cage is almost as tall as you but its slats are so close together you can't even
fit your hand through them.""",["steel cage", "cage"])
canSeeInside=True #add clause to list items that can be seen inside things, treat it like surface area.
steelCage.size=5
steelCage.weight=10
steelCage.isContainer=True
steelCage.containerSize=4
steelCage.canSeeInside=True
pulleyMechanism=item("""That's well out of your reach""", ["mechanism", "pulley", "pulleys"])
pulleyMechanism.size=5
thickChain=item("""That's well out of your reach""",["thick chain", "chain"])
thickChain.size=6
thickChain.weight=7

#chain mail shirt under puzzleRoom

    
#ITEMS THAT RELY ON PREVIOUS ITEMS TO BE INITIALIZED
     
class heal(item):
    isHeal=True
    isDisposable=False
    charged=True
    charges=None
    healAmount=1
    fullHealth=3
    rechargeTime=None
    untilCharged=None
    def healPlayer(self):
        player.hitPoints = self.fullHealth
        self.charged=False
        if self.rechargeTime is not None:
            self.untilCharged=gameClock.gameCount+self.rechargeTime
        if self.charges is not None:
            self.charges-=1
            
    def partHeal(self):
        player.hitPoints += self.healAmount
        self.charged=False
        
    def checkCharge(self):
        if self.charges is not None:
            if self.charges < 1:
                print ("The", self.name[0], "has been exhausted.")
                return None
        if self.rechargeTime is not None:
            if self.charged==False:
                if gameClock.gameCount >= self.untilCharged:
                    self.charged=True
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True
    def checkDisposable(self):
        if self.disposable==True:
            return True
        else:
            return False
        

healingObelisk=heal("""It's an obelisk of polished obsidian carved with ancient runes thatpulse with a soft
glow. On front of the obelisk are two hand-shaped indentations.""",
["obelisk of healing", "obelisk", "healing obelisk", "monument", "artifact"])
healingObelisk.rechargeTime=10
healingObelisk.charges=4



#LIVING THINGS

#MONSTER SCRIPTS(BEHAVIOR)

def hostileMonster(monster):
    monster.attackPlayer()

def hostileFlabberGhast(monster):
    #hit=monster.attackPlayer()
    if monster.attackPlayer() == True:
        if random.randint(0, 2)==2:
            print("Suddenly a brown cloud of disease explodes noisily around you. You have been flabberghasted.")
            stuck=input()
            print("")
            print("Unable to move or even blink you watch helplessly as the flabberghast's arms windmill furiously.")
            monster.attackPlayer()
            if player.hitPoints < 1:
                return
            stuck2=input()
            recover=0
            while recover != 1:
                recover=random.randint(0,1)
                if recover != 1:
                  print("You are still flabberghasted.\nA thin scream escapes your paralyzed lips as you stand there at the foul creature's mercy.")
                  print("")
                  monster.attackPlayer()
                  if player.hitPoints < 1:
                      return
                  stillStuck=input()
                else:
                    print("You are able to move again.")

def hostileNinjai(monster):
    if monster.attackPlayer() == True:
        if player.isPoisoned==False:
            player.isPoisoned=True
            player.poisonCount=20
        if player.isPoisoned == True:
            player.poisonCount-=1

def friendlyMagios(monster):
    if monster.hitPoints >= 3:
        pass
    else:
        pass
        #monster.attackPlayer()
        #magios.behavior=hostileMonster       

hostileBehavior=[hostileMonster, hostileFlabberGhast, hostileNinjai]
friendlyBehavior=[friendlyMagios]
            

#MONSTERS

class monster(item):
    isAlive=True
    hurtByFists=True
    attackDescription=None
    hitDescription=None
    missDescription=None
    playerDeathDescription="Alas, you have died."
    deathDescription=None
    behavior=[hostileMonster]#staticmethod(hostileMonster)]#None #adding explicitly later is different because adding it here implicitly adds a "self" variable
    curseReaction=None
    askAbout=None #dictionary
    understands=None #dictionary
    dodge = 1
    toHit = 1
    inventory=[]
    #def __init__(self, damage=1):
    #    super(item).init()
    #    self.damage=damage
    def attackPlayer(self):
        hits=False
        if random.randint(0, player.dodge) == player.dodge: #Changing this determines how likely monster's attacks
            if player.armor is not None:
                armorSave=random.randint(0, 9) #are to hit player
                if armorSave <= player.armor:
                    return print ("Your armor deflects the blow harmlessly.")
            player.hitPoints-=self.damage #amount of damage done by each hit
            if self.attackDescription is None:
                print ("The", self.name[0], "attacks and hits you.")
                if player.hitPoints < 1:
                    return print (self.playerDeathDescription)
                hits=True
                return hits
            else:
                print (self.attackDescription)
                if player.hitPoints < 1:
                    return print (self.playerDeathDescription)
                hits=True
                return hits
                
        else:
            print ("The", self.name[0], "attacks and misses you.")
            print("")
            return hits
#PEPTO BISMOL GLOP, no special abilities yet but will lack attackable body parts
peptoBismolGlop=monster("""It looks like a bright pink blob with slightly darker eyespots.
You can't identify any specific body parts in its amorphous form.""",
["pepto bismol glop", "blob", "ooze", "glop", "slime"])
peptoBismolGlop.hitPoints=3
peptoBismolGlop.damage=1
peptoBismolGlop.attackDescription = """The pepto bismol glop hits you with its goopy pink pseudopodia.
"""
peptoBismolGlop.playerDeathDescription="Still thrashing feebly, you succumb to the glop's grasping gooey tendrils.\nThe last thing you ever feel is a terrible burning as it begins to digest you.  THE END."
#peptoBismolGlop.behavior=hostileMonster #Inherits hostileMonster by default.
peptoBismolGlop.hitDescription="""The pepto bismol glop recoils from your blows with a soupy gurgle.
"""
peptoBismolGlop.deathDescription="With a gurgly groan the glop collapses into a puddle of bright pink ooze\nwhich then quickly evaporates."

#FLABBERGHAST, has a nasty ability to stun player, tougher than a regular human.    
flabberGhast=monster("""It has a frame that might once have been human, at once bulky and twisted.
Its skin is a sickly, greasy gray. It has sharp black claws on its hands and a lipless mouth full of
sharp teeth. It smells overwhelmingly of death, decay and stagnant water.
You'd be unwise to face this beast without a weapon or protection.
""", ["flabberghast", "ghast", "undead", "zombie","ghoul"])
flabberGhast.hitPoints=4
flabberGhast.damage=1
flabberGhast.hurtByFists=False
flabberGhast.behavior=[hostileFlabberGhast]
flabberGhast.attackDescription="""With a gravelly snarl the flabberghast slashes you with its needle-sharp, filthy claws.
"""
flabberGhast.hitDescription="""You wound the flabberghast and it gives out an inhuman yowl of fury.
"""
flabberGhast.deathDescription="""With a terrible groaning that sounds as though it came from lungs filled
with frothy putrid phlegm, the torn frame of the flabberghast falls backwards and remains still.  Its form
then dissolves into a cloud of ash that drifts away before your eyes."""
flabberGhast.playerDeathDescription="""Your despairing wail is cut short as the flabberghast tears you off your feet and
begins to devour you where your broken, unresisting body now lies. It's in no particular
hurry to kill you, so you watch in horror as it tears you apart until...THE END"""


#GIGGLER
giggler=monster("""Barely two and a half feet tall but nimble, also known as the reticulated cave clown.
It habitually bares its yellow teeth in a Glasgow smile with git-like pointy ears, dark grey
skin, and bulging, maniacal eyes.  In one hand it holds a knife.
It moves so quickly you probably want to find a way to slow it down.
""",
["giggler", "clown", "jester", "cave clown", "reticulated cave clown","goblin", "git"])
giggler.hitPoints=2
giggler.dodge=5
giggler.damage=1
giggler.attackDescription="""With shrill disconcerting giggles that echo off the cave walls.  The giggler slashes
you with its knife as it darts past you. "Haaaa Haaa!"  It taunts with gloating glee.
"""
giggler.playerDeathDescription="""With a final slash from the tiny fiend's wicked knife your legs finally collapse
underneath you.  The giggler stares down at you in gloating triumph with its crazy pasted-on smile spreading even
wider. Ahahahaahhehehehehehe! Its obnoxious tittering reaches a new crescendo as it raises its blade over its head
with both hands for the killing blow...THE END."""
giggler.missDescription="""HAAAAAA haaaaa hehehe!  Nanna canna hit meee!  The giggler taunts with a high
shrieking, cracking, cackling voice.
"""
giggler.deathDescription="""The cruel, tittering laughter of the giggler becomes a high, deafening screech of pain
as it collapses to the floor in a tiny, spasmodically twitching heap.  As soon as it stays motionless it
fades away.  The foul git's knife is all that remains.
"""
#giggler.behavior=hostileMonster
giggler.hitDescription="""The git's mockery is interrupted with a scream of pain and fury as you hit it.
"""
giggler.inventory.append(deepcopy(goldenKnife))
giggler.understands=({"hi":"Hihiihihihihi! DIEIEIEIEDIEEEEE!", "go away":'"Nah ah ah! Hahaha!" chastises the giggler.' })
giggler.understands.update({"aha":"""Often those who jest most can't take a joke.  As soon as the word leaves
your mouth, the cave clown screeches in rage and sorrow.  Just a moment ago
almost too quick for your reflexes to follow, the giggler is now blinded by
tears and visibly demoralized.  It should be a lot easier to catch now."""})
giggler.curseReaction='"Rakaneetsu!!" the giggler retorts defiantly.'
giggler.askAbout={"me":"I kill you before! Kill again ahaahaha!"}


#THE MAGIOS
magios=monster("""The magios stands before you.  He wears a dark blue robe with hood. The hood
hides the upper half of his face, but you can readily see a strong chin and a cynical
smile.""",["magios", "mage", "wizard"])
magios.behavior=[friendlyMagios]
magios.hitPoints=3
magios.damage=3
magios.dodge=1
magios.attackDescription="""Your only warning is hairs standing up on the back of your neck before the magios
sends a bolt of lightning right into you."""
magios.hitDescription="""The magios screams in agony and clutches his wound as he doubles over."""
magios.missDescription="""'You will have to do better than that, creature!', says the magios as he dodges your best
attempt at an attack."""
magios.playerDeathDescription="""You are unable to move away as the magios shocks you with streams of lightning.
The room rings with the magios' rich, powerful laughter.  The last sensation you ever know
is the smell of your own burning flesh."""
magios.deathDescription="""In disbelief the magios clutches at his wounds.  His mouth contorts in horror
as he begins to realize his wounds are fatal.  In an attempt to take you down with him he tries to
obliterate you with a last great lightning bolt.  He loses control of the energies he's trying to gather
and crumples pathetically to the floor.  He lingers on a short while longer before finally lying still.
A great shockwave of bright light fills the room and then fades.  When you can finally see again, no trace of
the magios' body remains."""
magios.understands=({"hi":"Greetings. I have been waiting for you here."})
magios.curseReaction="You are unwise to address me in such a fashion. You have no idea HOW unwise."
magios.askAbout={"me":"You are a construct made to serve the trickster God."}

#GREATER IMP
greaterImp=monster("""The greater imp has a human form but with wider shoulders, armored skin, and horns on its knees and elbows.
It shimmers back and forth between a more monstrous form and a nearly human form. Something about
it reminds you of yourself, strangely enough.""", ["greater imp", "imp"])
greaterImp.hitPoints=5
greaterImp.dodge=2
greaterImp.damage=1
greaterImp.hurtByFists=False
#greaterImp.behavior=hostileMonster
greaterImp.attackDescription="""With almost inhuman speed the greater imp lunges at you and in mid-lunge its fingers
transform into claws that tear into your flesh like knives."""
greaterImp.playerDeathDescription="""Your flesh torn to shreds, the blood loss finally too much, you collapse to the floor.
Before you pass out, you hear a voice hiss "And you thought you would repace me!" THE END."""
greaterImp.deathDescription="""The imp lets out horrendous shrieks and falls to the floor.  "It cannot be! I was chosen!" it screams.
"You were." says the Magios drily.
"Save me.  Give me another chance!"
As its speech becomes an incoherent gurgling of blood, the magios only reply is to turn his back on the greater imp and
face you instead."""
greaterImp.missDescription="""The greater imp dodges your attack and hisses at you with fury."""
greaterImp.curseReaction="""The greater imp hisses "I will remember that when I look into your lifeless eyes." """


#BLOWDART NINJAI
blowDartNinjai=monster("""A man clad in concealing black clothing hangs from the ceiling by a grappling hook well out
of your reach.  With one hand he holds onto his rope and in the other he holds a blowdart gun to his mouth aimed in
your direction.""",["blowdart ninjai", "ninja", "ninjai"])
blowDartNinjai.behavior=[hostileNinjai]
blowDartNinjai.hitPoints=1
blowDartNinjai.damage=0
blowDartNinjai.dodge=1
blowDartNinjai.attackDescription="""Thwoohnt!  Suddenly you feel a sharp pain.  You then bat away a small projectile
from your skin with the back of your hand.  "Oops! Dart in the neck." says the Ninjai."""
blowDartNinjai.missDescription="""Even though the ninjai hangs from the ceiling by his rope, well out of your reach,
you still swing wildly in his direction anyway.  "You seem kind of pissed off, buddy." says the ninjai in a
conversational tone. Maybe you could use some feelgood juice." """
blowDartNinjai.deathDescription="""The ninjai gives a bloodcurdling Wilhelm scream as your projectile knocks him loose
from his perch on the ceiling.  He hits the ground awkwardly and you hear his neck snap like a twig. Then, his sprite
flashes for a few seconds before disappearing."""
blowDartNinjai.curseReaction


#WEARABLE ITEMS, CLOTHING/ARMOR
class clothing(item):
    isClothing=True
    warmth=None
    armor=None
    wornOn=None

pinkBathrobe=clothing("""It's a bright pink, plush and fuzzy bathrobe.""",["pink bathrobe", "bathrobe", "robe"])
pinkBathrobe.warmth=3
pinkBathrobe.wornOn="torso"
pinkBathrobe.size=2
pinkBathrobe.weight=2

chainMailShirt=clothing("""It's a shirt of chainmail that offers some protection in a fight.""",
["shirt of chainmail","chainmail", "chain mail", "armor"])
chainMailShirt.armor=1
chainMailShirt.wornOn="torso"
chainMailShirt.size=3
chainMailShirt.weight=3
