import rooms
import items
import random


class roomCommand:
    withAction=None
    inAction=None
    fromAction=None
    onAction=None
    def __init__(self, name, description, error, action):
        self.name=name
        self.description=description
        self.error=error
        self.action=action
        #self.withAction=withAction
        #self.inAction=inAction


#CREATING ROOM COMMANDS
#each command uses a checkInput, error, and action methods, in that order.

#TAKE
class take (roomCommand):
    name = "take"
    description= "You take the "

    def allAction(prompt):  #Allows player to take all items at once
        itemCount=findItemCount()
        if itemCount == 0:
            print( "There's nothing you can take.")
        else:
            if rooms.currentRoom.monsters == []:
                notEverything=False
                while itemCount > 0: #rooms.currentRoom.items:
                    if rooms.currentRoom.items[0].size < 5:
                        inventory.append(rooms.currentRoom.items[0])
                        del rooms.currentRoom.items[0]
                    else:
                        notEverything=True
                    itemCount-=1
            else:
                return print ("You can't take anything while there's monsters here.")
            if notEverything==False:
                print ("Everything taken.")
            if notEverything==True:
                print ("Some of the things you tried to take are too big.") 
               
    def checkInput(verb, prompt):
        #takeThing=getPromptItem(prompt)
        #if takeThing is not None:
        #    if takeThing.size is None:
        #        return print("You can't take the ", takeThing.name[0]+".")
                
        itemCount=checkRoom(prompt) #Returns item index number or None

        if findVerbSubject(prompt) in all:
            itemCount=verbs[verb].allAction(prompt)
            return
        if rooms.currentRoom.monsters == []:
            #verb=findAllVerbs(prompt)
            if itemCount is not None:
                takeThing=getPromptItem(prompt)
                if takeThing.size >=5:
                    return print("The", takeThing.name[0],"is too big to take.")
                else:
                    return verbs[verb].action(itemCount)
        if itemCount is None: #error message if item not in room
            return verbs[verb].error(findRemainingWords(prompt))
        else:
            return print ("You can't take anything while there's monsters here.")

 
            #actionOrError(prompt, itemCount)
                                    
    def error(prompt):
        subject=findRemainingWords(prompt)
        location=getItemLocation(subject)
        if location is not None:
            if rooms.currentRoom.furniture != []:  #checks to see if it's on top of anything in the room, make into method use for doFrom()?
                #containerType=[surface, inventory]
                #containerBoolType=[isSurface, isContainer]
                #currentBool=None
                itemCount=0
                furnitureCount=0
                for thing in rooms.currentRoom.furniture:
                    if thing.isSurface==True:
                        for item in thing.surface:
                            for name in item.name:
                                if subject == name:
                                    takeThing=getPromptItem(prompt)
                                    if takeThing.size >=5:
                                        return print("The", takeThing.name[0],"is too big to take.")
                                    return take.fromFurnitureAction(thing, item, furnitureCount, itemCount)
                            itemCount+=1
                    furnitureCount+=1
            containerLocation=getTransparentContainerLocation(subject)        
            containerIndex=getTransparentContainerIndex(subject, containerLocation)
            if containerLocation is not None:
                container=containerLocation[containerIndex]
                if container.isContainer==True:
                    if container.canSeeInside==True:
                        itemIndex=getItemIndex(subject, location)
                        takeThing=containerLocation[containerIndex].inventory[itemIndex]
                        #takeThing=getPromptItem(prompt)
                        if takeThing.size >=5:
                            return print("The", takeThing.name[0],"is too big to take.")
                        else:
                            return take.fromTransparentContainer(container, takeThing, containerIndex, itemIndex, containerLocation)
                    

                                             
        alreadyHave=False
        isHere=False
        itemNumber=0
        verbSubject=findRemainingWords(prompt)
        for item in inventory:      #checks if item is inventory when you try to take it
            nameCount=0
            for name in item.name:
                if verbSubject == item.name[nameCount]:
                    alreadyHave=True
                    print("You already have the " + item.name[0])
                    break
                if alreadyHave == True:
                    break
                nameCount=nameCount+1
            itemNumber=itemNumber+1
        if alreadyHave==False:
            for item in rooms.currentRoom.intrinsicItems:
                for name in item.name:
                    if verbSubject == name:
                        if item.name == "player":
                            print("You can't take yourself, dumbass.")
                            isHere=True
                            break
                        else:
                            print("You can't take the " + findVerbSubject(prompt))
                        isHere=True
                        
            if isHere==False:
                locations=[rooms.currentRoom.monsters, rooms.currentRoom.furniture, rooms.currentRoom.door]
                for location in locations:
                    if location != []:
                        for item in location:
                            for name in item.name:
                                if verbSubject == name:
                                    return print("You can't take the", item.name[0])
                        
                print("There is no " + findVerbSubject(prompt) + " here.")
        

    def action(itemCount):#itemCount, objectName):
        print(take.description + rooms.currentRoom.items[itemCount].name[0])
        inventory.append(rooms.currentRoom.items[itemCount]) #adds item to inventory
        del rooms.currentRoom.items[itemCount] #deletes item you just picked up from the room

    def fromCheckInput(item, container, itemIndex):
        if container.isOpen==True:
            take.fromAction(item, container, itemIndex)
        elif container.isOpen==False:
            print("The",container.name[0],"is closed.")
    
    def fromAction(item, container, itemIndex):
        print("You take the", item.name[0], "from the", container.name[0]+".")
        inventory.append(item)
        container.containerSize=container.containerSize+item.size
        del container.inventory[itemIndex]

    def fromFurnitureAction(furniture, item, furnitureCount, itemCount):
        print(take.description + rooms.currentRoom.furniture[furnitureCount].surface[itemCount].name[0])
        inventory.append(rooms.currentRoom.furniture[furnitureCount].surface[itemCount]) #adds item to inventory
        furniture.surfaceSize += item.size
        del rooms.currentRoom.furniture[furnitureCount].surface[itemCount] #deletes item you just picked up from the room

    def fromTransparentContainer(container, item, containerCount, itemCount, location):
        if container.isOpen==True:
            print(take.description + location[containerCount].inventory[itemCount].name[0])
            inventory.append(location[containerCount].inventory[itemCount]) #adds item to inventory
            location[containerCount].containerSize += item.size
            del location[containerCount].inventory[itemCount] #deletes item you just picked up from the room
        else:
            print("You can see the", item.name[0], "but you can't get it while the", container.name[0], "is closed.")
                    
#DROP
class drop (roomCommand):
    name="drop"
    description= "You drop the "

    def allAction(prompt):  #Allows player to take all items at once
        if inventory == []:
            print( "There's nothing to drop.  Your inventory is empty.")
        else:
            while inventory != []:
               rooms.currentRoom.items.append(inventory[0])
               del inventory[0]
            items.player.equippedWeapon=None 
            print ("Everything dropped.")
        return True

    def checkInput(verb, prompt):
        #itemValid=checkInventory(verb, prompt)
        itemCount=checkInventory(prompt)

        if findVerbSubject(prompt) in all:  #Drop all
            verbs[verb].allAction(prompt)
        else:
            actionOrError(prompt, itemCount)
            
        #if itemValid==False: #error message if item not in room
        #    verbs[verb].error(verb, prompt)

    def error(prompt):
        isHere=False
        for item in rooms.currentRoom.items:
            for name in item.name:
                if findVerbSubject(prompt) == name:
                    print("You don't have the " + findVerbSubject(prompt) +".")
                    isHere = True
                    break
      
        intrinsicIndex=checkIntrinsicItems(prompt)
        if intrinsicIndex is not None:
            if "yourself" in rooms.currentRoom.intrinsicItems[intrinsicIndex].name:
                return print("You throw yourself to the ground in an impressive display of self-abasement.\n"
                "Then you get back up.")
                isHere=True
            else:
                print("You can't take the " + findVerbSubject(prompt) + ", therefore"
                " you'll never be able to drop it.")
                isHere = True
        if isHere == False:
            print ("There is no " + findVerbSubject(prompt) + " here.")

    def action(itemCount):
        item=inventory[itemCount]
        itemName=item.name[0]
        print(drop.description + itemName) #find how to get index number for a specific dict item
        rooms.currentRoom.items.append(item)
        if items.player.equippedWeapon is not None:
            if itemName == items.player.equippedWeapon.name[0]:
                items.player.equippedWeapon=None
        del inventory[itemCount]

#SAY
class say(roomCommand):
    name="say"
    description="You say "

    def checkInput(verb, prompt): 
        say.action(cutFirstWord(prompt))
        #say.action(findRemainingWords(prompt))
    def action(words):
        print(words + ", you say.")
        checkWords(words)

#SCREAM
class scream(roomCommand):
    name="scream"
    description="You scream until your throat starts to get hoarse.  I'd rather you stopped that."
    def checkInput(verb, prompt):
        words=findRemainingWords(prompt).upper()
        scream.action(words)
    def action(words):
        print(words + ", you scream.")
        checkWords(words)

def checkWords(words): #for scream and yell
    ahaWords=["aha", "aha!",'"aha"','"aha!"' ]
    hiWords=["hi", "hello", '"hello"','"hi!"']
    leaveWords=["go away", "get out of here", "leave"]
    narratorUnderstands={"hi":"Why hello, I'm amazed someone is actually talking to me, the narrator, for once!"}
    allWords=[ahaWords, hiWords, leaveWords]
    checkExpletives(words)
    for wordList in allWords:
        for word in wordList: #Added on
            if word == words.lower():  #was 'word' instead of sayWord
                if rooms.currentRoom.monsters != []:
                    monsterCount=0
                    for monster in rooms.currentRoom.monsters:
                        if monster.understands is not None:
                            for phrase in monster.understands:
                                if wordList[0]==phrase:
                                    print(monster.understands[phrase])
                        if wordList[0]=="aha":
                            if monster.name[0]=="giggler":
                                disableGiggler(monsterCount)
                        monsterCount +=1
                else: #if no one else in room
                    if wordList[0] in narratorUnderstands:
                        print(narratorUnderstands[wordList[0]])

def checkExpletives(words):
    if rooms.currentRoom.monsters != []:
        for monster in rooms.currentRoom.monsters:
            if words.lower() in expletives:
                if monster.curseReaction is not None:
                    print(monster.curseReaction)
    elif words.lower() in expletives:
        print(random.choice(retort))
                            
                        
def disableGiggler(monsterCount):
    rooms.currentRoom.monsters[monsterCount].dodge=1
    newAttack="""Weeping with shame and rage the cave clown stabs you in the leg"""
    newMiss="""The sad and weepy cave clown barely manages to dodge your attack."""
    rooms.currentRoom.monsters[monsterCount].attackDescription=newAttack
    rooms.currentRoom.monsters[monsterCount].missDescription=newMiss
    newHit="The git screams in rage and pain as your blow lands home."
    rooms.currentRoom.monsters[monsterCount].hitDescription=newHit
    newDies="""With a high, deafening screech of pain the cave clown collapses to the floor in a tiny, spasmodically twitching heap.
As soon as it stays motionless it fades away.  The foul git's knife is all that remains."""
    rooms.currentRoom.monsters[monsterCount].deathDescription=newDies
    

#ASK(ABOUT)
class ask(roomCommand):
    name="ask"
    description="Just ask."

    def checkInput(verb, prompt):
        ask.action(cutFirstWord(prompt))
        

    def action(words):
        meWords=["me", "myself", "player"]
        checkExpletives(words)
        if words in meWords:
            if rooms.currentRoom.monsters != []:
                for monster in rooms.currentRoom.monsters:
                    if monster.askAbout is not None:
                        for topic in monster.askAbout:
                            if meWords[0]==topic:
                                return print(monster.askAbout[topic])
        print("I was just assigned to you as your narrator.  I can tell you very little.")

    def aboutCheckInput():
        pass

    def aboutAction():
        pass


                    

    

#INVENTORY    
class lookAtInventory (roomCommand):
    name="inventory"
    description="look at inventory"

    def checkInput(verb, prompt):
        lookAtInventory.action()

    def error():
        pass
    
    def action():
        print ("Your Inventory:")
        for item in inventory:
               print(item.name[0])

#PUT IN(Open Object)
class putIn(roomCommand):
    name = "put in"
    description = "You put the"

    def inCheckInput(prompt, item, container):
        itemName=item.name[0]
        containerName=container.name[0]
        if item.size <= container.containerSize:
            putIn.inAction(item, container)
            return
        if item.size > container.containerSize:
            if container.inventory is not []:
                if container.containerSize != 0:
                    print ("The" , itemName,"doesn't fit.")
                    return
                if container.containerSize == 0:
                    print ("The", containerName, "is full.")
            else:
                print("The",itemName, "is too big to fit in the", containerName)
        else:
            print("There is no", itemName, "here")             

    def error(prompt):
       print("You can't put anything in the" , findLastVerb(prompt))

    def checkInput(verb, prompt):
        pass

    def inAction(item, container):
        container.containerSize=container.containerSize-item.size
        print(putIn.description, item.name[0], "in the", container.name[0])
        container.inventory.append(item)
        itemLocation=getItemLocation(item.name[0])
        del itemLocation[getItemIndex(item.name[0], itemLocation)]

    def onCheckInput(item, furniture):
        itemName=item.name[0]
        furnitureName=furniture.name[0]
        if item.size <= furniture.surfaceSize:
            return putIn.onAction(item, furniture)
        if item.size > furniture.surfaceSize:
            if furniture.surface is not []:
                if furniture.surfaceSize != 0:
                    return print ("The" , itemName,"doesn't fit.")
                if furniture.surfaceSize == 0:
                    return print ("There's no more room on the", furnitureName +".")
            else:
                print("The",itemName, "is too big to fit on the", furnitureName)
        else:
            print("There is no", itemName, "here")  


    def onAction(item, furniture):
        furniture.surfaceSize=furniture.surfaceSize-item.size
        print("You put the", item.name[0], "on the", furniture.name[0])
        itemLocation=getItemLocation(item.name[0])
        index=getItemIndex(item.name[0], itemLocation)
        if furniture.name[0]=="floor":
            rooms.currentRoom.items.append(item)
        else:
            furniture.surface.append(item)
        del itemLocation[index]


#WEAR(PUT ON)
class wear(roomCommand):
    name="wear"
    description="Type this as a verb when you want to wear clothing or armor."

    def checkInput(verb, prompt):
        garment=getPromptItem(prompt)
        if garment is not None:
            
            if garment.isClothing==True:
                wear.action(garment)
            else:
                print("You can't wear a", garment.name[0]+"!")

        else:
            print("You cannot wear what does not exist, unless it's the emperor's new clothes, of course.")

    def action(garment):
        garmentLocation=getItemLocation(garment.name[0])
        indexNumber=getItemIndex(garment.name[0], garmentLocation)
        partCount=0
        finished=False
        for part in items.player.partOf:
            for name in part.name:
                if garment.wornOn == name:
                    bodyPart=items.player.partOf[partCount]
                    finished=True
                    break
            if finished==True:
                break
            partCount+=1
        #if bodyPart.inventory == []: #prevents wearing multiple garments on same body part
        items.player.partOf[partCount].inventory.append(garment)
        if garment.armor is not None:
            if items.player.armor is None:
                items.player.armor=garment.armor
            if items.player.armor is not None:
                items.player.armor+=garment.armor
        #items.player.partOf[partCount].description="You are wearing a", garment.name[0], "on your", bodyPart.name[0] +"."
        items.player.clothesDescription="You are wearing a " + garment.name[0]+"."
        print("You put on the", garment.name[0])
        del garmentLocation[indexNumber]
        #else:
        #    print("You're already wearing a", garment.name[0], "on your", garment.wornOn +".")

#OPEN
class openItem(roomCommand):
    name="open"
    description="You open the "
    
    def checkInput(verb, prompt):
        result=getItem(findRemainingWords(prompt))  #isItemPresent(prompt)
        if result is not None:
            if result.isContainer==True:
                if result.isLocked==False:
                    if findVerbSubject(prompt) in rooms.currentRoom.intrinsicItems[0].name:
                        print ("With a sickening ripping sound, you tear open your stomach and your \n"
                        "intestines spill into a glistening pile on the floor you writhe in agony for \n"
                        "what seems an eternity before you finally expire. THE END")
                        items.player.isAlive=False
                    else:
                        openItem.action(result)
                elif result.isLocked is True:
                    return print("The", result.name[0], "is locked.")
                    
            else:
                openItem.error(result, prompt)
        else:
            openItem.error(result, prompt)


    def error (result, prompt):
        
        if result == None:
            print("There is no " + findVerbSubject(prompt) + " here.")
        else:
            print("You can't open that.")

    def action (item):
        item.isOpen=True
        print(openItem.description + item.name[0] +".")
        item.description=item.description+ " The " + item.name[0] + " is open."


    def withCheckInput(prompt, subjectItem, withItem):
        unlock.withCheckInput(prompt, subjectItem, withItem)
    def withAction():
        pass


#UNLOCK (with command)
class unlock(roomCommand):
    name="unlock"
    def withCheckInput(prompt, subjectItem, withItem):
        if subjectItem.lockedBy==withItem.name[0]:
            if subjectItem.isLocked==False:
                return print("The", subjectItem.name[0], "is already unlocked.")
            if subjectItem.isLocked==True:
                return unlock.withAction(subjectItem, withItem)

        if subjectItem.lockedBy is not None:
            return print ("The", withItem.name[0], "can't unlock the", subjectItem.name[0] )
        if subjectItem.lockedBy is None:
            return print ("The", subjectItem.name[0], "can't be unlocked.")
        
    def withAction(subjectItem, withItem):
        print("You unlock the", subjectItem.name[0], "with the", withItem.name[0] + ".")
        subjectItem.isLocked=False

    def checkInput(verb, prompt):
        return print("You need to try unlocking the", findRemainingWords(prompt), "with something.")

        

#CLOSE

class closeItem(roomCommand):
    name="close"
    description="You close the "

    def checkInput(verb, prompt):
        result=getItem(findRemainingWords(prompt))#isItemPresent(prompt)
        if result is not None:
            if result.isContainer==True:
                if result.isOpen==False:
                    return print("The", result.name[0], "is already closed.")
                    if findVerbSubject(prompt) in rooms.currentRoom.intrinsicItems[0].name:
                        print ("You can't close yourself.")
                      
                else:
                    closeItem.action(result)
            else:
                closeItem.error(result, prompt)
        else:
            closeItem.error(result, prompt)

    def error (result, prompt):
        if result == None:
            print("There is no " + findVerbSubject(prompt) + " here.")
        else:
            print("You can't close that.")

    def action (item):
        item.isOpen=False
        print(closeItem.description + item.name[0] +".")
        item.description=item.description[:-13 + -len(item.name[0])]

    def withCheckInput(verb, subjectItem, withItem):
        lock.withCheckInput(verb, subjectItem, withItem)

    def withAction():
        pass

#LOCK
class lock(roomCommand):
    name= "Lock"
    def withCheckInput(verb, subjectItem, withItem):     
        if subjectItem.lockedBy==withItem.name[0]:
            if subjectItem.isLocked==True:
                return print("The", subjectItem.name[0], "is already locked.")
            if subjectItem.isLocked==False:
                return lock.withAction(subjectItem, withItem)

        if subjectItem.lockedBy is not None:
            return print ("The", withItem.name[0], "can't lock the", subjectItem.name[0] )
        if subjectItem.lockedBy is None:
            return print ("The", subjectItem.name[0], "can't be locked.")

    def withAction(subjectItem, withItem):
        print("You lock the", subjectItem.name[0], "with the", withItem.name[0] + ".")
        subjectItem.isLocked=True

    def checkInput(verb, prompt):
        return print("You need to try locking the", findRemainingWords(prompt), "with something.")
 
#LOOK
class look(roomCommand):
    name="look"
    def checkInput():
        pass
    def error ():
        pass
    
    def action():
        lookAtRoom(rooms.currentRoom)

#LOOK AT
class lookAt(roomCommand):

    name="look at"
    
    def checkInput(verb, prompt):
        #itemExists=False
        #locations=[rooms.currentRoom.items, inventory, rooms.currentRoom.intrinsicItems,
        #rooms.currentRoom.door, rooms.currentRoom.monsters ,rooms.currentRoom.furniture]
        #for location in locations:
        #    if location != []:
        #        inventoryCount=getItemIndex(prompt, location)
        #        if inventoryCount is not None:
        #            itemExists=True
        #            if location[inventoryCount].isSurface==True:
        #                if location[inventoryCount].surface != []:
        #                    surfaceCount=getSurfaceItemIndex(prompt, location[inventoryCount])
        #                    if surfaceCount is not None:
        #                        return lookAt.action(location[inventoryCount].surface[surfaceCount])
        #                    
        #            if location[inventoryCount].partOf == []:
        #                return lookAt.action(location[inventoryCount])
        #            partOfCount=checkPartOf(prompt, location[inventoryCount])
        #            if partOfCount is not None:
        #                return lookAt.action(location[inventoryCount].partOf[partOfCount])
        #            else:
        #                return lookAt.action(location[inventoryCount])
                    
        subject=findRemainingWords(prompt)  #replace all the code above here with this?
        otherLocation=getItemLocation(subject)
        if otherLocation is not None:
            otherIndex=getItemIndex(subject, otherLocation)
            return lookAt.action(otherLocation[otherIndex])
        
            
    
        if itemExists==False:
            lookAt.error(prompt)

    def error(prompt):
        print("There is no " + findRemainingWords(prompt) + " here.")

    def action(item):
        #location=getItemLocation(item.name[0])
        #itemIndex=getItemIndex(item.name[0], location)
        if item.canSeeInside is True:
            listItemInventory(item)
        print(item.description)
        if item.isSurface is True:
            listSurfaceItems(item)#rooms.currentRoom.furniture)
        if "player" in item.name:
            print(items.player.clothesDescription)
            if items.player.hitPoints == 2:
                return print("You are injured.")
            if items.player.hitPoints == 1:
                print("You are severely injured.")

            

#LOOK IN (inside of a container)
class lookIn (roomCommand):
    name = "look in"
    description = "You look in the"

    def checkInput(verb, prompt):
        containerName=findRemainingWords(prompt)
        container=getItem(containerName)
        if container is None:
            print ("There is no", containerName, "here")
        if container is not None:
            if container.isContainer == False:
                return print ("You can't look into the", container.name[0]+".")
            if container.isOpen== True:
                if container.inventory != []:
                    return lookIn.action(container)
            if container.canSeeInside==True:
                if container.inventory != []:
                    return lookIn.action(container)
            if container.isOpen== False:
                return print("You can't see inside the", container.name[0], "while it's closed.")
            if container.inventory == []:
                print("The", container.name[0], "is empty.")
            
    def action(container):
        print("Inside the", container.name[0], "you see a:")
        for item in container.inventory:
            print(item.name[0])
    def error():
        pass

#HIT (with hands)
class hit(roomCommand):
    name="hit"
    description="You hit the "
    useWith=[items.goldenKnife]
    
    def checkInput(verb, prompt):
        itemValid=False
        locations=[rooms.currentRoom.items, inventory, rooms.currentRoom.intrinsicItems, rooms.currentRoom.door,
        rooms.currentRoom.monsters, rooms.currentRoom.furniture]
        #if rooms.currentRoom.furniture != []:
        #    for furniture in rooms.currentRoom.furniture:
        #        if furniture.isSurface == True:
        #            locations.append(furniture.surface)
        for location in locations:
            itemCount=getItemIndex(prompt, location) #check room
            if itemCount is not None:
                itemExists=True
 
                if location[itemCount].isSurface==True:
                    if location[itemCount].surface != []:
                        itemName=findRemainingWords(prompt)
                        #surfaceCount=0
                        for item in location[itemCount].surface:
                            for name in item.name:
                                if itemName == name:
                                    containerItemCount=getSurfaceIndex(name, location)
                                    location=getSurfaceLocation(name)
                                    return hit.action(location[containerItemCount].surface[itemCount], itemCount, location)
                            #surfaceCount += 1
                if location[itemCount].partOf == []:#checks if item has parts within it
                    return hit.action(location[itemCount], itemCount, location)
                partOfCount=checkPartOf(prompt, location[itemCount])
                if partOfCount is not None:
                    return hit.action(location[itemCount].partOf[partOfCount], itemCount, location)
                else:
                    return hit.action(location[itemCount], itemCount, location)             

        if itemValid==False: #error message if item not present
                hit.error(prompt)


    def error(prompt):
                print("There is no " + findVerbSubject(prompt) + " here.")


    def action(item, itemCount, location):
        
        if item.hitPoints is None:
            noEffect=["Your furious blows have no effect.", "To no effect!", "You slap and flail ineffectually.",
            "You can attack the " + item.name[0] +" all day if it makes you feel better.",
            "You vent your impotent rage at the universe on the " + item.name[0]+"."]
            return print(random.choice(noEffect))

        if 'yourself' in item.name:
            items.player.hitPoints -=1
            if items.player.equippedWeapon is not None:
                items.player.hitPoints -= items.player.equippedWeapon.damage
            #location[itemCount].hitPoints -= 1
            if items.player.hitPoints > 0:
               return print ("You have injured yourself")
            if items.player.hitPoints < 1:
                print ("You have killed yourself. THE END")
                items.player.isAlive=False
                return

        if location==rooms.currentRoom.monsters:
            if item.name[0]=="magios":
                return rooms.provokedMagios(item)
            if random.randint(0,item.dodge) == item.dodge:  #each monster has an int that determines if it gets hit
                if item.hurtByFists==False:
                    if items.player.equippedWeapon is None:
                        return print ("You can't hurt a beast like a", item.name[0], "with your bare hands!")
                if item.name[0]=="blowdart ninjai":
                    return print (items.blowDartNinjai.missDescription)
                item.hitPoints -= 1 #1 is default value.
                if items.player.equippedWeapon is not None:
                    item.hitPoints -= items.player.equippedWeapon.damage
                if item.hitPoints < 1:
                    if item.deathDescription is not None:
                        print(item.deathDescription)
                    else:
                        print("You have killed the " + item.name[0]+".")
                    if item.inventory != []:
                        for loot in item.inventory:  #drop loot when monster dies
                            rooms.currentRoom.items.append(loot)
                    del location[itemCount]
                    return
                if item.hitDescription is not None:
                    print(item.hitDescription)
                else:
                    print("You wound the " + item.name[0] +".")
            else:
                if item.missDescription is not None:
                    print (item.missDescription)
                else:
                    print("You miss the " + item.name[0] + ".")
                    print("")


            return

        else:
            item.hitPoints -=1
            if items.player.equippedWeapon is not None:
                item.hitPoints -= items.player.equippedWeapon.damage
        
        if item.hitPoints < 1:
            print("You have destroyed the " + item.name[0]+ ".")
            if item.isContainer==True:
                if item.inventory != []:
                    for thing in item.inventory:
                        location.append(thing)
            del location[itemCount]
        else:
            print("You have damaged the", item.name[0] +".")
            

    def withCheckInput(prompt, subjectItem, withItem):
        subject=subjectItem.name[0]
        withItemName=withItem.name[0]
        if subjectItem.hitPoints is not None:  #Is target destructible?
            hit.withAction(prompt, subjectItem, withItem)
            return None
        if subjectItem.hitPoints is None:
            hit.withError(subjectItem, withItem)
            #print("You can't do that to the " + subject + " with the " + withItemName)
            return None
        else:
            hit.withActionError(subjectItem, withItem)
            return None

    def withAction(prompt, subjectItem, withItem):
        if withItem.damage is not None:
            items.player.equippedWeapon=withItem #sloppy solution to this mess, creates as many problems as it solves
            #subjectItem.hitPoints-=item.damage
            hit.checkInput(withItem, prompt)
        else:
            hit.withError(subjectItem, withItem)#.name[0])

    def withError(subjectItem, withItem):
        print("You could attack the " + subjectItem.name[0] + " with the " + withItem.name[0] + " all day and you wouldn't"
        +" do much damage to it.")

#STAB
class stab(roomCommand):
    name= "stab"
    useWith=[items.goldenKnife]

    def checkInput(verb, prompt):
        if inventory !=[]:
            for item in inventory:
                if item.damage is not None:
                    if getItem(prompt) is not None:
                        weapon=item
                        return stab.action(prompt, weapon)
                        break
                    else:
                        return print("You can't attack what doesn't exist.")
                                     
        else:
            return print("You have no weapons.")

    def action(prompt, weapon):
        subjectItem=getPromptItem(prompt)
        hit.withCheckInput(prompt, subjectItem, weapon)

    

#EMPTY(DUMP OUT)
class empty(roomCommand):
    name="empty"
    description="You empty the "

    def checkInput(verb, prompt):
        containerName=findRemainingWords(prompt)
        container=getItem(containerName)
        basicName=container.name[0]
        if container.isContainer==True:
            if container.isOpen==True:
                if container.inventory != []: 
                    empty.action(container, basicName)  #perform action                       
                else:
                    return print("The", basicName, "is empty.")
            else:
                return print ("The", basicName, "isn't open.")
        else:
            return print("The", basicName, "can't have anything in it.")

    def action(container, basicName):
        
        containerLocation=getItemLocation(basicName)
        containerIndex=getItemIndex(basicName, containerLocation)
        print("You empty the", basicName +".")
        while container.inventory != []:
            nextItem=container.inventory[0] #adds item to room
            rooms.currentRoom.items.append(nextItem)
            container.containerSize=container.containerSize+nextItem.size #space in container freed up
            del container.inventory[0] #deletes item from container

#TOUCH
class touch(roomCommand):

    name="touch"

    def checkInput(verb, prompt):
        itemName=findRemainingWords(prompt)
        item=getPromptItem(itemName)
        if item is not None:
            touch.action(item)
        else:
            print("There is no", itemName, "here.")
        

    def action(item):
        if item.texture==None:
            print("You touch the", item.name[0] + ".")
        else:
            print(item.texture)
        if item.isHeal==True:
            healResult=item.checkCharge()
            if healResult==True:
                item.healPlayer()
            if healResult==False:
                return print("The", item.name[0], "is still recharging.")
            if healResult==None:
                return None
            print("You are now fully healed.")
        

#SMELL
class smell(roomCommand):
    name="smell"
    description="You sniff at the air in an attempt to assess the terroir of the locale."
    def checkInput(verb, prompt):
        smell.action(getPromptItem(prompt))
    def action(item):
        if item is not None:
            if item.smell is None:
                print("You smell the", item.name[0])
            else:
                print(item.smell)
        else:
            print("You cannot smell that which is not here.")

#TASTE
class taste(roomCommand):
    name="taste"
    description="What would you like to taste?"
    def checkInput(verb, prompt):
        taste.action(getPromptItem(prompt))
    def action(item):
        if item is not None:
            if item.taste is None:
                print("You taste the", item.name[0])
            else:
                print(item.taste)
        else:
            print("You cannot taste that which is not here.")

#KISS
class kiss(roomCommand):
    name="kiss"
    description="You kiss the air all around you showing your love for the universe."
    def checkInput(verb, prompt):
        kiss.action(getPromptItem(prompt))
    def action(item):
        if item is not None:
            print("You kiss the", item.name[0]+".", "The", item.name[0], "is loved.")
        else:
            print("You cannot kiss that which is not here.")

#SIT(DOWN)
class sit(roomCommand):
    name="sit"
    description="You sit down on the floor."
    def checkInput(verb, prompt):
        if len(verb)== len(prompt):
            return print(sit.description)
        seat=getPromptItem(prompt)
        if seat is not None:
            if seat.isSurface==True:
                return print("You sit on the", seat.name[0]+".")
            else:
                return print("You can't sit on a", seat.name[0]+"!")
        else:
            return print("""You try to sit on something doesn't exist, i.e. thin air.
You fall heavily on your ass and are now sitting on the floor.""")

    def inCheckInput(prompt, container):
        for item in inSit:
            if container.name[0]==item.name[0]:
                return print("You sit in the", container.name[0])
        for item in onSit:
            if container.name[0]==item.name[0]:
                return print("You sit ON the", container.name[0])
        else:
            if container==None:
                print("In a brave attempt to sit on something imaginary you fall on your ass.")
            else:
                print("You can't sit in a", item.name[0])
    def onCheckInput(prompt, furniture):
        for item in onSit:
            if furniture.name[0]==item.name[0]:
                return print("You sit on the", furniture.name[0])
        for item in inSit:
            if furniture.name[0]==item.name[0]:
                return print("You sit in the", furniture.name[0])
        else:
            if furniture==None:
                print("In a brave attempt to sit on something imaginary you fall on your ass.")
            else:
                print("You can't sit in a", furniture.name[0])
    def action():
        pass
    def inAction():
        pass
    def onAction():
        pass

#JUMP
class jump(roomCommand):
    name="jump"
    description="""You jump up and down like a spoiled child until it starts to become tiring.
Nothing accomplished except perhaps a light bout of cardivascular exercise."""
    def checkInput(verb, prompt):
        if prompt == "jump":
            return print (jump.description)
    def onCheckInput(item, furniture):
        if furniture is not None:
            print("You jump on the", furniture.name[0] +".")

    def onAction():
        pass
    
#EAT
class eat(roomCommand):
    name="eat"
    description="You cannot subsist on the air."

    def checkInput(verb, prompt):
        food=getPromptItem(prompt)
        if food is not None:
            if food.isEdible==True:
                eat.action(food)

            else:
                return print("You can't eat that!")

        else:
            return print("You can't eat imaginary things, except in your imagination of course.")
    

    def action(food):
        location=getItemLocation(food.name[0])
        index=getItemIndex(food.name[0], location)
        print("You eat the", food.name[0]+".")
        items.player.emptyStomach=False
        del location[index]

#POOP
class poop(roomCommand):
    name="poop"
    description="RRRRnnnngggRRR! You strain for all you're worth, but you have nothing to pass right now."

    def checkInput(verb, prompt):
        if items.player.poopTimer >=10:
            poop.action()
        else:
            print(poop.description)

    def action():
        print("With a sigh of deep relief you poop on the floor. For some reason RPGs never seem to have bathrooms.")
        rooms.currentRoom.items.append(items.turd)
        items.player.emptyStomach=True
        items.player.poopTimer=0

#FUCK(HAVE SEX WITH)
class fuck(roomCommand):
    name="fuck"
    description="It's a basic function of life, the function of procreation often used for recreation."
    def checkInput(verb, prompt):
        subject=findRemainingWords(prompt)
        sexItem=getItem(subject)
        if sexItem is not None:
            print("You painstakingly inspect the,", sexItem[0], "for an inviting orifice but fail to find one.")
        else:
            print("You must have a vivid imagination.")
    def withCheckInput():
        pass
    def withAction():
        pass
#THROW X AT
class throw(roomCommand):
    name="throw"
    description="You can't throw what's not there so you try to throw the air with a clumsy flailing motion."

    def checkInput(verb, prompt):
        item=getPromptItem(prompt)
        if item is not None:
            wordCount=findWordCount(prompt)
            if ' at ' in prompt:
                target=getLastItem(prompt)
                throw.atAction(item, target)
            else:
                if item.weight is None:
                    return print("I think you know it's impossible to throw that.")
                if item.weight > 4:
                    return print("That's too heavy for you to move, let alone throw.")
                else:
                    throw.action(item)
        else:
            print(throw.description)

    def deleteThrownItem(item, itemLocation, itemIndex):
        itemName=item.name[0]
        if itemLocation == inventory:
            if items.player.equippedWeapon is not None:
                if itemName == items.player.equippedWeapon.name[0]:
                    items.player.equippedWeapon=None
        if itemLocation != rooms.currentRoom.items:
            rooms.currentRoom.items.append(item)
            del itemLocation[itemIndex]

    def action(item):

        itemName=item.name[0]
        itemLocation=getItemLocation(itemName)
        itemIndex=getItemIndex(itemName, itemLocation)
        print("You throw the", itemName, "across the room.")
        throw.deleteThrownItem(item, itemLocation, itemIndex)
        #if items.player.equippedWeapon is not None:
        #    if itemName == items.player.equippedWeapon.name[0]:
        #        items.player.equippedWeapon=None
        #if itemLocation != rooms.currentRoom.items:
        #    rooms.currentRoom.items.append(item)
        #    del itemLocation[itemIndex]

        

    def atAction(item, target):
        if item.weight == None:
            return print("You know it's impossible to throw that!")
        itemName=item.name[0]
        itemLocation=getItemLocation(itemName)
        itemIndex=getItemIndex(itemName, itemLocation)
        getsHit=True
        if target.isAlive==True:
            if random.randint(0,target.dodge) == target.dodge:
                getsHit=True
            else:
                getsHit=False
        if getsHit== False:
            print("You throw the",item.name[0], "at the" ,target.name[0], "but it misses and goes flying onto the floor." )
            return throw.deleteThrownItem(item, itemLocation, itemIndex) 
        targetLocation=getItemLocation(target.name[0])
        targetIndex=getItemIndex(target.name[0], targetLocation)        
        if item.weight < 3:
            print("The",item.name[0], "bounces harmlessly off the", target.name[0])
            return throw.deleteThrownItem(item, itemLocation, itemIndex)
        if item.weight >= 3:
            if target.hitPoints==None:
                print("Even throwing heavy things at the", target.name[0], "won't accomplish anything.")
                return throw.deleteThrownItem(item, itemLocation, itemIndex)
            targetLocation[targetIndex].hitPoints -= 1
            if target.isAlive==True:
                print("With a sickening thud your projectile injures the",target.name[0])
            else:
                print("With a crash, your projectile damages the", target.name[0])
            checkKillMonster(target, targetLocation, targetIndex)
        throw.deleteThrownItem(item, itemLocation, itemIndex)
            
                

        
            
                                                   
#DICTIONARIES
quitProgram=['quit', 'q', 'exit', 'escape', 'esc']
yes=["yes", "y", "yeah"]
no=["n", "no", "nope"]
programCommands=['quit', 'q', 'exit', 'escape', 'esc',"yes", "y", "yeah", "n", "no", "nope"]
expletives=['fuck', 'shit', 'fuck you', 'bitch', 'bastard', 'shut up', "damn", 'crap', 'asshole', 'fucking',
            'mother fucker', 'mother fucking', 'ass','dick', "suck a dick", "fucker", "dickhead",
            'shut the fuck up', 'fuck off', 'piss off']
slurs=["nigger", "spic", "cracker", "mic", "daigo", "guinea", "jigaboo", "wetback", "mojau", "polock", "jew",
"kike", "goy", "garlic eater", "whitey", "guido", "white nigger", "white trash", "redneck", "jap", "nig", "nigrah",
"colored", "colored folk", "colored people", "kraut", "frog", "sand nigger", "towelhead", "camel jockey",
"poor white", "gook", "chink", "rice nigger", "fucking jew", "honky", "honkie"]
retort=["That's very naughty of you.", "I should rather you were more polite.",
        "So you think you're an adult now?", "Potty mouth.", "How rude!",
        "My, my such colorful choice of words.", "I'm telling teacher.",
        "Such vulgarity indeed."]
inventory= []
verbs={'take':take, 'get': take, 'grab' : take, 'pick up': take, 'drop': drop, 'put down': drop,
'inventory': inventory, 'i': inventory,'look at': lookAt, 'l at':lookAt, 'examine': lookAt, 'open' : openItem,
'close': closeItem, 'shut': closeItem, 'hit': hit, 'attack' : hit, 'punch' : hit, 'kick': hit, 'bash':hit, 'smash' : hit,
'break': hit, 'beat up': hit, 'kill' : hit, 'destroy' : hit, 'put' : putIn, "look in": lookIn, "look inside":lookIn,
"l in":lookIn, "look inside of": lookIn, "look into": lookIn, "empty": empty, "dump": empty, "empty out": empty,
"dump out": empty, "unlock": unlock, "lock": lock, "slap": hit, "touch": touch, "stab":stab, "cut":stab,
"slash":stab, "slice":stab,  "say": say, "mumble": say, "whisper" : say, "scream": scream, "yell": scream,
"bellow":scream, "screech": scream, "shout": scream, "smell": smell, "sniff": smell, "taste": taste, "lick": taste,
"kiss":kiss, "smooch":kiss, "wear":wear, "put on":wear, "sit in":sit, "sit": sit, "sit down": sit, "eat": eat, "poop": poop,
"go poop": poop, "throw":throw, "toss": throw, "fling": throw, "sit on": sit, "read":lookAt, "ask": ask, "jump": jump}

lookAndInventory={'i': lookAtInventory, 'inventory': lookAtInventory ,'l': look,
'look': look,'look at inventory': lookAtInventory,'l at inventory': lookAtInventory, 'l at room': look,
'look at room': look, 'look around': look, 'examine inventory': lookAtInventory, 'examine room': look}
weapons=[items.goldenKnife]
modifiers=[" with ", " and ", " on ", " in "," at ", " from ", " inside ", " inside of ", " on top of ", " into ", " out of ", 
" onto ", " on to "]
overlapVerbs=["put", "empty", "dump", "look"]
modifierWords=["of", "on", "to","top", "inside", "out"]
inSit=[items.loungeChair]
onSit=[items.servingBar, items.woodenTable, items.barStool, items.floor]
hiWords=["hi", "hello", '"hello"','"hi"']

#locations=[rooms.currentRoom.items, inventory, rooms.currentRoom.intrinsicItems, rooms.currentRoom.door,
#rooms.currentRoom.monsters ,rooms.currentRoom.furniture]

#modifiers=(' at ', ' on ', ' in ', ' and ')
#'look': look, 'l': look,
#SYNONYM DICTIONARIES
all = ['all', 'everything']


#INPUT/OUTPUT I/O

def enterRoom(presentCurrentRoom):
    rooms.roomTimer=0
    if rooms.currentRoom.enterScript is not None:
        rooms.currentRoom.enterScript()
    print(presentCurrentRoom.description)
    if presentCurrentRoom.items != []:
        describeItemsInRoom=0
    if presentCurrentRoom.monsters != []:
        for monster in presentCurrentRoom.monsters:
            print("You see a", monster.name[0] + ".")
    for item in presentCurrentRoom.items:
        print("There is a " + presentCurrentRoom.items[describeItemsInRoom].name[0] + " here.")
        if item.isSurface==True:
            if item.surface is not None:
                if item.surface != []:
                    listSurfaceItems(item)
        describeItemsInRoom=describeItemsInRoom+1
    listAllFurnitureSurfaceItems(rooms.currentRoom.furniture)

def lookAtRoom(presentCurrentRoom):
    print(presentCurrentRoom.description)
    if presentCurrentRoom.items != []:
        describeItemsInRoom=0
    if presentCurrentRoom.monsters != []:
        for monster in presentCurrentRoom.monsters:
            print("You see a", monster.name[0] + ".")
    for item in presentCurrentRoom.items:
        print("There is a " + presentCurrentRoom.items[describeItemsInRoom].name[0] + " here.")
        if item.isSurface==True:
            if item.surface is not None:
                if item.surface != []:
                    listSurfaceItems(item)
        describeItemsInRoom=describeItemsInRoom+1
    listAllFurnitureSurfaceItems(rooms.currentRoom.furniture)

def listAllFurnitureSurfaceItems(furniture): #returns all items on any furniture surface
    for thing in furniture:
        if thing.isSurface==True:
            if thing.surface != []:
              print("On the", thing.name[0], "you see a:")
              for item in thing.surface:
                  print(item.name[0])
                  if item.isSurface==True:
                      if item.surface is not None:
                          if item.surface != []:
                              listSurfaceItems(item)

def listSurfaceItems(item):  #returns all items on one item's surface
    if item.isSurface==True:
        if item.surface != []:
            if item.surface != None:
                for thing in item.surface:
                    print("On the", item.name[0], "you see a:")
                    print(thing.name[0])

def listItemInventory(item):
    if item.canSeeInside==True:
        if item.inventory != []:
            for thing in item.inventory:
                print("Inside the", item.name[0], "you see a:")
                print(thing.name[0])

                    
        


#def checkVerb(prompt):
#    complexVerb = findAllVerbs(prompt)
#    for verb in verbs:
#        if verb == complexVerb:
#            return True
#        else:
#            return False

#def findVerb(prompt):
#    verb='' #reset variables each iteration #How cute have come a long way since then.
#    verbLetterCount=0 #to start at prompt[0]
#    verbLetter=prompt[verbLetterCount]
#    while verbLetter != ' ': #reads first word of player input, stops when it encounters a space HMM  and if len(prompt)<
#        verb=verb+verbLetter #adds letter to verb word
#        verbLetterCount=verbLetterCount+1 
#        verbLetter=prompt[verbLetterCount]#moves on to next letter
#    return verb

def findAllVerbs(prompt):
    verbPhrase='' #store info here
    wordCount=findWordCount(prompt)
    while wordCount > 0:
        verbLetterCount=0 #Erase these variables each time around, store in verb variable
        verbLetter=''
        verbLetter=prompt[verbLetterCount]
        verb=''
        if wordCount > 1:
            while verbLetter != ' ': #reads first word of player input, stops when it encounters a space HMM  and if len(prompt)<
                verb=verb+verbLetter #adds letter to verb word
                verbLetterCount+=1 
                verbLetter=prompt[verbLetterCount]#moves on to next letter
        else:
            for letter in prompt:
                verb=verb+letter
        verbPhrase = verbPhrase + verb #adds word to string
        for name in verbs:   #does phrase so far match a valid verb?
            if name==verbPhrase:
                if verbPhrase in overlapVerbs: #put vs. put on, empty vs. empty out
                    testSentence=cutFirstWord(prompt)
                    testWord=findFirstWord(testSentence)
                    testPhrase=verbPhrase+" "+testWord
                    for name in verbs:
                        if name==testPhrase:
                            return testPhrase
                    else:
                        return verbPhrase
                else:
                    return verbPhrase #if yes, return verb
        if wordCount > 1: 
            verbPhrase = verbPhrase + " "  #add space on end
            
            prompt=prompt[len(findFirstWord(prompt))+1:]
        wordCount = wordCount -1
    return None

#def getNextWord (prompt):
#    verbLetter=""
#    verbLetterCount=0
#    verb=""
#    wordCount=findWordCount(prompt)
#    while verbLetter != ' ': #reads first word of player input, stops when it encounters a space HMM  and if len(prompt)<
#        verb=verb+verbLetter #adds letter to verb word 
#        verbLetter=prompt[verbLetterCount]#moves on to next letter
#        verbLetterCount+=1
#    print("this is what getNextWord returns:", verb)
#    return verb

def cutFirstWord (prompt):
    prompt=prompt[len(findFirstWord(prompt))+1:]
    return prompt

def cutLastWord (prompt):
    prompt=prompt[:-len(findLastWord(prompt))-1]
    return prompt

def beforeModifier(prompt):  #returns everything before 'and', 'on' etc.
    modifierCount=0
    for modifier in modifiers:
        tempPrompt=prompt
        extraWords=""
        result=None
        while findWordCount(tempPrompt) > 1:
            lastWord=findLastWord(tempPrompt)
            if lastWord == modifier.strip():
                if lastWord in modifierWords:
                    result=findBeforeComplexModifier(tempPrompt+extraWords, modifierCount)
                    #if result is not None:
                    #    return result
                if result is None:                 
                    tempPrompt=cutLastWord(tempPrompt)
                    return tempPrompt
            if lastWord in modifierWords:
                extraWords =" " + lastWord + extraWords   
            tempPrompt=cutLastWord(tempPrompt)
        modifierCount=modifierCount + 1
    else:
        return None

def afterModifier(prompt):  #returns words that come after on, in etc. to get input for multi-word item names
    modifierCount=0 
    for modifier in modifiers:
        tempPrompt=prompt
        while findWordCount(tempPrompt) > 1:
            firstWord=findFirstWord(tempPrompt)
            if firstWord == modifier.strip(): #reads through words in string until it finds modifier 
                if firstWord in modifierWords: #if 'look,' checks if it's 'look in'
                    result=findAfterComplexModifier(tempPrompt, modifierCount)
                    if result is not None:
                        return result
                tempPrompt=cutFirstWord(tempPrompt)
                return tempPrompt
            tempPrompt=cutFirstWord(tempPrompt)
        modifierCount=modifierCount+1  
    else:
        return None
    
def findAfterComplexModifier(prompt, modifierCount): #distinguishes between modifiers with overlapping words, returns correct modifier
    restModifiers=modifiers[modifierCount+1:]
    for modifier in restModifiers:
        tempPrompt=prompt
        complexModifier=""
        while findWordCount(tempPrompt) > 1:
            firstWord=findFirstWord(tempPrompt)
            complexModifier=complexModifier+firstWord
            if complexModifier == modifier:
                return tempPrompt[len(firstWord)+1:]
            complexModifier=complexModifier + " "
            tempPrompt=cutFirstWord(tempPrompt)
    else:
        return None

def findBeforeComplexModifier(prompt, modifierCount):
    restModifiers=modifiers[modifierCount+1:] #starts one item in the list after the one that triggered this method, prevent overlap
    for modifier in restModifiers:
        tempPrompt=prompt  #another copy needed if prompt changes during iteration?, loop stops short
        complexModifier=""
        while findWordCount(tempPrompt) > 1:
            lastWord=findLastWord(tempPrompt)
            complexModifier=lastWord+complexModifier
            if complexModifier == modifier:
                return tempPrompt[:-len(lastWord)-1] #cuts off the multi-word modifier, returns everything before it
            complexModifier=" " + complexModifier
            tempPrompt=cutLastWord(tempPrompt)
    else:
        return None
            
def beforeAnd(prompt):
    if findLastWord(prompt)== 'and':
        prompt=cutLastWord(prompt)
        return prompt
    else:
        prompt=cutLastWord(prompt)
        return beforeAnd(prompt)

def afterAnd(prompt):
    if findFirstWord(prompt) == 'and':
        prompt=cutFirstWord(prompt)
        return prompt
    else:
        prompt=cutFirstWord(prompt)
        return afterAnd(prompt)

def beforeWith(prompt):
    if findLastWord(prompt)== 'with':
        prompt=cutLastWord(prompt)
        return prompt
    else:
        prompt=cutLastWord(prompt)
        return beforeWith(prompt)
    
def afterWith(prompt):
    if findFirstWord(prompt) == 'with':
        prompt=cutFirstWord(prompt)
        return prompt
    else:
        prompt=cutFirstWord(prompt)
        return afterWith(prompt)  
    

def findRemainingWords(prompt):  #returns what comes after verb word(s) and before  "and" or "on": "put rock on table" returns "rock"
    verbPhrase='' #store info here
    prompt=prompt.replace(" the ", " ")
    wordCount=findWordCount(prompt)
    originalPrompt=prompt
    #while wordCount > 0:
    #verbLetterCount=0 #Erase these variables each time around, store in verb variable
    #verbLetter=''
    #verbLetter=prompt[verbLetterCount]
    #verb=''
    if wordCount > 1:
        testVerb=checkVerbOverlap(prompt)
        if testVerb is not None:
            verbWordCount=findWordCount(testVerb)
            prompt=prompt[len(testVerb)+1:]
            wordCount-=verbWordCount #keep track of count to avoid going out of index and crashing program
    #if wordCount > 1: 
    #    while verbLetter != ' ': #reads first word of player input, stops when it encounters a space HMM  and if len(prompt)<
    #        verb=verb+verbLetter #adds letter to verb word
    #        verbLetterCount=verbLetterCount+1 
    #        verbLetter=prompt[verbLetterCount]#moves on to next letter
    #    verbPhrase = verbPhrase + verb  #adds word to string             
    #    prompt=cutFirstWord(prompt)
    #    for name in verbs:   #does phrase so far match a valid verb?
    #        if name==verbPhrase:
    #            if findWordCount(prompt) > 1: #these prevent going out of index
    #    firstWord=findFirstWord(prompt)
    #    if firstWord=="the":  #Takes out "the"
    #        prompt=cutFirstWord(prompt)
    #        wordCount-=1
                #if ' and ' in prompt:
                #    prompt=beforeAnd(prompt)
                #if ' with ' in prompt:
                #    prompt=beforeWith(prompt)
        for modifier in modifiers:
            if modifier in prompt:
                prompt=beforeModifier(prompt)
                break
                return prompt #if yes, return non-verb words
            verbPhrase = verbPhrase + " "  #add space on end
        return prompt
    else:
        return prompt
        wordCount = wordCount -1
    return originalPrompt

def checkVerbOverlap(prompt):  #If "put on shirt"(returns "put on") or "put shirt on table"(returns "put") or original verb, or None if it's nonsense.
    firstWord=findFirstWord(prompt) 
    if firstWord in overlapVerbs: #put vs. put on, empty vs. empty out
        testSentence=cutFirstWord(prompt)
        testWord=findFirstWord(testSentence)
        testPhrase=firstWord+" "+testWord
        for name in verbs:
            if name==testPhrase:
                return testPhrase
        else:
            return firstWord
    if firstWord in verbs:
        return firstWord
    else:
        return None

def findVerbLength():
    verb='' #reset variables each iteration
    verbLetterCount=0 #to start at prompt[0]
    verbLetter=prompt[verbLetterCount]
    subjectWordCount=1

    while verbLetter != ' ': #reads verb from player input, stops when it encounters a space
        verb=verb+verbLetter #adds letter to verb word
        verbLetterCount=verbLetterCount+1 
        verbLetter=prompt[verbLetterCount]#moves on to next letter
    return verbLetterCount

def findVerbSubject(prompt):
    
    if " " not in prompt :  #if only one word, return that word, lead to error message for verb without subject?
        return prompt 
    if " " + findFirstWord(prompt) + " " not in modifiers: #" at " format in modifier list so it can be tacked on without adding more spaces.
        if findFirstWord(prompt) not in verbs:
            return prompt     
    prompt=prompt[len(findFirstWord(prompt))+1:]#Cut off word from the string before moving on to the next.
    return findVerbSubject(prompt)

def findFirstWord (input): #For use within methods, findVerb() does same thing with player input
    wordCount=findWordCount(input)
    if wordCount == 1:
        return input
    firstWord='' #reset variables each iteration
    firstWordLetterCount=0 #to start at prompt[0]
    firstWordLetter=input[firstWordLetterCount]
    while firstWordLetter != ' ': #reads first word of player input, stops when it encounters a space  and if len(prompt)<
        firstWord=firstWord+firstWordLetter #adds letter to verb word
        firstWordLetterCount=firstWordLetterCount+1
        firstWordLetter=input[firstWordLetterCount]
    return firstWord

def findFirstWordLength(prompt):
    firstWord=findFirstWord(prompt)
    return len(firstWord)

def findLastWordLength(prompt):
    lastWord=findLastWord(prompt)
    return len(lastWord)

def findLastWord(prompt):
    lastWord='' #reset variables each iteration
    lastWordLetterCount=-1 #to start at prompt[-1]
    lastWordLetter=prompt[lastWordLetterCount]
    while lastWordLetter != ' ': #reads first word of player input, stops when it encounters a space  and if len(prompt)<
        lastWord=lastWord+lastWordLetter #adds letter to verb word
        lastWordLetterCount=lastWordLetterCount-1
        lastWordLetter=prompt[lastWordLetterCount]
    return lastWord[::-1]

def findWordCount(prompt):
    wordCount=1
    for letter in prompt:
        if letter==' ':
            wordCount=wordCount+1
    return wordCount

def doWith (prompt):
    withItemName = afterWith(prompt)
    verb=findAllVerbs(prompt)
    subject=findRemainingWords(prompt)
    if verbs[verb].withAction == None:
        print ("You can't use anything to do that.")
        return None
    subjectItem=getItem(subject)
    withItem=getItem(withItemName)
    #validItem=getDoWithItem(verb, withItemName)
    if withItem is None:
        print("There is no " + withItemName + " here.")
        return None
    if subjectItem is None:
        print("There is no " + subject + " here.")
        return None
    if getItemLocation(withItemName) is not inventory:
        print ("You don't have the " + withItemName)
        return None
    else:
        verbs[verb].withCheckInput(prompt, subjectItem, withItem)
        
def getDoWithItem (verb, itemName):
    for withItem in verbs[verb].useWith:
        for name in withItem.name:
            if name==itemName:
                return withItem
        else:
            return None
def doIn(prompt):
    verb=findAllVerbs(prompt)
    item=getItem(findRemainingWords(prompt))
    container=getLastItem(prompt)
    if container is not None:
        if item is not None:
            if container.isContainer is False:
                print("There is nothing inside that.")
            if container.isContainer is True:
                if container.containerSize is None:
                    return print("You can't put anything in that.")
                if item.size is None:
                    return print("You can't put that in anything, silly billy.")
                if container.isOpen is True:
                    verbs[verb].inCheckInput(prompt, item, container)
                else:
                    print ("You can't do that if the " + container.name[0] + " is closed.")
        else:
            if verb == "sit":
                return verbs[verb].inCheckInput(prompt, container)
            return print("There is no", findRemainingWords(prompt), "here")
    else:
        print("There is no", findLastWord(prompt), "here.") 

def doFrom(verb, prompt):
    container=getLastItem(prompt)
    containerName=container.name[0]
    itemName=findRemainingWords(prompt)
    if container is not None:
        if container.isContainer is False:
            return print("There can't be anything in the", containerName+".")
        if container.isContainer is True:
            if container.inventory==[]:
                return print ("The", containerName, "is empty.")
            if container.inventory != []: #if something is in the inventory...
                itemIndex=0
                for item in container.inventory:
                    for name in item.name:
                        if name==itemName:
                            return verbs[verb].fromCheckInput(item, container, itemIndex)
                    itemIndex=itemIndex+1
                else:
                    return print ("There is no", itemName, "here.")
    elif container is None:
        return print ("There is no", afterModifier(prompt), "here.")

def doOn(verb, prompt):
    furniture=getLastItem(prompt)
    item=getPromptItem(prompt)
    simpleOn=["jump", "sit"]
    twoSubjects=True
    if item is None:
        twoSubjects=False
    elif item.size is None:
        return print("You can't put that on anything.")
    itemName=findRemainingWords(prompt)
    if furniture is not None:
        furnitureName=furniture.name[0]
        if furniture.isSurface is False:
            return print("There can't be anything on the", furnitureName+".")
        if furniture.isSurface is True:
            if twoSubjects == False:
                if verb in simpleOn:
                    return verbs[verb].onCheckInput(prompt, furniture)
                else:
                    return print("There is no", afterModifier(prompt), "here")
            else:
                return verbs[verb].onCheckInput(item, furniture)
    elif furniture is None:
        return print ("There is no", afterModifier(prompt), "here.")
    

#COMMAND EXECUTION

def actionOrError(prompt, itemCount):
    verb=findAllVerbs(prompt)
    if itemCount is not None:
        verbs[verb].action(itemCount)

    if itemCount is None: #error message if item not in room
        verbs[verb].error(findRemainingWords(prompt))
    
#ITEM FUNCTIONS

def checkIfInReach(prompt): #consider exceptions to rule like throw at and look at...
    pass

def checkKillMonster(monster, location, index):
    if monster.hitPoints < 1:
        if monster.deathDescription is not None:
            print(monster.deathDescription)
        else:
            print("You have killed the " + monster.name[0]+".")
        if monster.inventory != []:
            for loot in monster.inventory:  #drop loot when monster dies
                rooms.currentRoom.items.append(loot)
        del location[index]
    return

def findItemCount():
    itemCount = 0
    for item in rooms.currentRoom.items:
        itemCount = itemCount + 1
    return itemCount

def hasPartof(item): #Is it part of an item?
    if item.partOf != []:
        return True
    else:
        return False

def checkRoom(prompt):  #checks if something is in room.items returns True or False
    itemValid=False
    itemCount=0
    subject=findRemainingWords(prompt)
    for item in rooms.currentRoom.items: #checks each item in room to see if the verb subject matches                          
        for name in item.name: 
            if subject == name:  #checks if matches object in room
                itemValid=True
                return itemCount
        itemCount=itemCount+1
    if itemValid==False:
        return None

def checkEverything(prompt): #Does not check partsOf.  I still want this for commands like take.  
    itemValid=False          #Not so simple, returns index of an item name in names, not an item index in a location
    itemCount=0
    locations=[rooms.currentRoom.items, inventory, rooms.currentRoom.intrinsicItems, rooms.currentRoom.door,
    rooms.currentRoom.monsters ,rooms.currentRoom.furniture]
    subject=findRemainingWords(prompt)
    for location in locations:
        for item in location: #checks each item in room to see if the verb subject matches                          
            for name in item.name: 
                if subject == name:  #checks if matches object in room
                    itemValid=True
                    return itemCount
            itemCount=itemCount+1
    if itemValid==False:
        return None

def checkPartOf(prompt, item): #returns index number of part
    partOfItemCount=0
    subject=findRemainingWords(prompt)
    itemValid=False
    if item.partOf != []:
        for part in item.partOf:
            for names in part.name: #put this in each check method?
                if subject == names:
                    itemValid=True
                    return partOfItemCount
            partOfItemCount=partOfItemCount+1
    if itemValid==False:
        return None
    

def checkInventory(prompt):
    itemValid=False
    inventoryItemCount=0
    subject=findRemainingWords(prompt)
    for item in inventory:      
        for name in item.name:
            if subject == name:
                itemValid=True
                return inventoryItemCount
        inventoryItemCount=inventoryItemCount+1   
    if itemValid==False:
        return None
    
def checkIntrinsicItems(prompt):
    itemValid=False
    intrinsicItemCount=0
    for item in rooms.currentRoom.intrinsicItems: #checks walls, floor, player etc.            
        for name in item.name:
            if findVerbSubject(prompt) == name:
                itemValid=True
                return intrinsicItemCount
        intrinsicItemCount=intrinsicItemCount+1    
    if itemValid==False: 
        return None

def getSurfaceItemIndex(prompt, item):  #gets index of an item on a surface 
    if item.isSurface==True:
        if item.surface != []:
            itemName=findRemainingWords(prompt)
            surfaceCount=0
            for thing in item.surface:
                for name in thing.name:
                    if itemName == name:
                        return surfaceCount
                surfaceCount+=1
    return None

def getSurfaceIndex(itemName, location): #gets index of the surface that an item is on.
    #subject=findRemainingWords(prompt)
    itemCount=0
    for item in location:
        if item.surface is not None:
            for thing in item.surface:
                for names in thing.name:
                    if itemName==names:
                        return itemCount
        if item.partOf != []:
            for part in item.partOf:
                for names in part.name: 
                    if itemName == names:
                        return itemCount

        itemCount +=1
    else:
        return None

def getTransparentContainerIndex(itemName, location):
    itemCount=0
    if location is not None:
        for item in location:
            if item.canSeeInside is True:
                for thing in item.inventory:
                    for names in thing.name:
                        if itemName==names:
                            return itemCount
            if item.partOf != []:
                for part in item.partOf:
                    for names in part.name: 
                        if itemName == names:
                            return itemCount

            itemCount +=1
    else:
        return None

def getTransparentContainerLocation(itemName): #gets location of a see-through container that contains an item
    locations=[rooms.currentRoom.items, inventory, rooms.currentRoom.intrinsicItems, rooms.currentRoom.door,
    rooms.currentRoom.monsters, rooms.currentRoom.furniture]
    for location in locations:
        for item in location:
            if item.canSeeInside==True:
                if item.inventory != []:
                    for thing in item.inventory:
                        for names in thing.name:
                            if itemName == names:
                                return location
            if item.partOf != []:
                for part in item.partOf:
                    for names in part.name: 
                        if itemName == names:
                            return location
    else:
        return None
    
    
    
def getItemIndex(prompt, location):
    itemCount=0
    itemValid=False
    subject=findRemainingWords(prompt)
    for item in location: #checks each item in room to see if the verb subject matches                          
        for name in item.name: 
            if subject == name:  #checks if matches object in room
                itemValid=True
                if item.partOf==[]:
                    if item.isSurface==False:
                        return itemCount
                    if item.surface == []:
                        return itemCount
        if item.partOf != []:
            partCount=0
            for part in item.partOf:
                for names in part.name: 
                    if subject == names:
                        itemValid=True
                        return partCount
                partCount+=1
        if item.surface is not None:
            thingCount=0
            for thing in item.surface:
                for names in thing.name:
                    if subject==names:
                        return thingCount
                thingCount+=1
        if itemValid==True:
            return itemCount
        itemCount=itemCount+1
    if itemValid==False:
        return None
    
#get item (for searching)
def getItem(prompt):
    itemCount=0
    subject=findRemainingWords(prompt)
    locations=[rooms.currentRoom.items, inventory, items.player.partOf, rooms.currentRoom.intrinsicItems,
    rooms.currentRoom.door, rooms.currentRoom.monsters,rooms.currentRoom.furniture]
    for location in locations:
        for item in location: #checks each item in room to see if the verb subject matches                          
            for name in item.name:
                if subject == name:  #checks if matches object in room
                        return location[itemCount]
            if item.partOf != []:
                for part in item.partOf:
                    for names in part.name: 
                        if subject == names:
                            return location[itemCount]
            if item.inventory != []:
                inventoryCount=0
                for item in item.inventory:
                    for names in item.name:
                        if subject == names:
                            return location[itemCount].inventory[inventoryCount]
                    inventoryCount+=1
            if item.surface is not None:
                thingCount=0
                for thing in item.surface:
                    for names in thing.name:
                        if subject==names:
                            return location[itemCount].surface[thingCount]
                    thingCount+=1
            itemCount+=1
        itemCount=0
    else:
        return None

def getPromptItem(prompt):
    itemName=findRemainingWords(prompt)
    item=getItem(itemName)
    return item

def getLastItem(prompt):  #gets an item at end of string
    lastWord=findLastWord(prompt)
    lastItem=getItem(lastWord)
    if lastItem is not None:
        return lastItem
    while findWordCount(prompt) > 2:
        #print("wordCount:", findWordCount(prompt))
        #print("last word", lastWord)
        prompt=cutLastWord(prompt)
        #print("prompt is:", prompt)
        lastWord=findLastWord(prompt)+" "+lastWord
        lastItem=getItem(lastWord)
        if lastItem is not None:
            return lastItem
    else:
        return None

def getSurfaceLocation(itemName):
    locations=[rooms.currentRoom.items, inventory, rooms.currentRoom.intrinsicItems, rooms.currentRoom.door,
    rooms.currentRoom.monsters, rooms.currentRoom.furniture]
    for location in locations:
        for item in location:
            if item.isSurface==True:
                if item.surface != []:
                    for thing in item.surface:
                        for names in thing.name:
                            if itemName == names:
                                return location
            if item.partOf != []:
                for part in item.partOf:
                    for names in part.name: 
                        if itemName == names:
                            return location
    else:
        return None
    
    
def getItemLocation(itemName): #expects a string
    #itemName=findRemainingWords(itemName)
    locations=[rooms.currentRoom.items, inventory, rooms.currentRoom.intrinsicItems, rooms.currentRoom.door,
    rooms.currentRoom.monsters, rooms.currentRoom.furniture]

    for location in locations:
        for item in location: #checks each item in room to see if the verb subject matches
            itemValid=False
            for name in item.name:
                if itemName == name:  #checks if matches object in room
                    itemValid=True
                    if item.partOf == []:
                        if item.isSurface==False:
                                return location
                        if item.surface==[]:
                            return location
            if item.partOf != []:
                for part in item.partOf:
                    for names in part.name: 
                        if itemName == names:
                            itemValid=True
                            return item.partOf
            if item.isSurface==True:
                if item.surface != []:
                    for thing in item.surface:
                        for names in thing.name:
                            if itemName == names:
                                itemValid=True
                                return item.surface
            if item.canSeeInside==True:
                for thing in item.inventory:
                    for names in thing.name:
                        if itemName == names:
                            itemValid=True
                            return item.inventory
            if itemValid==True:
                return location
    else:
        return None

#def getExactLocation(itemName):
#    locations=[rooms.currentRoom.items, inventory, rooms.currentRoom.intrinsicItems, rooms.currentRoom.door,
#    rooms.currentRoom.monsters, rooms.currentRoom.furniture]
#    for location in locations:
#        for item in location: #checks each item in room to see if the verb subject matches
#            itemCount=0
#            for name in item.name:
#                if itemName == name:  #checks if matches object in room
#                    itemValid=True
#                    return location[itemCount]
#                itemCount+=1
#            if item.partOf != []:
#                for part in item.partOf:
#                    for names in part.name: 
#                        if itemName == names:
#                            itemValid=True
#                            return location.item.partOf
#    else:
#        return None  

def isItemPresent(prompt):
    itemExists=False
    inInventory=False
    inIntrinsicItems=False
    subject=findRemainingWords(prompt)

    for item in inventory:      #checks if item is inventory when you try to look at it
        for name in item.name:
            if subject == name:
                inInventory=True
                itemExists=True
                return(item)
        for part in item.partOf:  #If not an item in room, is it part of one of those items?
                    for names in part.name:
                        if subject == names:
                            itemExists=True
                            return(part)
                            
       
    if inInventory==False:
        if rooms.currentRoom.items != []:  #checks if item is in the room when you try to look at it
            for item in rooms.currentRoom.items:
                for name in item.name:
                    if subject == name:
                        itemExists=True
                        return(item)
                for part in item.partOf:  #If not an item in room, is it part of one of those items?
                    for names in part.name:
                        if subject == names:
                            itemExists=True
                            return(part)
                            
       
    for item in rooms.currentRoom.intrinsicItems:
        for names in item.name:
            if subject == names:
                itemExists=True
                return(item)

    else:
        return None

#MODIFIER COMMANDS

def executeCommand(prompt):
    verb=findAllVerbs(prompt)
    commands.verbs[verb].checkInput(verb, prompt)

def andSentence(prompt):
    secondPhrase=commands.afterAnd(prompt)
    secondVerb=commands.findAllVerbs(secondPhrase)
    if secondVerb is not None:
        commands.verbs[secondVerb].checkInput(secondVerb, secondPhrase)

def withSentence(prompt):
    if commands.verbs[verb].withAction is not None:
        commands.doWith(prompt)

def inSentence(prompt):
    pass

def onSentence(prompt):
    pass

