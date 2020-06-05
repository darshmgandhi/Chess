import pygame
import pygame.gfxdraw
from pygame.locals import *



#Player Class-------------------------------------------------------------------
class Player():    
 mate=0
 chess_Pieces=[['Wp','Wr','Wh','Wb','Wq','Wk'],['Bq','Bk','Bb','Bh','Br','Bp']]
 score_Board={'p':1,'q':9,'r':5,'b':3,'h':3}
 turn=0
 noOfMoves=0
 sequence=['WHITE','BLACK']

 def __init__(self,colour):
  self.score=0
  self.colour=colour
  self.moves_Performed=[]
  
 #Gets called as soon as player plays a move
 def finishMove(self,taken_Piece,taken_Index,chosen_Piece):
  global alphaboard   
  printPiece(chosen_Piece,(bwidth,bheight),indexToCoords(taken_Index))
  inboard[taken_Index]=chosen_Piece     
  if taken_Piece!='e':   
   self.score+=self.score_Board[taken_Piece[1]]
   Player.noOfMoves=0
  if rule.checkForCheck(inboard,Player.turn)==True:
   Player.mate=2
  else:
   Player.mate=0
  rule.legal_Moves=[]
  Player.noOfMoves+=1
  self.moves_Performed.append([chosen_Piece+alphaboard[chosen_Index],taken_Piece+alphaboard[taken_Index]])
  chosen_Piece='e'
  Player.turn=abs(Player.turn-1)
  Rules.simboard=inboard.copy()
  rule.checkMate(Rules.simboard,self.turn)
  Player.mate=rule.staleMate(self)
  
 #Covers the entire process of player clicking on a piece and playing a move
 def movePiece(self):
  global inboard
  global mouseClicked
  global chosen_Piece
  global chosen_Index
  for event in pygame.event.get():
   if event.type==pygame.MOUSEBUTTONDOWN and mouseClicked==False:
    chosen_Index=coordsToIndex(pygame.mouse.get_pos())
    chosen_Piece=inboard[chosen_Index]
    if chosen_Piece in self.chess_Pieces[self.turn]:
     mouseClicked=True
     Rules.simboard=inboard.copy()
     inboard[chosen_Index]='e'
     printPiece(chosen_Piece,(bwidth,bheight),(pygame.mouse.get_pos()[0]-(bheight//2),pygame.mouse.get_pos()[1]-(bwidth//2)))
   elif event.type==pygame.MOUSEBUTTONUP and mouseClicked==True:
    if chosen_Piece in self.chess_Pieces[self.turn]:       
     move_Index=coordsToIndex(pygame.mouse.get_pos())
     move_Piece=inboard[move_Index]     
     if chosen_Index!=move_Index and rule.checkValidity(move_Index)==True:
      self.finishMove(move_Piece,move_Index,chosen_Piece)
     else:
      inboard[chosen_Index]=chosen_Piece
      printPiece(chosen_Piece,(bwidth,bheight),indexToCoords(chosen_Index))
     mouseClicked=False
  if mouseClicked==True:  
   if chosen_Piece in self.chess_Pieces[self.turn]:  
    rule.placeCheckRestrictions(chosen_Piece,chosen_Index)
    rule.plotValidMoves()   
    printPiece(chosen_Piece,(bwidth,bheight),(pygame.mouse.get_pos()[0]-(bheight//2),pygame.mouse.get_pos()[1]-(bwidth//2)))



#Chess Rules Class--------------------------------------------------------------
class Rules():
 valid_Moves=[]
 final_valid_Moves=[]
 check_Player=2
 simboard=[]

 def lateralMoves(self,Piece,Index,board):
  for i in range(Index-8,-1,-8):
   Rules.valid_Moves.append(i)
   if board[i]!='e':
    break    
  for i in range(Index+1,(Index//8)*8+8):
   Rules.valid_Moves.append(i)
   if board[i]!='e':
    break
  for i in range(Index+8,64,8):
   Rules.valid_Moves.append(i)
   if board[i]!='e':
    break    
  for i in range(Index-1,(Index//8)*8-1,-1):
   Rules.valid_Moves.append(i)
   if board[i]!='e':
    break     

 def diagonalMoves(self,Piece,Index,board):
  for i in range(Index,0,-7):
   Rules.valid_Moves.append(i)
   if board[i] not in ['e',Piece] or i%8==7:
    break    
  for i in range(Index,63,7):
   Rules.valid_Moves.append(i)
   if board[i] not in ['e',Piece] or i%8==0:
    break
  for i in range(Index,-1,-9):
   Rules.valid_Moves.append(i)
   if board[i] not in ['e',Piece] or i%8==0:   
    break    
  for i in range(Index,64,9):
   Rules.valid_Moves.append(i)
   if board[i] not in ['e',Piece] or i%8==7:
    break
  for i in range(0,4):
   if Index in Rules.valid_Moves:   
    Rules.valid_Moves.remove(Index)
   

 def computeValidMoves(self,Piece,Index,board):
  
  #Pawn
  if Piece[0]=='W': 
   chosen_Operand=1
  elif Piece[0]=='B': 
   chosen_Operand=-1   
  if Piece[1]=='p':
   if (Index-8*chosen_Operand) in range(0,64):     
    if board[Index-8*chosen_Operand]=='e':   
     Rules.valid_Moves.append(Index-8*chosen_Operand)
    if ((Index in range(8,16) and Piece[0]=='B') or (Index in range(47,56) and Piece[0]=='W')) and board[Index-16*chosen_Operand]=='e':
     Rules.valid_Moves.append(Index-16*chosen_Operand)
    if board[Index-7*chosen_Operand]!='e' and ((Index-8*chosen_Operand)%8!=int(7/2+(chosen_Operand*7/2))): 
     Rules.valid_Moves.append(Index-7*chosen_Operand)
    if board[Index-9*chosen_Operand]!='e' and ((Index-8*chosen_Operand)%8!=int(7/2-(chosen_Operand*7/2))):
     Rules.valid_Moves.append(Index-9*chosen_Operand)

  #Rook
  elif Piece[1]=='r':    
   self.lateralMoves(Piece,Index,board)

  #Bishop  
  elif Piece[1]=='b':
   self.diagonalMoves(Piece,Index,board)    

  #Queen
  elif Piece[1]=='q':
   self.lateralMoves(Piece,Index,board)
   self.diagonalMoves(Piece,Index,board)

  #Knight
  elif Piece[1]=='h': 
   knight_Moves=[[{6:-2,-17:-1,15:-1,-10:-2},0,1],[{-6:2,10:2,-15:1,17:1},1,0]]
   for i in knight_Moves:
    for j in i[0].keys():    
     if (Index+j) in range(0,64) and (Index+i[0][j])%8 in range(0+i[0][j]*i[1],8+i[0][j]*i[2]):
      Rules.valid_Moves.append(Index+j)

  #King
  elif Piece[1]=='k':
   king_Moves=[-1,-9,7,-8,8,1,-7,9]
   for i in king_Moves:
    if (Index+i) in range(0,64):
     if (Index%8==0 and king_Moves.index(i)>2) or (Index%8==7 and king_Moves.index(i)<5) or (Index%8 in range(1,7)):    
      Rules.valid_Moves.append(Index+i)    
        
  #Remove the moves of the same side                
  for i in range(len(Rules.valid_Moves)-1,-1,-1):
   if Piece[0]=='W' and board[Rules.valid_Moves[i]][0]=='W':
    Rules.valid_Moves.remove(Rules.valid_Moves[i])
   elif Piece[0]=='B' and board[Rules.valid_Moves[i]][0]=='B':
    Rules.valid_Moves.remove(Rules.valid_Moves[i])
   
  Rules.final_valid_Moves=Rules.valid_Moves
  Rules.valid_Moves=[]
  return Rules.final_valid_Moves
       
  #Plot all the valid moves
 def plotValidMoves(self):
  for i in Rules.final_valid_Moves: 
   if inboard[i]=='e':
    pygame.draw.circle(win,(0,255,0),(indexToCoords(i)[0]+bwidth//2,indexToCoords(i)[1]+bheight//2),7)
   else:
    pygame.draw.rect(win,(255,0,0),(indexToCoords(i)[0],indexToCoords(i)[1],bwidth-2,bheight-2),4)       
  pygame.draw.rect(win,(0,0,255),(indexToCoords(chosen_Index)[0],indexToCoords(chosen_Index)[1],bwidth-2,bheight-2),4)

 #Check the validity of the move
 def checkValidity(self,move_Index):
  if move_Index in Rules.final_valid_Moves:
   return True 
  else:   
   return False

 #Check for the King's Check condition
 def checkForCheck(self,board,turn):
  legal_Moves=[]
  for i in range(0,64):
   if (turn==0 and board[i][0]=='W') or (turn==1 and board[i][0]=='B'):    
    legal_Moves+=self.computeValidMoves(board[i],i,board)
  for i in legal_Moves:   
   if (board[i]=='Bk' and turn==0) or (board[i]=='Wk' and turn==1):
    legal_Moves=[]    
    return True
  else:
   legal_Moves=[]
   return False
   
 #If a player is in check, places restrictions on it's pieces
 def placeCheckRestrictions(self,check_Piece,check_Index): 
  check_Moves=self.computeValidMoves(check_Piece,check_Index,inboard).copy()
  for i in range(len(check_Moves)-1,-1,-1):
   Rules.simboard[check_Index]='e'
   kill_Piece=Rules.simboard[check_Moves[i]]
   Rules.simboard[check_Moves[i]]=check_Piece
   a=check_Moves[i]
   if self.checkForCheck(Rules.simboard,abs(Player.turn-1))==True:
    check_Moves.pop(i)
   Rules.simboard[check_Index]=check_Piece
   Rules.simboard[a]=kill_Piece   
  Rules.final_valid_Moves=check_Moves
  return check_Moves

 #Check for checkmate 
 def checkMate(self,board,turn):
  check_mate_Moves=[]
  for i in range(0,64):
   if (turn==0 and board[i][0]=='W') or (turn==1 and board[i][0]=='B'):
    check_mate_Moves+=self.placeCheckRestrictions(board[i],i)
  if len(check_mate_Moves)==0:
   if rule.checkForCheck(board,abs(turn-1))==True:
    Player.mate=1
   else:  
    Player.mate=3

 #Check for stalemate: Includes 3 rules overall   
 def staleMate(self,Player):

  #Rule 1
  duplicate_Moves=0    
  if len(Player.moves_Performed)>1: 
   for i in range(0,len(Player.moves_Performed)):
    for j in range(0,len(Player.moves_Performed)):
     if Player.moves_Performed[i][0][0:2]+Player.moves_Performed[i][1][len(Player.moves_Performed[1])-2:]==Player.moves_Performed[j][0][0:2]+Player.moves_Performed[j][1][len(Player.moves_Performed[1])-2:]:
      duplicate_Moves+=1
    if duplicate_Moves>=3:
     break
    else: 
     duplicate_Moves=0

  #Eule 3 
  if Player.noOfMoves==100 or duplicate_Moves>=3:   
   Player.mate=3       
  return Player.mate      
      
#Initial Variables and Functions------------------------------------------------ 
bheight=60
bwidth=60
fps=60
board=[]
X=0
Y=0
global mate
mate=0
winheight=600
winwidth=1000
OffsetX=(winwidth-(bwidth*8))/2
OffsetY=(winheight-(bheight*8))/2
mouseClicked=False
Player1=Player('W')
Player2=Player('B')
rule=Rules()

#Load Pieces
 #Individual Chess Piece
def printPiece(piece,size,coordinates):
 global win   
 Image=pygame.image.load('alpha\\320\\'+piece+'.png')
 mainImg=pygame.transform.scale(Image,size)
 win.blit(mainImg,coordinates)

 #Initialize Chessboard
def loadpieces(inboard):
 global OffsetX
 global OffsetY
 global bheight
 global bwidth
 pX=0
 pY=0
 for i in inboard:
  if pX==(bwidth*8):
   pX=0
   pY+=bheight
  if i!='e':
   printPiece(i,(bwidth,bheight),(pX+OffsetX,pY+OffsetY))
  pX+=bwidth

  
#Datatype Converter
def coordsToIndex(c):
 global OffsetX
 global OffsetY
 d=(c[0]-OffsetX,c[1]-OffsetY)
 ind=((d[1]//60)*8)+(d[0]//60)
 return int(ind)
def indexToCoords(i):
 global OffsetX
 global OffsetY    
 y=(i//8)*60   
 x=(i%8)*60    
 return (int(x+OffsetX),int(y+OffsetY))

#For showing scores
def scoreboard(msg,coords):
 font=pygame.font.Font('freesansbold.ttf', 28)
 text=font.render(msg,True,(0,0,0))
 win.blit(text,coords)

#Beginning of code execution----------------------------------------------------
#Board Array
for i in range(64):
 if i%16<=7:   
  board.append(i%2)
 else:   
  board.append((i+1)%2) 
print(board)

#Initial game board
inboard=['Br','Bh','Bb','Bq','Bk','Bb','Bh','Br','Bp','Bp','Bp','Bp','Bp','Bp','Bp','Bp','e','e','e','e','e','e','e','e','e','e','e','e','e','e','e','e','e','e','e','e','e','e','e','e','e','e','e','e','e','e','e','e','Wp','Wp','Wp','Wp','Wp','Wp','Wp','Wp','Wr','Wh','Wb','Wq','Wk','Wb','Wh','Wr']
alphaboard=['8a','8b','8c','8d','8e','8f','8g','8h','7a','7b','7c','7d','7e','7f','7g','7h','6a','6b','6c','6d','6e','6f','6g','6h','5a','5b','5c','5d','5e','5f','5g','5h','4a','4b','4c','4d','4e','4f','4g','4h','3a','3b','3c','3d','3e','3f','3g','3h','2a','2b','2c','2d','2e','2f','2g','2h','1a','1b','1c','1d','1e','1f','1g','1h']

#Initializing pygame
pygame.init()
win=pygame.display.set_mode((winwidth,winheight))
pygame.display.set_caption("Chess")
clock=pygame.time.Clock()

#Game Loop----------------------------------------------------------------------
while True:
 #Speed
 clock.tick(fps)    
 #Input
 for event in pygame.event.get():
  if event.type==pygame.QUIT:
   pygame.quit()    
 #Board
 win.fill((255,255,255))
 for i in board:
  if X==(bwidth*8):
   X=0
   Y+=bheight
  if i==0:
   boxcol=(181,136,99)
  else:
   boxcol=(240,217,181)
  pygame.draw.rect(win,boxcol,(X+OffsetX,Y+OffsetY,bwidth,bheight)) 
  X+=bwidth
 X=0
 Y=0
 #Pieces
 loadpieces(inboard)
 #Interface
 scoreboard('Black',(OffsetX+bwidth*8+OffsetX//10,OffsetY))
 scoreboard(str(Player2.score),(OffsetX+bwidth*8+OffsetX//10,OffsetY+bheight))
 scoreboard('White',(OffsetX+bwidth*8+OffsetX//10,OffsetY+6*bheight+bheight//2))
 scoreboard(str(Player1.score),(OffsetX+bwidth*8+OffsetX//10,OffsetY+7*bheight+bheight//2))
 if Player.mate==1: 
  scoreboard('CHECKMATE',(OffsetX-(2*OffsetX//10)-180,OffsetY+4*bheight-15))
  scoreboard(Player.sequence[abs(Player.turn-1)]+' WINS',(OffsetX-(2*OffsetX//10)-180,OffsetY+4*bheight-15+30))
 elif Player.mate==2:
  scoreboard(Player.sequence[Player.turn]+' IN CHECK',(OffsetX-(2*OffsetX//10)-200,OffsetY+4*bheight-15))
 elif Player.mate==3:
  scoreboard('STALEMATE',(OffsetX-(2*OffsetX//10)-180,OffsetY+4*bheight-15))
 #Gameplay
 if Player.turn==0:
  Player1.movePiece()
 else:
  Player2.movePiece()
 pygame.display.flip()
