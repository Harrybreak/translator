'''
	CODE SOURCE DU BOT RADIO TPN
	programmé par HarryBreak;
	
	<--- Variables temporaires --->
	$data			: pour un objet
	$information 	: pour un long message
	$contenu 		: pour une longue liste
	$nombre 		: pour une quantité
	$position 		: pour une position
	$date			: pour une date
	$link			: pour un lien (fichier ou web)
	$a et $b 		: respectivement pour un point de départ et un point de fin
	$ligne 			: pour une position en ligne dans un fichier
	
	<--- Variables intemporaires --->
	$operateurs		: id  des utilisateurs possédant les hauts privilèges
	$operateursNom	: nom des utilisateurs possédant les hauts privilèges
'''

# Retirer toutes les occurences d'un caracètre dans une chaîne
def strremove(chaine, c):
	index = chaine.find(c)
	while index > -1:
		chaine = chaine[:index] + chaine[index+1:]
		index = chaine.find(c)
	return chaine

# Mettre un item à la fin d'une liste
def puttoend(liste, item):
	i = liste.index(item)
	return liste[:i] + liste[i+1:] + [liste[i]]

# Listes opérateurs (je m'ajoute :D )
operateurs = []
operateursNom = []
operateurs.append(280453752283201536)
operateursNom.append("Harrybreak")


# Les bibliothèques
from math import *
from googletrans import Translator, constants
import discord
import time
import datetime

# Les données de l'application
# Elles consistent à stocker la langue native de chaque utilisateur qui utilise le bot.
preferences = dict()
# Je m'ajoute :D
preferences[280453752283201536] = "French"


# Toute la base de donnée se situe dans le sous-repertoire "bdd" donc allons-y !
import os
os.chdir("bdd")

# Le token secret :)
token = ""

# La fonction de load/reload
def loadbdd():
	ligne = 1
	try:
		with open('bdd.txt', 'r') as file:
			for line in file:
				line = line.split(",")
				try:
					nombre = int(line[0])
				except TypeError:
					pass
				else:
					preferences[nombre] = line[1][:-1].lower()
				ligne += 1
	except FileNotFoundError:
		open('bdd.txt', 'w').close()
	# Pour le token
	try:
		with open('token.txt', 'r') as file:
			global token
			for line in file:
				token = line
				break
	except FileNotFoundError:
		return False
	return True

# Elle retourne False ou True selon si l'exécution échoue ou non
def savebdd():
	ligne = 1
	with open('bdd.txt', 'w') as file:
		for key,value in preferences.items():
			file.write(str(key)+","+value+"\r")
			ligne += 1
	return True

# La fonction de tentative d'envoi sur un channel privé
async def sendto(message, content):
	try:
		await message.author.send(content)
	except discord.Forbidden:
		await message.channel.send(content)
	except AttributeError:
		pass

async def trydelmsg(message):
	try:
		await message.delete()
	except discord.Forbidden:
		pass

print("==========================================================")
print("Lecture des données dans la base de données ...")
loadbdd()
print("==========================================================")
print("Configuration du bot...")
# Configuration du reboot du bot
instance_intents = discord.Intents.default()
instance_intents.members = True
translator = Translator()

# Reboot du bot
client = discord.Client(intents=instance_intents)
@client.event
async def on_ready():
	data = discord.Game("End your message with an \"&\" and I translate what you say in English")
	await client.change_presence(activity = data)
	print("==========================================================")
	print("Le bot est connecté !")
	
@client.event
async def on_message(message):
	# Translation
	if len(message.content) > 1 and message.content[-1] == '&':
		if message.author.id in preferences and preferences[message.author.id] != "unknown":
			if len(message.content) > 2 and message.content[-2] == '&':
				information = translator.translate(message.content[:-2], src=preferences[message.author.id], dest="en").text
				await message.channel.send("**__"+message.author.name+" :__** "+information)
				await trydelmsg(message)
			else:
				information = translator.translate(message.content[:-1], src=preferences[message.author.id], dest="en").text
				await message.channel.send("**__"+message.author.name+" :__** "+information)
		else:
			preferences[message.author.id] = "unknown"
			await sendto(message, "Can you please choose first your native language by typing here ``&<*lang*>`` where *lang* is the name of your language **in English!** ?\nYou can get a non exhaustive list of availible languages by typing ``&<>``")
	# Asking for examples of native langs
	elif message.content == "&<>":
		information = "The 2 letter ISO format is supported : **it**, **en**, **cz**, **fr**, **de**, *etc*...\n"
		information += "Other formats are also supported.\n"
		information += "When you configure your native language, I test whether I can translate in your language or not :)\n"
		information += "__Example :__ **&<fr>** to set your native language to 'French' and **Bonjour&** to translate it in English."
		await sendto(message, information)
	# Setting native language
	elif message.content.startswith("&<") and message.content[-1] == '>':
		preferences[message.author.id] = message.content[2:-1]
		await sendto(message,"Your native language has been updated to "+message.content[2:-1]+"! An attempting is going to be written here...")
		try:
			await sendto(message, translator.translate("Everything's ok !", dest=message.content[2:-1], src="en").text)
		except ValueError:
			preferences[message.author.id] = "unknown"
			information = "**WRONG FORMAT !** Sorry but I can't translate in this language ;-;\nTry another language with ``&<*lang*>`` !\n"
			information += "The 2 letter ISO format is supported : **it**, **en**, **cz**, **fr**, **de**, *etc*...\n"
			information += "Another formats are also supported.\n"
			information += "When you configure your native language, I test whether I can translate in your language or not :)\n"
			information += "__Example :__ **&<fr>** to set your native language to 'French' and **Bonjour&** to translate it in English."
			await sendto(message, information)
	'''
	COMMAND SECTION
	'''
	if message.content.startswith("$"):
		## CMDS COMMAND
		if message.content.split()[0] == "$cmds":
			information = "__Here is the administrator commands list :__\n"
			information += "``$upg``: upgrade an user\n"
			information += "``$dwng``: downgrade an user\n"
			information += "``$save``: save server data base\n"
			information += "``$kill``: kill bot\n"
			information += "``$test``: debug current snapshot\n"
			information += "__Here is the common commands list :__\n"
			information += "``$cmds``: show this command list\n"
			information += "``$help``: get some help\n"
			information += "``$info``: get some info about me\n"
			await sendto(message, information)
		elif message.content.split()[0] == "$help":
			information = "__A brief introduction to Translator bot :__\n"
			information += "**Translator** is a bot who helps you to communicate with other people in multilingual servers. I can translate everything you say from any language into English. I aim to create better connections between people around the World Wide Web and enhance more international interactions !\n\n"
			information += "__Starting with me :__\n"
			information += "> **Translate what you say in English** : end your message with an ampersam ('&') and I'll try to translate it in English (*if you have set your native language first*)\n*You can also delete your message by ending your message with 2 ampersams ('&&') instead of one's.*\n"
			information += "> **Set your native language** : type ``&<*lang*>`` where *lang* is your native language in the 2 letter ISO Format (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)\n"
			information += "> **Still lost ?** : type ``&<>`` to get some examples of usages\n"
			information += "> **Other features** : the ``$cmds`` command show you what you can do else with me :)\n"
			information += "\n"
			information += "**Hope my services are helpful for you and every communities !**"
			await sendto(message, information)
		elif message.content.split()[0] == "$info":
			information = "__**Translator Discord Bot Bétà 1.1**__\n"
			information += "__Date of last release :__ 3.30.2022\n"
			information += "__Date of creation :__ 3.27.2022\n"
			information += "__Programmer :__ Harrybreak (:email: : harrybreak975@gmail.com)\n"
			information += "__Source code :__ https://github.com/Harrybreak/translator/releases\n"
			await sendto(message, information)
		## UPGRADE COMMAND (OPÉRATION QUI NÉCESSITE D'ÊTRE OPÉRATEUR)
		elif message.content.split()[0] == "$upg":
			if message.author.id in operateurs:
				contenu = message.content.split()
				if len(contenu) == 1 or (len(contenu) == 2 and contenu[1] == "help"):
					information = "Voici la liste des opérateurs:\n"
					for i in operateursNom:
						information += "+ " + str(i) + "\n"
					information += "Pour augmenter des utilisateurs, suivez cette commande de leur @pseudo."
					await message.author.send(information)
				elif len(contenu) > 1 and len(message.mentions) == 0:
					await message.author.send("**Erreur d'identification** ! Impossible d'augmenter les utilisateurs indiqués !")
				else:
					information = "Les utilisateurs suivants sont dorénavant des opérateurs :\n"
					for i in message.mentions:
						if not(i.id in operateurs):
							operateurs.append(i.id)
						if not(i.name in operateursNom):
							operateursNom.append(i.name)
							information += "+ " + i.name + "\n"
					await message.author.send(information)
			else:
				await message.author.send("**Permission error** ! This operation requires an elevation.")
		## DOWNGRADE COMMAND (OPÉRATION QUI NÉCESSITE D'ÊTRE OPÉRATEUR)
		elif message.content.split()[0] == "$dwng":
			if message.author.id in operateurs:
				contenu = message.content.split()
				if len(contenu) == 1 or (len(contenu) == 2 and contenu[1] == "help"):
					await message.author.send("Pour retirer les privilèges d'opérateur de plusieurs utilisateurs, suivez cette commande de leur @pseudo")
				elif len(contenu) > 1 and len(message.mentions) == 0:
					await message.author.send("**Erreur d'identification** ! Impossible d'identifier les utilisateurs indiqués !")
				else:
					information = "Les utilisateurs suivants ne jouissent dorénavant plus des privilèges d'opérateur :\n"
					for i in message.mentions:
						try:
							operateurs.remove(i.id)
							operateursNom.remove(i.name)
						except ValueError:
							information += "+ " + i.name + "  *(était déjà dépourvu des privilèges)*" + "\n"
						else:
							information += "+ " + i.name + "\n"
					information += "Pour leur redonner accès aux fonctions d'opérateur, utilisez la commande ``$upg``."
					await message.author.send(information)
			else:
				await message.author.send("**Permission error** ! This operation requires an elevation.")
		## KILL COMMAND
		elif message.content.split()[0] == "$kill":
			if message.author.id in operateurs:
				await message.author.send("**FERMETURE D'URGENCE DANS 5 SECONDES**")
				await client.close()
			else:
				await message.author.send("**Permission error** ! This operation requires an elevation.")
		## TEST COMMAND
		elif message.content.split()[0] == "$test":
			if message.author.id in operateurs:
				contenu = message.content.split()
				for i in range(len(message.attachments)):
					await message.attachments[i].save(fp = message.attachments[i].filename)
			else:
				await message.author.send("**Permission error** ! This operation requires an elevation.")
		## SAVE COMMAND
		# Déclaration des dictionnaires
		# m : MUSIQUE // d : DESSIN // s : SIMULATION INFORMATIQUE // p : DÉVELOPPEMENT // l : LITTÉRATURE // r : VMM // v : AVD // o : ORIGINAUX
		# dict = {artiste1 = [(date, linkorfilename),(date, linkorfilename),...], artiste2 = [(date, linkorfilename),(date, linkorfilename),...], ...}
		elif message.content.split()[0] == "$save":
			if message.author.id in operateurs:
				if savebdd():
					await message.author.send("Base de donnée sauvegardée !")
				else:
					await message.author.send("**Echec de la sauvegarde !**")
			else:
				await message.author.send("**Permission error** ! This operation requires an elevation.")
		## UNRECOGNIZED COMMAND
		else:
			pass
	'''
	END OF COMMAND SECTION
	'''
		

# Run le client
client.run(token)

# Lors de l'exécution du client
print("==========================================================")
print("Sauvegarde de la base de données en cours ...")
savebdd()
print("Sauvegarde terminée avec succès !")
print("Le bot a bien été déconnecté !")