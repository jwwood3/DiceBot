import discord
import random
import botAuth

bot = discord.Client()

distribution = "fun"
luckyGuy = ""
unluckyGuy = ""
fixes = {}

@bot.event
async def on_ready():
    setLucks()
    
def setLucks():
    global luckyGuy
    global unluckyGuy
    players = []
    for i in bot.guilds[0].members:
        #print(str(i) + " : " + str(i.bot) + " : " + str(i.status) + " : " + str(i.name) + ":" + str(i.discriminator))
        is_dm = False
        for role in i.roles:
            if role.guild==bot.guilds[0] and role.name == "DM":
                is_dm = True
        if not i.bot and i.status == bot.guilds[0].me.status and not is_dm:
            players.append(i.name)
    #print(players)
    if(len(players)>0):
        luckyGuy = random.choice(players)
        players.remove(luckyGuy)
    if(len(players)>0):
        unluckyGuy = random.choice(players)
    print("luck : "+luckyGuy)
    print("unluck : "+unluckyGuy)

def roll_die(user, num, die, best, add):
    global luckyGuy
    global unluckyGuy
    global distribution
    results = []
    bestResults = []
    
    for i in range(num):
        value = 1
        if distribution=="true":
            value = random.randint(1, die)
        elif distribution=="fun":
            if user.name==luckyGuy:
                value = random.choices(range(1,die+1),weights=([1]*(die-1))+[1.2], k=1)[0]
            elif user.name==unluckyGuy:
                value = random.choices(range(1,die+1),weights=([1]*(die-1))+[1.2], k=1)[0]
            else:
                value = random.randint(1, die)
        if user.name in fixes and fixes[user.name]<=die:
            value = fixes[user.name];
            fixes.pop(user.name);
        results.append(value)
    #print(best)
    bestNums = best
    if best>num or best==-1:
        bestNums = num
    for j in range(bestNums):
        results.sort()
        bestVal = results[len(results)-1]
        bestResults.append(bestVal)
        results.pop(len(results)-1)
    retString = ""+str(num)+"d"+str(die)
    if best!=-1:
        retString+="b"+str(best)
    if add>0:
        retString+="+"+str(add)
    elif add<0:
        retString+="-"+str(-1*add)
    retString+=" = {"
    for l in range(len(bestResults)):
        retString+=""+str(bestResults[l])+","
    if add==0:
        retString+="}\nSum = "
    elif add>0:
        retString+="} + "+str(add)+"\nSum = "
    elif add<0:
        retString+="} - "+str(-1*add)+"\nSum = "
    for m in range(len(bestResults)):
        retString+=""+str(bestResults[m])+" + "
    if add==0:
        retString = retString[0:-3] + " = "
    elif add>0:
        retString+="" + str(add) + " = "
    elif add<0:
        retString = retString[0:-3] + " - " + str(-1*add) + " = "
    sum = 0
    for n in range(len(bestResults)):
        sum+=bestResults[n]
    sum+=add
    retString+=str(sum)
    return retString
    
def helpText(permis):
    retString="Commands may/must be prefixed by /, //, !, or !!\n\n"+\
    "Normal Commands:\n"+\
    "help - Shows this help message\n\n"
    if permis<2:
        retString+="DM Commands:\n"+\
        "true - Sets rolls to follow true random distribution\n"+\
        "fun - Sets rolls to follow fun distribution\n"+\
        "check - Shows which players are affected by fun distribution\n"+\
        "checkrng [num] - Rolls 100000 d[num]s and displays results using current distribution\n"+\
        "fixnext [player] [num] - Guarantees [player]'s next roll to be a [num] if possible\n"+\
        "restartfun - Picks new players to be affected by the fun distribution\n\n"
    if permis==0:
        retString+="Owner Commands:\n"+\
        "exit - Turns off the bot\n\n"
    retString+="Rolls:\n"+\
    "(num)d[dieType](b[bestNum])(+[modifier]) - Rolls (num), defaults to 1, [dieType] sided dice.\n"+\
    "Optionally, you may add the best of and modifier sections.\n"+\
    "b[bestNum] takes the best [bestNum] results from the rolled dice assuming [bestNum]<=(num).\n"+\
    "+[modifier] adds the given [modifier] value to the roll's sum."
    return retString
    
def value_test(die):
    global distribution
    results = [0]*die
    for i in range(100000):
        if distribution=="true":
            value = random.randint(1,die)
        elif distribution=="fun":
            value = random.choices(range(1,die+1),weights=([1]*(die-1))+[1.2], k=1)[0]
        else:
            value = 1
        results[value-1]+=1
    return results
@bot.event
async def on_message(message):
    global distribution
    global luckyGuy
    global unluckyGuy
    global fixes
    numDie = 1
    dieKind = 20
    bestSelector = -1
    additive = 0
    cmd = ""
    if message.content[0:2] == '//' or message.content[0:2] == '!!':
        cmd = message.content[2:].lower()
    elif message.content[0:1] == '!' or message.content[0:1] == '/':
        cmd = message.content[1:].lower()
    is_dm = False
    is_player = False
    if isinstance(message.author, discord.Member):
        for role in message.author.roles:
            if role.guild==bot.guilds[0] and role.name == "DM":
                is_dm = True
            elif role.guild==bot.guilds[0] and role.name == "Player":
                is_player = True
    if message.author.name=="jackson" and message.author.discriminator=="0941":
        permis = 0
    elif is_dm:
        permis = 1
    elif is_player:
        permis = 2
    else:
        permis = 3
    if cmd!="":
        if cmd=="true" and permis<2:
            distribution = "true"
            await message.channel.send("distribution = true")
        elif cmd=="fun" and permis<2:
            distribution = "fun"
            await message.channel.send("distribution = fun")
        elif cmd=="check" and permis<2:
            await message.channel.send("luck = " + luckyGuy + "\nunluck = " + unluckyGuy + "\ndist = " + distribution)
        elif cmd=="exit" and permis==0:
            await bot.logout()
            #exit()
        elif cmd=="help":
            if isinstance(message.channel, discord.DMChannel) or message.channel.name=="dm_stuff":
                await message.channel.send(helpText(permis))
            else:
                await message.channel.send(helpText(2))
        elif cmd=="restartfun" and permis<2:
            setLucks()
        elif cmd.startswith("checkrng") and permis<2:
            results = value_test(int(cmd.split(" ")[1]))
            await message.channel.send(str(results))
        elif cmd.startswith("fixnext") and permis<2:
            cmds = cmd.split(" ")
            fixes[cmds[1]]=int(cmds[2])
        else:
            args = cmd.split('d')
            if args[0].isdigit():
                numDie = int(args[0])
            if args[1].find('b')!=-1:
                args2 = args[1].split('b')
                if args2[0].isdigit():
                    dieKind = int(args2[0])
                if args2[1].find('+')!=-1:
                    args3 = args2[1].split('+')
                    if args3[0].isdigit():
                        bestSelector = int(args3[0])
                    if args3[1].isdigit():
                        additive = int(args3[1])
                elif args2[1].find('-')!=-1:
                    args3 = args2[1].split('-')
                    if args3[0].isdigit():
                        bestSelector = int(args3[0])
                    if args3[1].isdigit():
                        additive = -1*int(args3[1])
                else:
                    if args2[1].isdigit():
                        bestSelector = int(args2[1])
            else:
                if args[1].find('+')!=-1:
                    args3 = args[1].split('+')
                    if args3[0].isdigit():
                        dieKind = int(args3[0])
                    if args3[1].isdigit():
                        additive = int(args3[1])
                elif args[1].find('-')!=-1:
                    args3 = args[1].split('-')
                    if args3[0].isdigit():
                        dieKind = int(args3[0])
                    if args3[1].isdigit():
                        additive = -1 * int(args3[1])
                else:
                    if args[1].isdigit():
                        dieKind = int(args[1])
            await message.channel.send(roll_die(message.author, numDie, dieKind, bestSelector, additive))
bot.run(botAuth.token)