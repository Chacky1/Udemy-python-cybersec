import os.path
import subprocess
import sys
import random
import string
import cryptography.fernet

def generateMasterPassword():
  key = cryptography.fernet.Fernet.generate_key()
  with open("./master.key", "wb") as masterPasswordWriter:
    masterPasswordWriter.write(key)

def loadMasterPassword():
  return open("./master.key", "rb").read()

def createVault():
  vault = open('./vault.txt', 'wb')
  vault.close()

def encryptData(data):
  f = cryptography.fernet.Fernet(loadMasterPassword())
  with open("./vault.txt", "rb") as vaultReader:
    encryptedData = vaultReader.read()
  if encryptedData.decode() == '':
    return f.encrypt(data.encode())
  else:
    decryptedData = f.decrypt(encryptedData)
    newData = decryptedData.decode() + data
    print(newData)
    return f.encrypt(newData.encode())

def decryptData(encryptedData):
  f = cryptography.fernet.Fernet(loadMasterPassword())
  return f.decrypt(encryptedData)

def appendNewPassword():
  print()
  userName = input("Veuillez entrer un nom d'utilisateur : ")
  password = input("Veuillez entrer le mot de passe : ")
  website = input("Veuillez entrer l'adresse du site web : ")
  print()

  userNameLine = "Nom d'utilisateur : " + userName + "\n"
  passwordLine = "Mot de passe : " + password + "\n"
  websiteLine = "Site Web : " + website + "\n\n"

  encryptedData = encryptData((userNameLine + passwordLine + websiteLine))
  with open("./vault.txt", "wb") as vaultWriter:
    vaultWriter.write(encryptedData)

def readPasswords():
  encryptedData = ''
  with open("vault.txt", "rb") as passwordsReader:
    encryptedData = passwordsReader.read()
  print()
  print(decryptData(encryptedData).decode())

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

if os.path.exists('./vault.txt') and os.path.exists('./master.key'):
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
else:
  print("Génération d'un mot de passe maître et d'un fichier de stockage...")
  generateMasterPassword()
  createVault()
  print("Génération terminée, veuillez relancer le programme.")