#Setup
import pygame
import socket
import threading
PORT = 9999
SERVER = '107.23.250.168'
#SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Client.connect(ADDR)
def send(msg):
    msg = str(msg)
    Message = msg.encode('utf-8')
    msg_length = len(Message)
    send_length = str(msg_length).encode('utf-8')
    send_length += b' '*(64-len(send_length))
    Client.send(send_length)
    Client.send(Message)
def recv():
    msg_length = Client.recv(64).decode('utf-8')
    if msg_length:
        msg_length = int(msg_length)
        msg = Client.recv(msg_length).decode('utf-8')
        return msg
    else:
        pass
def CMD():
    if input('') == 'CMD':
        send('CMD')
        send(input(''))
        if recv() == 'CMD UNLOCKED':
            while True:
                send(input('CMD: '))
def Host_Game():
    send('host')
    print(recv())
    print(recv())
def Join_Game():
    global User_Input
    global Entered_Code
    send('player')
    while True:
        print(User_Input)
        print(Entered_Code)
        if Entered_Code == True:
            break
    send(User_Input)
    print(recv())
def Server_Receiver():
    global Cash                           
    global Power
    global Clicker
    send('singleplayer')
    while True:
        msg = recv()
        msg = msg.split(' ')
        if msg[0] == 'Clicker':
            Clicker = int(msg[1])
        elif msg[0] == 'Power':
            Power = int(msg[1])
        elif msg[0] == 'Cash':
            Cash = float(msg[1])



pygame.init()

screen = pygame.display.set_mode((1400,800))
pygame.display.set_caption('Tycoon!')
game_running = False
Cash = 0
Power = 0
Clicker = 0
Battery_Cap = 5
Mouse_Down = False
Shop_Open = False
Delay = False
Modes_Menu_Open = False
Code_Recv = False
Hosted_Game = False
Joined_Game = False
Entered_Code = False
Text_Break = False
Server_Connected = False
User_Input = ''

#Owned

Battery_Workers = 0

DisplayFont = pygame.font.Font(None,100)

#Load

Background = pygame.image.load("Graphics\Menu\MenuBackground.png").convert_alpha()
Start_Button = pygame.image.load("Graphics\Menu\Start_Button.png").convert_alpha()
Modes_Button = pygame.image.load("Graphics\Menu\Modes_Button.png").convert_alpha()
Host_A_Game_Button = pygame.image.load("Graphics\Menu\Host_Multiplayer_Button.png").convert_alpha()
Join_A_Game_Button = pygame.image.load("Graphics\Menu\Join_Multiplayer_Button.png").convert_alpha()
Modes_Button = pygame.image.load("Graphics\Menu\Modes_Button.png").convert_alpha()
Modes_Background = pygame.image.load("Graphics\Menu\Modes_Background.png").convert_alpha()
Shop_Button = pygame.image.load("Graphics\Shop\Shop_Button.png").convert_alpha()
Shop_Background = pygame.image.load("Graphics\Shop\Shop_Background.png").convert_alpha()
Buy_Battery_Worker_Button = pygame.image.load("Graphics\Shop\Buy_Battery_Worker.png").convert_alpha()
Increase_Battery_Button = pygame.image.load("Graphics\Shop\Increase_Battery_Cap.png").convert_alpha()
Sell_Button = DisplayFont.render('SELL', True, 'yellow')
Start_Button_Rect = Start_Button.get_rect(center = (700,400))
Modes_Button_Rect = Modes_Button.get_rect(center = (700,450+Start_Button.get_height()))
Modes_Background_Rect = Modes_Background.get_rect(center = (700,400))
Host_A_Game_Button_Rect = Host_A_Game_Button.get_rect(bottomleft = (Modes_Background_Rect.left,Modes_Background_Rect.bottom))
Join_A_Game_Button_Rect = Join_A_Game_Button.get_rect(bottomleft = (Modes_Background_Rect.left,Host_A_Game_Button_Rect.top))
CMD_Thread = threading.Thread(target=CMD)
CMD_Thread.start()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            send('[DISCONNECT]')
            pygame.quit()
            exit()
    pygame.display.update()
    mouse_pos = pygame.mouse.get_pos()

    #Menu

    if game_running == False:
        if event.type == pygame.KEYDOWN:
            if Joined_Game == True and Modes_Menu_Open == True and Text_Break == False:
                if event.key == pygame.K_BACKSPACE:
                    Text_Break = True
                    User_Input = User_Input[:-1]
                elif event.key == pygame.K_KP_ENTER:
                    Text_Break = True
                    Entered_Code = True
        if event.type == pygame.TEXTINPUT and Text_Break == False:
            Text_Break = True
            User_Input += event.text
        elif event.type == pygame.KEYUP and Text_Break == True:
            Text_Break = False
        screen.blit(Background,(0,0))
        screen.blit(Start_Button, Start_Button_Rect)
        screen.blit(Modes_Button, Modes_Button_Rect)
        if pygame.mouse.get_pressed() == (True, False, False) or Modes_Menu_Open == True:
            if Start_Button_Rect.collidepoint(mouse_pos) and Modes_Menu_Open == False:
                screen.fill('black')
                game_running = True
            elif Modes_Button_Rect.collidepoint(mouse_pos) or Modes_Menu_Open == True:
                Modes_Menu_Open = True
                screen.blit(Modes_Background, Modes_Background_Rect)
                screen.blit(Host_A_Game_Button, Host_A_Game_Button_Rect)
                screen.blit(Join_A_Game_Button, Join_A_Game_Button_Rect)
                if pygame.mouse.get_pressed() == (True, False, False) and Modes_Menu_Open == True:
                    if Host_A_Game_Button_Rect.collidepoint(mouse_pos) and Hosted_Game == False:
                        Hosted_Game = True
                        Host_Thread = threading.Thread(target=Host_Game)
                        Host_Thread.start()
                    elif Join_A_Game_Button_Rect.collidepoint(mouse_pos) and Joined_Game == False:
                        Joined_Game = True
                        Join_Thread = threading.Thread(target=Join_Game)
                        Join_Thread.start()
            if not Modes_Background_Rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed() == (True, False, False) and Modes_Menu_Open == True:
                Modes_Menu_Open = False

    #Server

    if game_running == True and Server_Connected == False:
        Server_Connected = True
        Server_Tread = threading.Thread(target=Server_Receiver)
        Server_Tread.start()

    #Displays

    if game_running == True:
        screen.fill('black')
        Cash_Display = DisplayFont.render(f'Cash: ${Cash}', True, 'green')
        Power_Display = DisplayFont.render(f'Power: {Power}/{Battery_Cap}', True, 'yellow')
        screen.blit(Cash_Display,(0,0))
        screen.blit(Power_Display,(0,Cash_Display.get_height()))
    
    #Manual Power

        if game_running == True:
            Power_Button = DisplayFont.render(f'Click to create Power ({Clicker}/3)', True, 'blue')
            Power_Button_Rect = Power_Button.get_rect(topleft = (0,Cash_Display.get_height()+Power_Display.get_height()))
            screen.blit(Power_Button,Power_Button_Rect)
            if event.type == pygame.MOUSEBUTTONDOWN and Mouse_Down == True:
                if Power_Button_Rect.collidepoint(mouse_pos):
                    Mouse_Down = False
            else:
                if event.type == pygame.MOUSEBUTTONUP and Mouse_Down == False:
                    if Power_Button_Rect.collidepoint(mouse_pos):
                        Mouse_Down = True
                        send('Clicker')


    #Sell Button

    if game_running == True:
        Sell_Button_Rect = Sell_Button.get_rect(topleft = (Power_Button.get_width()+200,Power_Button_Rect.top))
        screen.blit(Sell_Button,Sell_Button_Rect)
        if Sell_Button_Rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, 'yellow', Sell_Button_Rect)
            Sell_Button = DisplayFont.render('SELL', True, 'black')
            screen.blit(Sell_Button,Sell_Button_Rect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                send('Sell')
        else:
            Sell_Button = DisplayFont.render('SELL', True, 'yellow')
            screen.blit(Sell_Button,Sell_Button_Rect)
    
    #Shop

    if game_running == True:
        Shop_Button_Rect = Shop_Button.get_rect(topright = (1400,Sell_Button_Rect.bottom))
        Shop_Background_Rect = Shop_Background.get_rect(center = (700,400))
        Buy_Battery_Worker_Button_Rect = Buy_Battery_Worker_Button.get_rect(topleft = (Shop_Background_Rect.left+100,Shop_Background_Rect.top+150))
        Increase_Battery_Button_Rect = Increase_Battery_Button.get_rect(topleft = (Buy_Battery_Worker_Button_Rect.right+100,Shop_Background_Rect.top+150))
        screen.blit(Shop_Button,Shop_Button_Rect)
        if event.type == pygame.MOUSEBUTTONUP and Shop_Button_Rect.collidepoint(mouse_pos) and Shop_Open == False:
            Shop_Open = True
        elif event.type == pygame.MOUSEBUTTONDOWN and Shop_Open == True and not Shop_Background_Rect.collidepoint(mouse_pos):
            Shop_Open = False
        if Shop_Open == True:
            screen.blit(Shop_Background,Shop_Background_Rect)
            screen.blit(Buy_Battery_Worker_Button,Buy_Battery_Worker_Button_Rect)
            screen.blit(Increase_Battery_Button,Increase_Battery_Button_Rect)
    if Shop_Open == True:
        if event.type == pygame.MOUSEBUTTONDOWN and Mouse_Down == True:
                Mouse_Down = False
        else:
            if event.type == pygame.MOUSEBUTTONUP and Mouse_Down == False:
                if Buy_Battery_Worker_Button_Rect.collidepoint(mouse_pos):
                    Mouse_Down = True
                    send('Buy Battery Worker')
                else:
                    if Increase_Battery_Button_Rect.collidepoint(mouse_pos):
                        Mouse_Down = True
                        if Cash == 5 or Cash > 5:
                            Cash -= 5
                            Battery_Cap += 5
    
    #Owned
    
    if Battery_Workers == 1 or Battery_Workers > 1:
        if Delay == False:
            Delay = True
            Reset = 0
            Current_Time = int(pygame.time.get_ticks()/1000)
        if Current_Time == 10 or Current_Time > 10:
            Reset = int(pygame.time.get_ticks()/1000)
            Current_Time = int(pygame.time.get_ticks()/1000)-Reset
            if Power+Battery_Workers*1 < Battery_Cap:
                Power += Battery_Workers*1
            else:
                Power = Battery_Cap
        else:
            if Current_Time == 0 or Current_Time > 0:
                Current_Time = int(pygame.time.get_ticks()/1000)-Reset
        print(Current_Time)

    pygame.display.update()
    clock = pygame.time.Clock()
    clock.tick(100)
