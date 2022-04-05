from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from random import choice,randint
import array, time
import rp2

#Oled Display
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128,64,i2c)

#configure Buttons
btn_up = Pin(4, Pin.IN, Pin.PULL_UP)
btn_down = Pin(5, Pin.IN, Pin.PULL_UP)
btn_select = Pin(6, Pin.IN, Pin.PULL_UP)

#Player Selection values
x = 0
Player = 0

# Configure the number of WS2812 LEDs.
NUM_LEDS = 34
PIN_NUM = 2
brightness = 0.2

#Colors
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
COSTUME = (25, 55, 150)
COLORS = (ORANGE, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, COSTUME)

#Neopixel configuration
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()


# Create the StateMachine with the ws2812 program, outputting on pin
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))

# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(NUM_LEDS)])

##########################################################################
def pixels_show():
    dimmer_ar = array.array("I", [0 for _ in range(NUM_LEDS)])
    for i,c in enumerate(ar):
        r = int(((c >> 8) & 0xFF) * brightness)
        g = int(((c >> 16) & 0xFF) * brightness)
        b = int((c & 0xFF) * brightness)
        dimmer_ar[i] = (g<<16) + (r<<8) + b
    sm.put(dimmer_ar, 8)
    time.sleep_ms(10)

def pixels_set(i, color):
    ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]

color = BLACK
for i in range(NUM_LEDS):
    pixels_set(i,color)
    pixels_show()

#Player Selection
if Player == 0:
    while (x != 3):

        if not (btn_up.value()):
            if((Player == 6)):
                if not btn_up.value():
                    Player = 1
                    time.sleep(0.5)
            else:
                Player += 1
                time.sleep(0.1)
                while not btn_up.value():
                    time.sleep(0.1)
        elif not btn_down.value():
            if (Player >= 1):
                Player -= 1
                time.sleep(0.1)
                while not btn_down.value():
                    time.sleep(0.1)
        elif not btn_select.value():
            x = 3
            break
            time.sleep(0.1)
            while not btn_select.value():
                    time.sleep(0.1)
        oled.fill(0)
        oled.text("Player: "+str(Player), 30, 30)
        oled.show()
time.sleep(1)

while btn_select.value():
    #Rules 
    oled.fill(0)
    oled.text("Rules:",0,0)
    oled.text("Nils loses",0,10)
    oled.text("Drink or exercise",0,20)
    oled.text("Press select",0,40)
    oled.show()

oled.fill(0)
oled.text("Game start",30,30)
oled.show()

Part = NUM_LEDS // Player

#Game
while True:
    
    Active = randint(1,Player)
    oled.fill(0)
    oled.text("Active: "+str(Active),30,30)
    oled.show()
    if Active == 1:
        color = choice(COLORS)
        for i in range(0, Part):
            pixels_set(i,color)
            pixels_show()
        continue
    elif Active == 2:
        color = choice(COLORS)
        for i in range(Part,(2* Part)):
            pixels_set(i,color)
            pixels_show()
        continue
    elif Active == 3:
        color = choice(COLORS)
        for i in range((2*Part),(3*Part)):
            pixels_set(i,color)
            pixels_show()
        continue
    elif Active == 4:
        color = choice(COLORS)
        for i in range((3*Part),(4*Part)):
            pixels_set(i,color)
            pixels_show()
        continue
    elif Active == 5:
        color = choice(COLORS)
        for i in range((4*Part),(5*Part)):
            pixels_set(i,color)
            pixels_show()
        continue
    elif Active == 6:
        color = choice(COLORS)
        for i in range((5*Part), NUM_LEDS):
            pixels_set(i,color)
            pixels_show()
        continue
    else:
        oled.text("Finish",30,30)
        break
    color = BLACK
    for i in range(NUM_LEDS):
        pixel_set(i,color)
        pixel.show()




print ("ende")

