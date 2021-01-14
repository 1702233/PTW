import time
import RPi.GPIO as GPIO
import random
GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( 0 )

led_pin = 18
switch_pin = 23
servo_pin = 25
trig_pin = 20
echo_pin = 21
shift_clock_pin = 5
latch_clock_pin = 6
data_pin = 13
strip_clock_pin = 19
strip_data_pin = 26

class led:
    """
    initializes a Led on the given pin_nr
    set_led can then be called to turn the led on or off
    """
    
    led_pin = 0
    
    def __init__( self, led_pin ):
        self.led_pin = led_pin
        GPIO.setup( self.led_pin, GPIO.OUT )
        
    def set_led( self, on ):
        if on:
            GPIO.output( self.led_pin, GPIO.HIGH )
            return
        GPIO.output( self.led_pin, GPIO.LOW )
    
class switch:
    """
    initializes a switch on the given pin_nr
    the switch will be initialized as pulled down
    get_switch will return a boolean on wether the switch is pressed or not
    """
    
    switch_pin = 0

    def __init__( self, switch_pin ):
        self.switch_pin = switch_pin
        GPIO.setup( self.switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )

    def get_switch( self ):
        return GPIO.input( self.switch_pin )

class servo:
    """
    initializes a servo on the given pin_nr
    the servo can then be set in 1 of 100 positions with the set_servo function
    """
    
    servo_pin = 0

    def __init__( self, servo_pin ):
        self.servo_pin = servo_pin
        GPIO.setup( self.servo_pin, GPIO.OUT )

    def set_servo( self, position ):
        GPIO.output( self.servo_pin, GPIO.HIGH )
        time.sleep( 0.0005 + ( 0.00002 * position ))
        GPIO.output( self.servo_pin, GPIO.LOW )
        time.sleep( 0.0195 - ( 0.00002 * position ))

class SR04:
    """
    initializes a SR04 distance sensor when given a pin_nr of the echo and trigger pin
    get distance can then be called to get the distance measured in cm
    get_distance will take a minimum of 0.06 second to run in order to avoid muliple calls misreaping data
    """
    
    trigger_pin = 0
    echo_pin = 0

    def __init__( self, trigger_pin, echo_pin ):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        GPIO.setup( self.trigger_pin, GPIO.OUT )
        GPIO.setup( self.echo_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
        self.get_distance #first measurement is always wrong so this gets rid of that data

    def get_distance( self ):
        GPIO.output( self.trigger_pin, GPIO.HIGH )
        time.sleep(0.000001)
        GPIO.output( self.trigger_pin, GPIO.LOW )
        while not GPIO.input( self.echo_pin ):
            pass
        init_time = time.perf_counter()
        while GPIO.input( self.echo_pin ):
            pass
        time_passed = time.perf_counter() - init_time
        time.sleep(0.06)
        return ( ( time_passed * 343 ) * 50 )

class register:
    """
    initializes a shifting register when given the shift clock latch clock and data pin
    set_bit can be used to shift a single bit into the register
    set_byte can be used to sen da byte into the regsiter
    """
    
    shift_clock_pin = 0
    latch_clock_pin = 0
    data_pin = 0
    delay = 0.1

    def __init__( self, shift_clock_pin, latch_clock_pin, data_pin ):
        self.shift_clock_pin = shift_clock_pin
        self.latch_clock_pin = latch_clock_pin
        self.data_pin = data_pin

        GPIO.setup( self.shift_clock_pin, GPIO.OUT )
        GPIO.setup( self.latch_clock_pin, GPIO.OUT )
        GPIO.setup( self.data_pin, GPIO.OUT )

    def set_bit( self, value ):
        if value:
            GPIO.output( self.data_pin, GPIO.HIGH )
        else:
            GPIO.output( self.data_pin, GPIO.LOW )
        GPIO.output( self.shift_clock_pin, GPIO.HIGH )
        GPIO.output( self.shift_clock_pin, GPIO.LOW )
        GPIO.output( self.latch_clock_pin, GPIO.HIGH )
        GPIO.output( self.latch_clock_pin, GPIO.LOW )
        time.sleep( self.delay )

    def set_byte( self, value ):
        byter = bytes([value])
        byte = byter[0]
        for x in range(8):
            bit = (byte >> x) & 1
            if bit == 1:
                GPIO.output( self.data_pin, GPIO.HIGH )
            else:
                GPIO.output( self.data_pin, GPIO.LOW )
            GPIO.output( self.shift_clock_pin, GPIO.HIGH )
            GPIO.output( self.shift_clock_pin, GPIO.LOW )
            time.sleep( self.delay )
        GPIO.output( self.latch_clock_pin, GPIO.HIGH )
        GPIO.output( self.latch_clock_pin, GPIO.LOW )

class led_strip:
    """
    initializes a led strip when given a clock and data pin
    the set_colors function can be called to set the colors of the strip
    this function always needs a list, wich can either be a list of lists each containing an RGB value
    or it can be called using strings with wil be converted into the RGB value
    the class remembers teh previous colors and thus the set_colors can be called with less than 8 colors
    """
    
    clock_pin = 0
    data_pin = 0

    options = { "red": [ 0, 0, 255 ], "green": [ 0, 255, 0 ], "blue": [ 255, 0, 0],
                "white": [ 255, 255, 255 ], "yellow": [ 0, 255, 255 ], "orange": [ 0, 128, 255 ],
                "pink": [ 255, 0, 255 ], "gray": [ 128, 128, 128 ], "black": [ 0, 0, 0 ],
                "lime": [ 0, 255, 128], "cyan": [ 255, 255, 0 ], "purple": [ 255, 0, 128 ]}

    colors = [ [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
               [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0] ]
    
    delay = 0.3

    def __init__( self, clock_pin, data_pin ):
        self.clock_pin = clock_pin
        self.data_pin = data_pin

        GPIO.setup( self.clock_pin, GPIO.OUT )
        GPIO.setup( self.data_pin, GPIO.OUT )

    def apa102_send_bytes( self, bytes ):
        for byte in bytes:
            for x in range(8):
                bit = (byte >> x) & 1
                if bit == 1:
                    GPIO.output( self.data_pin, GPIO.HIGH )
                elif bit == 0:
                    GPIO.output( self.data_pin, GPIO.LOW )
                GPIO.output( self.clock_pin, GPIO.HIGH )
                GPIO.output( self.clock_pin, GPIO.LOW )
        
    def apa102( self ):
        self.apa102_send_bytes( bytes([0,0,0,0]) )
        for x in range(len(self.colors)):
            self.apa102_send_bytes( bytes([255]) )
            self.apa102_send_bytes( bytes(self.colors[x]) )
        self.apa102_send_bytes( bytes([255, 255, 255, 255]) )

    def set_colors( self, colors ):
        for x in range(len(colors)):
            if isinstance(colors[x], list):
                self.colors[x] = colors[x]
            elif colors[x].lower() in self.options:
                self.colors[x] = self.options[colors[x]]
            else:
                print("not a valid color")
                self.colors[x] = [ 0, 0, 0 ]
        self.apa102()
        
                            

led_1 = led( led_pin )
switch_1 = switch( switch_pin )
servo_1 = servo( servo_pin )
SR04_1 = SR04( trig_pin, echo_pin )
reg_1 = register( shift_clock_pin, latch_clock_pin, data_pin ) 
led_strip_1 = led_strip( strip_clock_pin, strip_data_pin )    

led_strip_1.set_colors(["cyan", "orange", "yellow", "gray", "white", "purple", "pink", "black"])
                    
while True:
    reg_1.set_byte( 170 )
    reg_1.set_byte( 85 )
    if SR04_1.get_distance() < 10:
        break

    
while True:
    if switch_1.get_switch():
        led_1.set_led( True )
        servo_1.set_servo( random.randint(1, 100) )
        time.sleep(0.05)
    else:
        led_1.set_led( False )
    time.sleep( 0.1 )

