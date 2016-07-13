from twython import Twython, TwythonError
from threading import Timer
from secrets import *
from random import randint

import nltk
from math import exp

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

#dictionary of words to replace
replace = { "America": "Feminism",
			"American": "Feminist",
			"Americans": "Feminists",
			"#AmericaFirst": "#FeminismFirst",
			"amazing": "feminist",
			"bad": "sexist",
			"broken": "sexist",
			"charity": "equality",
			"child": "girl",
			"children": "daughters",
			"Christian": "Sister",
			"Christians": "Sisters",
			"Church": "Sisterhood",
			"Church's": "Sisterhood's",
			"Clinton": "and Misogynists",
			"condemn": "oppress",
			"condemnation": "oppression",
			"conservative": "feminist",
			"Conservative": "Feminist",
			"conservatives": "feminists",
			"Conservatives": "Feminists",
			"corrupt": "misogynist",
			"country": "equality",
			"Country": "Equality",
			"death": "inequality",
			"Death": "Inequality",
			"deficit": "sexism",
			"Democrat": "Misogynist",
			"Democratic": "Misogynistic",
			"evil": "misogyny",
			"evils": "misogyny",
			"everyone": "all women",
			"everybody": "all women",
			"faith": "feminism",
			"Faith": "Feminism",
			"father": "mother",
			"fathers": "mothers",
			"forgiveness": "equality",
			"friendship": "feminism",
			"freedom": "equality",
			"Freedom": "Equality",
			"freedoms": "equality",
			"good": "feminist",
			"great": "feminist",
			"gun": "equality",
			"guns": "equality",
			"guy": "lady",
			"guys": "ladies",
			"hate": "misogyny",
			"he": "she",
			"He": "She",
			"Hillary": "Sexists",
			"him": "her",
			"Him": "Her",
			"his": "her",
			"His": "Her",
			"holy": "womanly",
			"Holy": "Womanly",
			"horrible": "sexist",
			"hunger": "misogyny",
			"human": "woman",
			"humanity": "womanhood",
			"illegal": "misogynist",
			"illegals": "misogynists",
			"immigrant": "sexist",
			"immigrants": "sexists",
			"immigration": "sexism",
			"ineffective": "oppressive",
			"institution": "sisterhood",
			"institutions": "sisterhoods",
			"Islam": "Sexism",
			"Islamic": "Sexist",
			"jobs": "equality",
			"killer": "sexist",
			"King": "Queen",
			"king": "queen",
			"life": "womanhood",
			"love": "feminism",
			"Love": "Feminism",
			"#MakeAmericaGreatAgain": "#MakeAmericaFeministAgain",
			"media": "patriarchy",
			"mercy": "equality",
			"Muslim": "Misogyny",
			"Muslims": "Misogynists",
			"NRA": "Feminists",
			"others": "other women",
			"Obama": "Misogynists",
			"People": "Women",
			"people": "women",
			"person": "woman",
			"press": "patriarchy",
			"racist": "misogynist",
			"racism": "misogyny",
			"Republican": "Feminist",
			"Republicans": "Feminists",
			"safe": "feminist",
			"savage": "misogynist",
			"Saudi Arabia": "the Patriarchy",
			"selfishness": "misogyny",
			"sick": "sexist",
			"sin": "sexism",
			"sinful": "misogynistic",
			"sins": "sexism",
			"smart": "feminist",
			"son": "daughter",
			"sons": "daughters",
			"supporter": "feminist",
			"supporters": "feminists",
			"system": "patriarchy",
			"terrible": "sexist",
			"terror": "misogyny",
			"Terror": "Misogyny",
			"terrorism": "misogyny",
			"terrorists": "misogynists",
			"terrorist": "misogynist",
			"thug": "misogynist",
			"thugs": "misogynists",
			"trouble": "inequality",
			"#Trump": "#Feminism",
			"#TrumpTrain": "#FeministTrain",
			"#Trump2016": "#Feminism2016",
			"violent": "misogynistic",
			"voter": "ally",
			"voters": "allies",
			"weak": "sexist",
			"wrong": "sexist"
			}




def getTrumpTweet():
	"""
	Gets Trump's latest tweet
	"""
	trump_timeline = twitter.get_user_timeline(screen_name="realDonaldTrump",count=1)
	for tweet in trump_timeline:
		#print(tweet['text'].encode('utf8')).decode('utf8')
		print("Got Trump Tweet!")
		return tweet['text'].encode('utf8').decode('utf8')




def makeNewTweet(tweetWords, hotWords):
	"""
	Takes a list of words and makes it "Feminist"
	tweetWords is the list of words
	
	hotwords is a dictionary of words in the tweet that have been frequently
	used in past tweets. The dictionary contains the words and their "temperature"
	and the number of tweets since the word has been used
	"""
	numEdits = 0					#counter of number of changes made to tweet
	newWords = []					#put new tweet in this list
	index = 0						#index of current word being looked at


	for x in tweetWords:			#for each word in the tweet
		havePunc = False			#Whether or not it has punctuation
		punc = ''

		#The current character count of the tweet
		currLen = len(' '.join(newWords[:index] + tweetWords[index:]))


		#if there is punctuation with the word being checked
		if x[-1] == ',' or x[-1] == '.' or x[-1] == '?' or x[-1] == '!' or x[-1] == ':' or x[-1] == ';':
			havePunc = True 		#it has punctuation
			punc = x[-1:]			#store the punctuation for later
			X = x[:-1]				#set the word to just the word with no punctuation
		elif x[-2:] == "'s":		#if the word is possessive
			havePunc = True
			punc = "'s" 			#store the 's
			X = x[:-2]				#set the word to just the word
		else:
			X = x 					#Otherwise make no changes


		if X == '&amp':
			newWords.append('&')
		elif X in replace and len(replace[X] + punc) - len(X + punc) + currLen <= 140:	#if it's a key word and adding it doesn't put tweet over 140 char
			# print(X + " " + str(len(replace[X] + punc) - len(X + punc) + currLen))
			newWords.append(replace[X] + punc)											#replace it
			numEdits += 1						    									#add to the number of edits
		elif X.lower() in replace and len(replace[X.lower()] + punc) - len(X.lower()+ punc) + currLen <= 140:
				
			if X == X.lower().capitalize():												#check for capitalization
				newWords.append(replace[X.lower()].capitalize() + punc)
			else:
				newWords.append(replace[X.lower()].upper() + punc)						#or all caps
			numEdits += 1						    									#add to the number of edits
		elif X.lower() in hotWords and hotWords[X.lower()][0] >= 80 and currLen <= 131:	#Check if the word is "hot"
			newWords.append("feminism" + punc)											#replace it if it is "hot enough"
			numEdits += 1 																#add to number of edits
		else:									   										#else don't change it
			newWords.append(X + punc)
		index += 1 																		#update current index

	currLen = len(' '.join(newWords))

	#if these key words are in the tweet, add these hashtags at the end
	if ('woman' in newWords or 'all' in newWords or 'all women' in newWords or 'women' in newWords) and len(' '.join(newWords)) <= 127:
		newWords.append('#yesallwomen')
		numEdits += 1

	if ("girl" in newWords or "girls" in newWords or "daughter" in newWords or "daughters" in newWords) and len(' '.join(newWords)) <= 128:
		newWords.append("#ToTheGirls")
		numEdits += 1

	if "equality" in newWords and len(' '.join(newWords)) <= 128:
		newWords.append("#Planet5050")
		numEdits += 1

	if ("sexism" in newWords or "misogyny" in newWords or "misogynistic" in newWords) and len(' '.join(newWords)) <= 125:
		newWords.append("#EverydaySexism")
		numEdits += 1


	currLen = len(' '.join(newWords))				#update current character count
	print("Character Count:",currLen)

	if(numEdits < 1):								#if no changes to tweet
		return None									#return None
	return newWords 								#Else return the new tweet



def tweet(tweet):
	"""
	Tweets a string
	"""
	twitter.update_status(status = tweet);



def decay(currTemp, tweetsSince):
	"""
	Exponential Decay function
	Adjusts the current "temperature"
	of a word used in tweets
	currTemp is the last temperature recorded
	tweetsSince is the number of tweets since the last
	temperature was recorded.
	"""
	ret = float(format(currTemp * exp((-0.1) * tweetsSince), '.2f'))
	return ret


def getHotWords(tweetText):
	"""
	Returns a dictionary of "hot" words in
	the tweet and updates the temperature of
	words recorded in past tweets
	"""
	common = open('common.txt', 'r')								#Open text file of 'common' words
	commonList = common.readlines()									#Make file into list
	commonDict = {}													#Make dictionary that will hold all recorded words, their
																	#"temperatures", and tweets since last recorded
	

	for line in commonList:											#For each entry in the 'common' list
		elements = line.split()										#Put them in the dictionary
		commonDict[elements[0]] = [elements[1], elements[2]]
	common.close()

	# print(commonDict)

	text = nltk.word_tokenize(tweetText)							#Get just the words from the tweet (no punctuation)
	tags = nltk.pos_tag(text)										#Tag each part of speech
	# print(tags)

	common = open('common.txt', 'w')

	hotWords = {}													#Make dictionary to store "hot" words from this tweet

	for word in tags:												#Look through each word in the tweet
		if (not word[0] in replace) and (word[1] == 'NNP' or word[1] == 'NN'):					#If it's a noun
			if word[0].lower() in commonDict:						#Update it's temp if its already in the common Dictionary
				newTemp = decay(float(commonDict[word[0].lower()][0]), int(commonDict[word[0].lower()][1]))
				commonDict[word[0].lower()] = [float(format(newTemp + 25.0, '.2f')), 0]
			else:													#Otherwise add it to the dictionary
				commonDict[word[0].lower()] = [50.0, 0]				#With an initial temperature
			# common.write(word[0].lower() + '\n')

			hotWords[word[0].lower()] = commonDict[word[0].lower()]	#Add it to the "hot" Words dictionary for this tweet


	#Delete words from common dictionary that have not been mentioned in tweets recently
	delWords = []													#Make a list of words to delete
	for word in commonDict:											#Go through each entry in the common dictionary

		if not (word in hotWords):													#if the word isn't in the current tweet
			newTemp = decay(float(commonDict[word][0]), int(commonDict[word][1]))	#update it's temperature (it will get "colder")
			if newTemp <= 0:														#If the temperature is below 0
				delWords.append(word)												#delete it from common words dictionary
			else:																	#Otherwise, update the number of tweets
				commonDict[word] = [newTemp, int(commonDict[word][1]) + 1]			#since it's been mentioned			
	for word in delWords:
		del commonDict[word]

	#Rewrite the common words file
	for x in commonDict:
		xStr = str(x)
		numStr = str(commonDict[x][0])
		daysSinceStr = str(commonDict[x][1])
		newStr = xStr + " " + numStr + " " + daysSinceStr + " \n"
		common.write(newStr)

	common.close()

	return hotWords	#return the "hot" words from the tweet dictionary



lastTweet = None		#to store the last tweet that was edited by the bot


def runBot():
	print("Bot running!")

	trumpTweet = getTrumpTweet()						#Get Trump's most current tweet
	
	# trumpTweet = ''

	
	hotWords = getHotWords(trumpTweet)					#Get and update "hot" words (commonly used words)

	global lastTweet

	if trumpTweet != lastTweet:							#make sure the bot hasn't edited the tweet before
		trumpTweetWords = trumpTweet.split()			#turn the tweet into a list of words
		
		try:
			print(trumpTweet)
		except:
			print("Cannot print Trump tweet")

		newTweetWords = makeNewTweet(trumpTweetWords, hotWords)	#Edit the tweet

		if newTweetWords == None:						#If no changes to tweet
			print("No changes to tweet!")
		else:											#Otherwise
			newTweet = ' '.join(newTweetWords) 			#combine the words into one string

			try:
				print(newTweet)
			except:
				print("Cannot print")

			if (not debug):								#If not in debug mode
				try:
					tweet(newTweet)						#Tweet the new tweet
					print("I just tweeted!")
				except:
					print("Ran into a problem tweeting!")

		lastTweet = trumpTweet 							#make this the latest tweet
	else:
		print("No new Tweet!")






def setInterval(func, sec):
	def func_wrapper():
		setInterval(func, sec)
		func()
	t = Timer(sec, func_wrapper)
	t.start()
	return t


debug = True
runOnce = True

runBot()
if not runOnce:
	setInterval(runBot, 60*60*1)		#runs every hour