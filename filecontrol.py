from os import path

def getSongList(songName):
    songList = []

    with open(path.join("songs", songName)) as file:
        for line in file:
            songList.append(line.strip('\n\r'))

    return songList

def getHighScore():
    with open(path.join("data", "highscore.txt")) as file:
        return int(file.readline().strip('\n\r'))

def setHighScore(score):
    with open(path.join("data", "highscore.txt"), 'w') as file:
        file.write(str(score))