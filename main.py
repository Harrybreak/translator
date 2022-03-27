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

# La fonction de merde mdr
def strremove(chaine, c):
	index = chaine.find(c)
	while index > -1:
		chaine = chaine[:index] + chaine[index+1:]
		index = chaine.find(c)
	return chaine
	
def puttoend(liste, item):
	i = liste.index(item)
	return liste[:i] + liste[i+1:] + [liste[i]]
	
# Listes opérateurs (je m'ajoute :D )
operateurs = []
operateursNom = []
operateurs.append(280453752283201536)
operateursNom.append("Harrybreak")



from math import *
from translate import Translator
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
	return True

# Elle retourne False ou True selon si l'exécution échoue ou non
def savebdd():
	ligne = 1
	with open('bdd.txt', 'w') as file:
		for key,value in preferences.items():
			file.write(str(key)+","+value+"\r")
			ligne += 1
	return True

print("==========================================================")
print("Lecture des données dans la base de données ...")
loadbdd()
print("==========================================================")
print("Configuration du bot...")
# Configuration du reboot du bot
instance_intents = discord.Intents.default()
instance_intents.members = True

# Reboot du bot
client = discord.Client(intents=instance_intents)
@client.event
async def on_ready():
	data = discord.Game("End your message with an \"&\" and I'll try to translate it in English")
	await client.change_presence(activity = data)
	print("==========================================================")
	print("Le bot est connecté !")
	
@client.event
async def on_message(message):
	if message.content[-1] == '&':
		if message.author.id in preferences and preferences[message.author.id] != "Unknown":
			data = Translator(from_lang = preferences[message.author.id], to_lang = "English")
			information = data.translate(message.content[:-1])
			if type(message.channel) == discord.DMChannel:
				await message.author.send(information)
			else:
				await message.channel.send("**__"+message.author.name+" :__** "+information)
		else:
			preferences[message.author.id] = "Unknown"
			await message.author.send("Can you please choose first your native language by typing here ``&<*lang*>`` where *lang* is the name of your language **in English!** ?\nYou can get a non exhaustive list of availible languages by typing ``&<>``")
	elif message.content == "&<>":
		information = "The 2 letter ISO is supported : **it**, **en**, **cz**, **fr**, **de**, *etc*...\n"
		information += "Another formats are also supported !\n"
		information += "When you configure your native language, I test whether I can translate in your language or not :)\n"
		await message.author.send(information)
	elif message.content.startswith("&<") and message.content[-1] == '>':
		preferences[message.author.id] = message.content[2:-1]
		await message.author.send("Your native language has been updated to "+message.content[2:-1]+"! An attempting is going to be written here...")
		data = Translator(to_lang=message.content[2:-1])
		await message.author.send(data.translate("Everything's ok !"))

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
			await message.channel.send(information)
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
				await message.delete()
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
				await message.delete()
		## KILL COMMAND
		elif message.content.split()[0] == "$kill":
			if message.author.id in operateurs:
				await message.author.send("**FERMETURE D'URGENCE DANS 5 SECONDES**")
				await client.close()
			else:
				await message.author.send("**Permission error** ! This operation requires an elevation.")
				await message.delete()
		## TEST COMMAND
		elif message.content.split()[0] == "$test":
			if message.author.id in operateurs:
				contenu = message.content.split()
				for i in range(len(message.attachments)):
					await message.attachments[i].save(fp = message.attachments[i].filename)
			else:
				await message.author.send("**Permission error** ! This operation requires an elevation.")
				await message.delete()
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
client.run("ODkwNTk4ODMyMTMwMzc5ODI3.YUyIzA.OQd906unLAB4zzaXYJ66e3JDwNg")

# Lors de l'exécution du client
print("==========================================================")
print("Sauvegarde de la base de données en cours ...")
savebdd()
print("Sauvegarde terminée avec succès !")
print("Le bot a bien été déconnecté !")