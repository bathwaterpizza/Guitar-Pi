# type: ignore
import pygame, cfg, filecontrol, inputcontrol
from os import path
from objects import *

# ------------------- Definitions -------------------
def updateBoardLines():
    global boardLines

    for line in boardLines:
        line.progress(cfg.BOARD_PROGRESS_STEPSIZE * gameDT)

    # Offscreen lines
    if boardLines and boardLines[-1].posY > cfg.SCREEN_HEIGHT:
        del boardLines[-1]

def updateBoardNotes():
    global boardNotes

    for boardNote in boardNotes:
        boardNote.progress(cfg.BOARD_PROGRESS_STEPSIZE * gameDT)

    # Offscreen notes
    if boardNotes and boardNotes[-1].posY > cfg.SCREEN_HEIGHT + boardNotes[-1].width:
        for note in boardNotes[-1].notes:
            if note.type in 'rgby':
                removeLife()
                break

        del boardNotes[-1]

def drawBoardLines():
    for line in boardLines:
        pygame.draw.line(gameScreen, 'black', line.leftPos, line.rightPos, round(line.width))

def drawBoardNotes():
    for boardNote in boardNotes:
        for note in boardNote.notes:
            if note.type == '-':
                continue
            elif note.type == 'r':
                pygame.draw.circle(gameScreen, 'red', note.pos, boardNote.width)
            elif note.type == 'g':
                pygame.draw.circle(gameScreen, 'green', note.pos, boardNote.width)
            elif note.type == 'b':
                pygame.draw.circle(gameScreen, 'blue', note.pos, boardNote.width)
            elif note.type == 'y':
                pygame.draw.circle(gameScreen, 'yellow', note.pos, boardNote.width)
            elif note.type == 'x':
                pygame.draw.circle(gameScreen, 'black', note.pos, boardNote.width)
            
        # Show collision rect
        #pygame.draw.rect(gameScreen, 'orange', boardNote.rect)

def drawBackground():
    # Background
    gameScreen.fill('darkgrey')

    # Board
    pygame.draw.polygon(gameScreen, 'white', [
        (cfg.SCREEN_WIDTH_SIXTH, cfg.SCREEN_HEIGHT),
        (5 * cfg.SCREEN_WIDTH_SIXTH, cfg.SCREEN_HEIGHT),
        (4 * cfg.SCREEN_WIDTH_SIXTH, cfg.SCREEN_HEIGHT_HALF),
        (2 * cfg.SCREEN_WIDTH_SIXTH, cfg.SCREEN_HEIGHT_HALF)]
    )

    # Left outline
    pygame.draw.line(gameScreen, 'black',
        (cfg.SCREEN_WIDTH_SIXTH, cfg.SCREEN_HEIGHT),
        (2 * cfg.SCREEN_WIDTH_SIXTH , cfg.SCREEN_HEIGHT_HALF - 3),
        5
    )
    pygame.draw.line(gameScreen, 'black',
        (cfg.SCREEN_WIDTH_SIXTH - 5, cfg.SCREEN_HEIGHT),
        (2 * cfg.SCREEN_WIDTH_SIXTH , cfg.SCREEN_HEIGHT_HALF - 3),
        5
    )

    # Right outline
    pygame.draw.line(gameScreen, 'black',
        (5 * cfg.SCREEN_WIDTH_SIXTH, cfg.SCREEN_HEIGHT),
        (4 * cfg.SCREEN_WIDTH_SIXTH , cfg.SCREEN_HEIGHT_HALF - 3),
        5
    )
    pygame.draw.line(gameScreen, 'black',
        (5 * cfg.SCREEN_WIDTH_SIXTH + 5, cfg.SCREEN_HEIGHT),
        (4 * cfg.SCREEN_WIDTH_SIXTH , cfg.SCREEN_HEIGHT_HALF - 3),
        5
    )

    # Top outline
    pygame.draw.line(gameScreen, 'black',
        (2 * cfg.SCREEN_WIDTH_SIXTH, cfg.SCREEN_HEIGHT_HALF - 2),
        (4 * cfg.SCREEN_WIDTH_SIXTH, cfg.SCREEN_HEIGHT_HALF - 2),
        3
    )

def drawPicks():
    pygame.draw.line(gameScreen, '#8b0000', # Dark Red
        (cfg.BOARD_REDPICK_START, cfg.BOARD_PICK_HEIGHT),
        (cfg.BOARD_REDPICK_END, cfg.BOARD_PICK_HEIGHT),
        20 if 'r' in boardInput else 10
    )
    pygame.draw.line(gameScreen, '#013220', # Dark Green
        (cfg.BOARD_GREENPICK_START, cfg.BOARD_PICK_HEIGHT),
        (cfg.BOARD_GREENPICK_END, cfg.BOARD_PICK_HEIGHT),
        20 if 'g' in boardInput else 10
    )
    pygame.draw.line(gameScreen, '#00008B', # Dark Blue
        (cfg.BOARD_BLUEPICK_START, cfg.BOARD_PICK_HEIGHT),
        (cfg.BOARD_BLUEPICK_END, cfg.BOARD_PICK_HEIGHT),
        20 if 'b' in boardInput else 10
    )
    pygame.draw.line(gameScreen, '#FFD700', # Dark Yellow
        (cfg.BOARD_YELLOWPICK_START, cfg.BOARD_PICK_HEIGHT),
        (cfg.BOARD_YELLOWPICK_END, cfg.BOARD_PICK_HEIGHT),
        20 if 'y' in boardInput else 10
    )

def drawScoreText():
    renderText = gameFont_arial.render(str(gameScore), False, 'white')  
    gameScreen.blit(renderText, renderText.get_rect(topleft=(cfg.SCREEN_WIDTH_THIRD, cfg.SCREEN_HEIGHT_TWELVETH)))

    renderText = gameFont_arial.render(str(gameHighScore), False, 'gold')
    gameScreen.blit(renderText, renderText.get_rect(topright=(2 * cfg.SCREEN_WIDTH_THIRD, cfg.SCREEN_HEIGHT_TWELVETH)))

def drawEndText():
    renderText = gameFont_arial.render('Press SPACE to retry', False, 'white')
    gameScreen.blit(renderText, renderText.get_rect(center=(cfg.SCREEN_WIDTH_HALF, cfg.SCREEN_HEIGHT_THIRD)))

def drawLifeRects():
    for rect in gameLifeRects:
        pygame.draw.rect(gameScreen, 'white', rect)

def progressBoard():
    global boardTime, boardEnd
    
    boardTime += gameDT
    
    if boardTime > cfg.BOARD_PROGRESS_TIME:
        boardTime = 0

        nextNote = boardSong.pop(0)

        if nextNote == '.':
            endCurrentBoard()
        elif nextNote == '----':
            boardLines.insert(0, BoardLine())
        else:
            boardNotes.insert(0, BoardNote(nextNote))
            boardLines.insert(0, BoardLine())

def collidePicksWithNotes():
    if boardNotes and boardNotes[-1].rect.collidepoint((cfg.SCREEN_WIDTH_HALF, cfg.BOARD_PICK_HEIGHT)):        
        for index in range(4):
            if boardNotes[-1].notes[index].type == 'rgby'[index] and 'rgby'[index] in boardInput: # type: ignore
                modifyScore(1)
                pygame.mixer.Sound.play(gameSfx[index])
                boardNotes[-1].notes[index].type = '-'
            elif boardNotes[-1].notes[index].type == 'x' and 'rgby'[index] in boardInput: # type: ignore
                removeLife()
                pygame.mixer.Sound.play(gameSfx[4])
                boardNotes[-1].notes[index].type = '-'

def modifyScore(amount):
    global gameScore, gameHighScore, gameHeaderUpdate
    
    gameScore += amount

    if gameScore > gameHighScore:
        gameHighScore = gameScore
        
        filecontrol.setHighScore(gameHighScore)
    
    gameHeaderUpdate = True

def removeLife():
    global gameLives, boardEnd, gameHeaderUpdate

    if cfg.GAME_IGNORE_MISS: return

    gameLives -= 1
    if gameLifeRects: del gameLifeRects[-1]

    if gameLives <= 0:
        endCurrentBoard()

    gameHeaderUpdate = True

def endCurrentBoard():
    global boardEnd, gameHeaderUpdate

    boardEnd = True
    gameHeaderUpdate = True
    pygame.mixer.music.unload()

def loadGame():
    global gameRunning, gameFont_arial, gameClock, gameDT, gameLives, gameLifeRects, \
        gameScore, gameHighScore, boardEnd, boardTime, boardLines, boardNotes, boardInput, \
        boardSong, gameSfx, gameHeaderUpdate, gameScreen
    
    pygame.init()
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])

    if cfg.SCREEN_FULLSCREEN:
        flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
        gameScreen = pygame.display.set_mode((0, 0), flags)
    else:
        gameScreen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
        pygame.display.set_caption('Guitar Project')

    gameRunning = True
    gameFont_arial = pygame.font.SysFont('arial', cfg.SCREEN_WIDTH // 20)
    gameClock = pygame.time.Clock()
    gameDT = 0
    gameLives = cfg.GAME_MAXLIVES
    gameLifeRects = []
    gameScore = 0
    gameHighScore = filecontrol.getHighScore()
    gameSfx = [
        pygame.mixer.Sound(path.join('assets', cfg.GAME_AUDIO_RED)),
        pygame.mixer.Sound(path.join('assets', cfg.GAME_AUDIO_GREEN)),
        pygame.mixer.Sound(path.join('assets', cfg.GAME_AUDIO_BLUE)),
        pygame.mixer.Sound(path.join('assets', cfg.GAME_AUDIO_YELLOW)),
        pygame.mixer.Sound(path.join('assets', cfg.GAME_AUDIO_MISS))
    ]
    gameHeaderUpdate = True

    for mult in range(cfg.GAME_MAXLIVES):
        gameLifeRects.append(
            pygame.Rect(
                cfg.SCREEN_WIDTH_THIRD + (cfg.SCREEN_WIDTH_THIRD / cfg.GAME_MAXLIVES) * mult,
                5,
                (cfg.SCREEN_WIDTH_THIRD / cfg.GAME_MAXLIVES) - 5,
                cfg.SCREEN_HEIGHT / 24
            )
        )

    boardEnd = False
    boardTime = 0
    boardLines = []
    boardNotes = []
    boardInput = []
    boardSong = filecontrol.getSongList(cfg.GAME_START_SONG)

    pygame.mixer.music.load(path.join('assets', cfg.GAME_AUDIO_MUSIC))
    if cfg.GAME_ENABLE_MUSIC:
        pygame.mixer.music.play(-1)

    # Draw background once
    drawBackground()
    pygame.display.flip() if cfg.SCREEN_FULLSCREEN else pygame.display.update()

# ------------------- Setup -------------------
gameScreen = None
gameRunning = None
gameFont_arial = None
gameClock = None
gameDT = None
gameLives = None
gameLifeRects = None
gameScore = None
gameHighScore = None
gameSfx = None
gameHeaderUpdate = None
boardEnd = None
boardTime = None
boardLines = None
boardNotes = None
boardInput = None
boardSong = None

loadGame()

# ------------------- Main loop -------------------
while gameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
            break
        elif event.type == pygame.KEYDOWN:
            if boardEnd and event.key == pygame.K_SPACE: # Restart
                loadGame()
                break

    gameClock.tick(60)
    gameDT = gameClock.get_time()

    if not boardEnd: progressBoard()
    updateBoardLines()
    updateBoardNotes()

    boardInput = inputcontrol.getBoardInput()
    if boardInput: collidePicksWithNotes()

    drawBackground()

    if cfg.SCREEN_FULLSCREEN or gameHeaderUpdate:
        gameHeaderUpdate = False

        drawScoreText()
        drawLifeRects()

        if boardEnd:
            drawEndText()

        # Draw header render update area
        #pygame.draw.rect(gameScreen, 'blue', cfg.SCREEN_RENDERING_RECT_HEADER, 5)

        if not cfg.SCREEN_FULLSCREEN:
            pygame.display.update(cfg.SCREEN_RENDERING_RECT_HEADER)

    drawBoardLines()
    drawPicks()
    drawBoardNotes()

    # Draw board render update area
    #pygame.draw.rect(gameScreen, 'red', cfg.SCREEN_RENDERING_RECT_BOARD, 5)

    if cfg.SCREEN_FULLSCREEN:
        pygame.display.flip()
    else:
        pygame.display.update(cfg.SCREEN_RENDERING_RECT_BOARD)

pygame.quit()