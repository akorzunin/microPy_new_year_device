from machine import Pin, I2C
import neopixel
import time
import ssd1306
import am2320
from ds3231_port import DS3231
import uasyncio as asyncio

from led_strip_effects import led_cleanup_effect, led_effect_1, rainbowCycle, week_day_routine_effect

i2c = I2C(1, sda=Pin(21), scl=Pin(22), freq=100000)
display = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3C)
ds3231 = DS3231(i2c)
sensor = am2320.AM2320(i2c)
sensor.measure()

D25 = Pin(25, Pin.OUT, 1)
D27 = Pin(27)
D33 = Pin(33, Pin.IN, Pin.PULL_UP)
np = neopixel.NeoPixel(D27, 30)
np.fill((0, 0, 0))
np.write()
print('init done')


def fill_all(*args):
    np.fill(args)
    np.write()


def draw_layout():
    display.fill(0)
    display.text('HUMIDITY:', 0, 24, 3)
    display.text('TEMP:', 0, 24+12, 1)


async def udpate_humidity():
    while True:
        D25.off()
        await asyncio.sleep_ms(50)
        sensor.measure()
        D25.on()
        await asyncio.sleep_ms(5000)


def udpate_time():
    a = ds3231.get_time()
    display.text('                ', 0, 12*4, 1)
    display.text(
        f'{a[2]:02}.{a[1]:02}   {a[3]:02}:{a[4]:02}:{a[5]:02}', 0, 12*4, 1)


def update_sensor_data():
    display.text(f'{sensor.humidity():.3} %', 80, 12*2, 1)
    display.text(f'{sensor.temperature():.3} C', 80, 12*3, 1)


async def update_display():
    while True:
        display.fill(0)
        draw_layout()
        udpate_time()
        update_sensor_data()
        display.text(f'LED EFFECT: {LED_EFFECT}', 0, 12*1, 1)
        display.show()
        await asyncio.sleep_ms(1000)

LED_EFFECT = 0


async def update_led_strip():
    # switch between differen lep strpi effects
    while True:
        if LED_EFFECT == 0:
            await led_cleanup_effect(np)
        elif LED_EFFECT == 1:
            await led_effect_1(np)
        elif LED_EFFECT == 2:
            await rainbowCycle(np)
        elif LED_EFFECT == 3:
            await week_day_routine_effect(np, ds3231)


async def poll_button():
    while True:
        if D33.value() == 0:
            global LED_EFFECT
            LED_EFFECT += 1
            if LED_EFFECT > 3:  # max number of led strip effect
                LED_EFFECT = 0
            await asyncio.sleep_ms(500)
        await asyncio.sleep_ms(100)


loop = asyncio.new_event_loop()
loop.create_task(update_display())
loop.create_task(update_led_strip())
loop.create_task(poll_button())
loop.create_task(udpate_humidity())
loop.run_forever()
