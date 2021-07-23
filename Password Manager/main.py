import os.path
import subprocess
import sys
import random
import string
import bcrypt

def checkExistence():
  if os.path.exists("vault.txt"):
    pass
  else:
    file = open("vault.txt", "w")
    file.close()

def hashPassword(password):
  salt = bcrypt.gensalt()
  hash = bcrypt.hashpw(password.encode('utf-8'), salt)
  return hash

def appendNewPassword():
  with open("vault.txt", "a") as appender:
    print()
    userName = input("Veuillez entrer un nom d'utilisateur : ")
    password = input("Veuillez entrer le mot de passe : ")
    website = input("Veuillez entrer l'adresse du site web : ")
    print()

    hashedPassword = hashPassword(password)

    userNameLine = "Nom d'utilisateur : " + userName + "\n"
    passwordLine = "Mot de passe : " + str(hashedPassword) + "\n"
    websiteLine = "Site Web : " + website + "\n"

    appender.write('-' * 60 + '\n')
    appender.write(userNameLine)
    appender.write(passwordLine)
    appender.write(websiteLine)
    appender.write('-' * 60 + '\n')

def readPasswords():
  content = ''
  with open("vault.txt", "r") as reader:
    content = reader.read()
  print()
  print(content)

def generateNewPassword(passwordLength):
  randomString = string.ascii_letters + string.digits + string.punctuation
  newPassword = ''
  for i in range(passwordLength):
    newPassword += random.choice(randomString)
  print()
  print("Voici votre mot de passe : " + newPassword)


# Partie principale du programme
subprocess.call('clear', shell=True)

print('-' * 60)
print("Bienvenue dans le gestionnaire de mots de passe !")
print('-' * 60)

print("Vous pouvez sélectionner l'une des options suivantes : ")
print("1 - Sauvegarder un nouveau mot de passe")
print("2 - Générer un nouveau mot de passe aléatoire")
print("3 - Obtenir la liste de vos mots de passe")

userChoice = input("Que souhaitez-vous faire ? (1/2/3) ")

if userChoice == "1":
  appendNewPassword()
elif userChoice == "2":
  passwordLength = input("Quelle est la longueur souhaitée pour le mot de passe ? ")
  if not (string.ascii_letters in passwordLength):
    generateNewPassword(int(passwordLength))
  else:
    print("Merci de rentrer un nombre la prochaine fois...")
    sys.exit()
elif userChoice == "3":
  readPasswords()
else:
  print("L'option sélectionnée n'existe pas...")
  sys.exit()