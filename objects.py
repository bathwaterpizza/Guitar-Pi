import cfg
import pygame

class BoardLine:
    def __init__(self):
        self.posY = cfg.SCREEN_HEIGHT_HALF
        self.leftPos  = [2 * cfg.SCREEN_WIDTH_SIXTH, self.posY]
        self.rightPos = [4 * cfg.SCREEN_WIDTH_SIXTH, self.posY]
        self.width = cfg.BOARD_LINE_WIDTH
    
    def progress(self, step):
        self.posY += step

        self.leftPos[0] -= cfg.BOARD_LINE_POS_SCALER * step
        self.leftPos[1] = self.posY

        self.rightPos[0] += cfg.BOARD_LINE_POS_SCALER * step
        self.rightPos[1] = self.posY

        self.width += cfg.BOARD_LINE_SCALER_RATIO * step

class BoardNote:
    def __init__(self, layout):
        self.posY = cfg.SCREEN_HEIGHT_HALF
        self.notes = [
            Note(layout[0], [9  * (cfg.SCREEN_WIDTH_TWFOURTH), self.posY]),
            Note(layout[1], [11 * (cfg.SCREEN_WIDTH_TWFOURTH), self.posY]),
            Note(layout[2], [13 * (cfg.SCREEN_WIDTH_TWFOURTH), self.posY]),
            Note(layout[3], [15 * (cfg.SCREEN_WIDTH_TWFOURTH), self.posY])
        ]
        self.width = cfg.BOARD_NOTE_WIDTH
        self.rect = pygame.Rect(0, 0, cfg.BOARD_PICK_WIDTH_HALF, cfg.BOARD_PICK_WIDTH_HALF)
        self.rect.center = (cfg.SCREEN_WIDTH_HALF, cfg.SCREEN_HEIGHT_HALF) # type: ignore
    
    def progress(self, step):
        self.posY += step
        self.rect.center = (cfg.SCREEN_WIDTH_HALF, self.posY) # type: ignore

        self.notes[0].pos[0] -= cfg.BOARD_NOTE_POS_FAR_SCALER * step
        self.notes[1].pos[0] -= cfg.BOARD_NOTE_POS_CLOSE_SCALER * step

        self.notes[2].pos[0] += cfg.BOARD_NOTE_POS_CLOSE_SCALER * step
        self.notes[3].pos[0] += cfg.BOARD_NOTE_POS_FAR_SCALER * step

        for index in range(4):
            self.notes[index].pos[1] = self.posY

        self.width += cfg.BOARD_NOTE_SCALER_RATIO * step

class Note:
    def __init__(self, type, pos):
        self.type = type
        self.pos = pos
