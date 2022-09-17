import pyautogui as pog
import time, random

pog.PAUSE = 0.5
target_image_size = 1024
render_instances = 25
camera_focal_length = 35
render_wait_time = 1
import_wait_time = 1

blocks_file = open('E:\\Documents\\PRGM\\NEURAL\\Blocks\\parts-popular.txt','r')

blocks = [block.replace('\n','') for block in blocks_file.readlines()]
time.sleep(2)

# Need 30241_22, 64567_24

for block in blocks[94:]:

    t0 = time.time()

    x_range = list(range(0,355,5))
    random.shuffle(x_range)
    y_range = list(range(0,355,5))
    random.shuffle(y_range)
    z_range = list(range(0,355,5))
    random.shuffle(z_range)

    angles = [(x_range[idx],y_range[idx],z_range[idx]) for idx in range(render_instances)]

    pog.moveTo(43,36) # File Menu
    pog.click(43,36) 

    #time.sleep(3)

    pog.moveTo(43,300) # Import
    pog.moveTo(315,525)
    time.sleep(0.2)
    pog.click(315,525) # LDraw Import
    pog.moveTo(850,55) #File Path Text Field
    pog.click(850,55) #File Path Text Field

    
    pog.typewrite('E:\\DATA\\blocks\\ldraw\\parts\\'+block+'.dat')

    #s = input('...')
    pog.click(1275,1010) #Finish Import
    pog.click(1275,1010) #Finish Import

    time.sleep(import_wait_time)
    
    pog.PAUSE = 0.2

    pog.click(1600,444) #Render Properties Tab
    pog.click(1770,441) # Switch From Cycles
    pog.click(1770,462) # ^
    pog.click(1770,462) # ^

    #s = input('...')

    pog.moveTo(1630,840)
    pog.click(1630,840) #Film
    
    pog.moveTo(1743,893) #Toggle Transparency
    pog.click(1743,893)

    #s = input('..')
    
    pog.moveTo(1600,480)
    pog.click(1600,480) #View Layer Properties
    pog.moveTo(1825,465)
    pog.click(1825,465) #Change Res X
    pog.hotkey('delete')
    pog.typewrite(str(target_image_size)) #Enter X Res
    #pog.hotkey('enter')
    pog.hotkey('tab')
    pog.hotkey('delete')
    pog.typewrite(str(target_image_size)) #Enter Y Res
    pog.hotkey('enter')
    

    pog.moveTo(1900,165) # Remove Ground Plane From Render
    pog.click(1900,165)

    pog.moveTo(1700,149) # Select Camera Object
    pog.click(1700,149)

    pog.moveTo(1600,715) # View Camera Properties
    pog.click(1600,715)

    pog.moveTo(1800,535) # Select Focal Length
    pog.click(1800,535)

    pog.typewrite(str(camera_focal_length))
    pog.hotkey('enter')

    #s = input('.....')

    pog.moveTo(1700,125) # Select Object For Rotation
    pog.click(1700,125)

    pog.moveTo(275,85) #Object Menu
    pog.click(275,85)

    pog.moveTo(275,130) # Origin Menu
    time.sleep(0.2)

    pog.moveTo(500,150) # Set Origin To Geometry
    pog.click(500,150)

    pog.moveTo(1600,630) # Object Properties
    pog.click(1600,630)
    
    for index,instance in enumerate(range(render_instances)):
        pog.moveTo(1800,565) # X Rotation
        pog.click(1800,565)
        pog.hotkey('delete')
        pog.typewrite(str(angles[index][0])) #Enter X Rotation

        pog.hotkey('tab')
        pog.hotkey('delete')
        pog.typewrite(str(angles[index][1])) #Enter Y Rotation

        pog.hotkey('tab')
        pog.hotkey('delete')
        pog.typewrite(str(angles[index][2])) #Enter Z Rotation
        pog.hotkey('enter')

        #pog.PAUSE = 0.5

        pog.hotkey('f12') #Render image


        time.sleep(render_wait_time)

        pog.hotkey('alt','s')

        
        pog.moveTo(1440,54) # File Location Bar
        pog.click(1440,54)
        pog.hotkey('delete')
        pog.typewrite('E:\\DATA\\blocks\\rendered_images')
        pog.hotkey('enter')

        pog.moveTo(1230,1010) # Name Bar #,885
        pog.click(1230,1010)
        pog.typewrite(block+'_'+str(index)+'.png')
        pog.hotkey('enter')

        pog.moveTo(1655,1010) # Save Button
        pog.click(1655,1010)

        pog.moveTo(1890,25) # Close Render Window
        pog.click(1890,25)

        #s = input('....')

    pog.hotkey('ctrl','n') # New Workspace
    pog.moveTo(1825,75) 
    pog.click(1825,75)

    pog.moveTo(1000,570) #Do Not Save Button
    pog.click(1000,570)

    pog.PAUSE = 0.5

    print("--- %s seconds ---" % (time.time() - t0))