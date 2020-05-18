# DiceBot
DnD discord bot for dice rolls

Bot rolls dice allowing for:
Any number of any type of die (all dice must be of the same type for one command)
"best of" commands obtaining the best few results
Added modifiers
Adds up the sum of the results and modifiers

Alternate random distributions:
true - pseudorandom results, all with equal weight
fun - Chooses two players, one gets higher odds for a max roll and the other gets higher odds for a minimum roll.
	- These odds are set up by giving the weighted outcome a weight of 1.2 rather than 1.

Commands may/must be prefixed by /, //, !, or !!

Normal Commands:
help - Shows this help message

DM Commands:
true - Sets rolls to follow true random distribution
fun - Sets rolls to follow fun distribution
check - Shows which players are affected by fun distribution
checkrng [num] - Rolls 100000 d[num]s and displays results using current distribution
fixnext [player] [num] - Guarantees [player]'s next roll to be a [num] if possible
restartfun - Picks new players to be affected by the fun distribution

Owner Commands:
exit - Turns off the bot

Rolls:
(num)d[dieType](b[bestNum])(+[modifier]) - Rolls (num), defaults to 1, [dieType] sided dice.
Optionally, you may add the best of and modifier sections.
b[bestNum] takes the best [bestNum] results from the rolled dice assuming [bestNum]<=(num).
+[modifier] adds the given [modifier] value to the roll's sum. 


