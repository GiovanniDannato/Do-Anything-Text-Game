#CURRENT PROBLEMS:
#Be able to ask magios questions (need to learn how to call parent class __init__ properly
#read command for plaques, right now, is just "look at" equivalent
#be able to take off clothing
#get rid of player from intrinsicItems!  Having it in two places is a disaster
#when putting an item with an item on it on a table it doesn't reset containerSize
#implement drinking beverages.  Go pee later?
#Have " and " trigger the end of a statement, start reading a new statement AND check if it's part of the same statement.
#"You can't take part of an item" error
#Hook up open/close to more recent IO.  Can't use "and" for modifier sentence structure
#Write GetLastItem, to read multiple word nouns.(Or just use afterModifier?)
#Make a modifier loop instead of having an if statement for each modifier!
#Be able to target body parts with lower probability of hitting but more damage like fallout?
#when drunk do random actions?
#anything thrown at glop gets stuck in its inventory
#add another step to ninjai puzzle: have to put things in box to make it heavier
#MORE TENTATIVE
#if player input off by one letter "tae" instead of "take", "Did you mean to say take?"  y or no
#If someone types in "turd" by itself: "What do you want to do with the turd?  Same with isolated verbs"
#Open door with key automatically if you have it.


#CONTENTS

    #- GAME LOOP
    #ask for input
    #move
    #quit
    #single word command
    #command + modifier + object
    #verb object
    #isNonsense filter "I don't know what that means"

#IMPORT LIBRARIES
#from copy import deepcopy
from move import directions, north, south, east, west, allDirections
import items
import commands
import rooms
import random
        


#BEGINNING OF GAME

quit=False #The game loop continues so long as it stays this way.
items.gameClock.gameCount=0
print("""Hi, I will be your narrator today.  Ahem...let's get started, shall we? I was appointed
to your case by the narrator's guild so there's no use protesting.  Here we go...
""")
programStart=print(rooms.currentRoom.description) #Describes starting room
if rooms.currentRoom.items != []:
    describeItemsInRoom=0
    for item in rooms.currentRoom.items:
        print("There is a " + rooms.currentRoom.items[describeItemsInRoom].name[0] + " here.")
        if item.isSurface==True:
            if item.surface is not None:
                if item.surface != []:
                    commands.listSurfaceItems(item)
        describeItemsInRoom=describeItemsInRoom+1
    commands.listAllFurnitureSurfaceItems(rooms.currentRoom.furniture)
    if rooms.currentRoom.monsters != []:
        for monster in rooms.currentRoom.monsters:
            print("You see a", monster.name[0], "here.")


                   
while quit is False: #PROGRAM LOOP STARTS HERE IF THIS ISN'T WORKING, NO GAME
    items.player.inventory=commands.inventory
    isNonsense=True #if input recognized as a valid command, gets set to false

    if rooms.roomTimer >= 1:
        if rooms.currentRoom.scripts is not None: #if room has a special behavior
            for script in rooms.currentRoom.scripts:
                script(rooms.roomTimer)
        if rooms.currentRoom.monsters != []:
            for monster in rooms.currentRoom.monsters:
                for behavior in monster.behavior: #was a list but created overlapping variables
                    #monster.behavior(monster)
                    behavior(monster)
    if items.player.emptyStomach==False:  #Player digests food
        items.player.poopTimer+=1
        if items.player.poopTimer == 12:
            print("Now that your earlier meal has been fully digested, you have to go poop.")
        if items.player.poopTimer == 17:
            print ("You writhe in pain and discomfort.  You urgently need to void your bowels.")
        if items.player.poopTimer ==21:
            print ("""You scream as terrible pain lances through your abdomen.  You desperately
need to poop.""")
        if items.player.poopTimer ==23:
            print("""You scream to the heavens as your intestines finally rupture from the strain
of holding accumulated waste.  You can only lay there unable to move as your blood starts to
go septic from exposure to your own feces.  Your last day is agonizing, let's leave it
at that. THE END.""")
            input()
            items.player.isAlive=False
            break

    if items.player.isPoisoned==True:  #Deals with the ninja's sleeping poison
        if items.player.poisonCount==0:
            items.player.isAwake=False
            items.player.isPoisoned=False
        else:
            if items.player.poisonCount==10:
                print("""You are starting to feel peaceful and sleepy from the ninjai's darts.
""")
            if items.player.poisonCount==5:
                print("""Suddenly you feel yourself being dragged by exhaustion and you know you won't be able to stay
awake much longer.  Whatever was on the ninjai's darts seems to have drugged you.
""")
            items.player.poisonCount-=1

    if items.player.isAwake==False:
        if rooms.currentRoom.monsters != []:
            for monster in rooms.currentRoom.monsters:
                if monster.behavior in items.hostileBehavior:
                    print("""With the last of your willpower you try to stay awake but it's no use.  Drugged by the ninjai's darts,
a deep and restful euphoria steals over you even though you know you are in mortal danger.  One more attempt to make it to the
next room but you fall to the floor, your vision growing watery and clouded.  As your eyes finally seal shut, some
part of you still screams with the terrible knowledge that you will never wake up.  Your enemies will make short
work of you while you're unconscious. THE END.""")
                    items.player.isAlive=False
                    input()
                    break
                
        if rooms.currentRoom.name=="northRoom":
            print("""Oh no, suddenly you realize the soporific effects of the ninjai's darts have finally caught up with you and
you suddenly find you can't move any farther.  Your sense of creeping horror at your situation is muted by waves of peaceful
euphoria.  Thhwiwiwieewwwwwww!  Shriek the winter winds.  You know if you fall asleep here, you will become a
human popsicle long before you wake up again.  Unable to walk now, you try to crawl.  The south door is
right in front of you now.  Almost... Almost...almost. THE END""")
            input()
            items.player.isAlive=False
        if items.player.isAlive is False:
            break


        elif items.player.isAlive is True:
            items.player.isAwake=True
            print("""Drugged by the ninjai's darts. You find yourself sinking into a state of euphoria and then fall into a
deep sleep.  When you wake up, you cannot even guess how long you must have been out.""")
            
                
    if items.player.hitPoints < 1:
        input()
        break  #If you're dead, game ends
    if items.player.isAlive==False: #For things that kill you instantly
        input()
        break
        
    rooms.roomTimer+=1 #time spent in room for room scripts.
                        #set to 0 again by commands.enterRoom()
    
    prompt=input().lower().strip() #This is where all player input is entered.  Lower so there's no problems with case sensitivity
    print("")

    #Go to next room if there's a door, or be stopped by a wall, gives a description of what happens
    isBlocked=False
    validDirection=False
    for direction in allDirections: # e, w, s, n 
        for goDirection in allDirections[direction]: #every way it could be referred to  
            if prompt == goDirection:  #User input is a valid direction
                isNonsense=False
                for room in rooms.currentRoom.nextRoom:
                    #print("goDirection is", goDirection)
                    #print("nextRoom directions are", rooms.currentRoom.nextRoom[room])
                    if goDirection in rooms.currentRoom.nextRoom[room]:#dict key gets direction, is it possible to go that way?
                        #print("made it inside direction if")

                        validDirection=True
                        if rooms.currentRoom.door != []: #Is there a door here, in the next room?
                            for door in rooms.currentRoom.door:
                                if door.goesTo==room.name: #Is there a door in the direction you're trying to go?
                                    #print ("Goes To equals:", room.name) Important that room name matches exactly or no door
                                    if door.isOpen is False:  #Is the door open?
                                        isBlocked=True
                                        print ("You can't go that way because the door is closed.")
                                        break
                        break #will pass on wrong direction if it keeps iterating.

                
                if isBlocked==False:  #Successfully go to another room
                    print(rooms.currentRoom.allDirections[direction][goDirection]) #prints go in direction description
                    if validDirection==True:
                        rooms.currentRoom=room
                        #rooms.currentRoom.door=room.door#reassigns currentRoom to new room
                        commands.enterRoom(rooms.currentRoom) #prints out description and items of new room
                      


   #quit the program yes or no    
    if prompt in commands.quitProgram:
        isNonsense=False
        
        prompt=input("Are you sure you want to quit?\n")
        if prompt in commands.yes:
            print("Good bye, Sailor")
            input()
            break
        if prompt in commands.no:
            pass

    #If player uses curse words
    if prompt in commands.expletives:
        if rooms.currentRoom.monsters == []:
            print (random.choice(commands.retort))
    if prompt in commands.slurs:
        raceRetort=["I will not stand for discrimination.", "Racist scum!", "Racist!",
        "I'm a narrator, I don't have a racial background.", "Dungeons are equal opportunity."]
        print(random.choice(raceRetort))
    

    #Look at inventory or look at room, most basic commands
    if prompt in commands.lookAndInventory:
        for command in commands.lookAndInventory:
            if prompt == command:
                isNonsense=False
                commands.lookAndInventory[command].action()
          
    
    if prompt not in rooms.currentRoom.allDirections:
        if prompt not in commands.programCommands:
            if isNonsense==True:
                if prompt not in commands.expletives:
                    if prompt != "":
                        verb=commands.findAllVerbs(prompt)
                        if verb is not None:
                            isNonsense=False
                            hasModifier=False
                            if ' in ' in prompt: #I need to write a loop to handle all these.
                                #hasModifier=True #interferes with look in
                                if commands.verbs[verb].inAction is not None:
                                    hasModifier=True
                                    commands.doIn(prompt)
                            if ' from ' in prompt:
                                #hasModifier=True
                                if commands.verbs[verb].fromAction is not None:
                                    hasModifier=True
                                    commands.doFrom(verb, prompt)
                            if 'put on ' not in prompt:
                                if ' on ' in prompt:
                                    #hasModifier=True
                                    if commands.verbs[verb].onAction is not None:
                                        hasModifier=True
                                        commands.doOn(verb, prompt)
                                    
                            
                            if ' with ' in prompt:
                                hasModifier=True
                                if commands.verbs[verb].withAction is not None:
                                    commands.doWith(prompt)
                                    
                            if hasModifier == False:
                                commands.verbs[verb].checkInput(verb, prompt) #sends input to command
                    
                            if ' and ' in prompt:
                                secondPhrase=commands.afterAnd(prompt)
                                secondVerb=commands.findAllVerbs(secondPhrase)
                                if secondVerb is not None:
                                    commands.verbs[secondVerb].checkInput(secondVerb, secondPhrase)


        
    #unrecognized input gets "I don't know what that means"
    if prompt not in rooms.currentRoom.allDirections:
        if prompt not in commands.programCommands:
                        if isNonsense==True:
                            if prompt != '':
                                if prompt not in commands.expletives:
                                    if prompt not in commands.slurs:
                                        print("I don't know what that means")
    items.gameClock.gameCount+=1



#https://github.com/krieghan/archmage/blob/master/rooms/room.py
#https://github.com/krieghan/archmage
"""If you define a __init__ on the child class, though,
you have to explicitly call the parent class's __init__ if you want it to be
called
It's something like this:
super(MyClassName, self).__init__(*args, **kwargs)
Put that in the first line of the child __init__
That's true
Anything in __init__ is only going to be on instances"""
