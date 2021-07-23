from random import randint
import os

NUMBER_OF_TRIES_MAX = 10

def getPlayerScore(playerName):
  playerScore = 0
  if os.path.isfile('./scores/' + playerName + '.txt'):
    with open('./scores/' + playerName + '.txt', 'r') as reader:
      playerScore = reader.readline()
  return playerScore

def setNewPlayerScore(playerName, playerScore):
  with open('./scores/' + playerName + '.txt', 'w') as writer:
    writer.write(str(playerScore))

def getAWordFromDictionary():
  randomWord = ''
  with open('./dictionnaire.txt', 'r') as reader:
    words = reader.readlines()
    randomWord = words[randint(0, len(words))]
    if '\n' in randomWord:
      randomWord = randomWord[:len(randomWord)-1]
  return randomWord.lower()

def changeStarsInWordToFind(hiddenWord, wordToFind, letterGiven):
  newHiddenWord = ''
  if letterGiven in wordToFind:
    for i in range(len(wordToFind)):
      if wordToFind[i] == letterGiven:
        newHiddenWord += letterGiven
      else:
        newHiddenWord += hiddenWord[i]
  else:
    newHiddenWord = hiddenWord
  return newHiddenWord

def checkIfGameIsOver(numberOfTries, hiddenWord):
  return (numberOfTries >= NUMBER_OF_TRIES_MAX) or (hiddenWord.find('*') == -1)


print('*************************************************')
print('*********** Bienvenue au jeu du pendu ***********')
print('*************************************************')

playerName = input('Rentrez votre nom d\'utilisateur : ')
print()

print('Vous avez ' + str(NUMBER_OF_TRIES_MAX) + ' tentatives pour trouver le bon mot !')
print()

wordToFind = getAWordFromDictionary()
hiddenWord = '*' * len(wordToFind)
numberOfTries = 0
playerScore = int(getPlayerScore(playerName))

print('Votre score actuel s\'élève à : ' + str(playerScore))
print()

while(not checkIfGameIsOver(numberOfTries, hiddenWord)):
  print('Voici le mot à trouver : ' + hiddenWord)
  print('Il vous reste ' + str(NUMBER_OF_TRIES_MAX - numberOfTries) + ' tentatives.')
  playerLetter = input('Quel est votre lettre ? ')
  hiddenWord = changeStarsInWordToFind(hiddenWord, wordToFind, playerLetter.lower())
  numberOfTries += 1
  print()

if numberOfTries < NUMBER_OF_TRIES_MAX:
  print('Félicitations ! Vous avez deviné le mot caché !')
  playerScore += NUMBER_OF_TRIES_MAX - numberOfTries
  setNewPlayerScore(playerName, playerScore)
else:
  print('Dommage... Le mot caché était : ' + wordToFind)