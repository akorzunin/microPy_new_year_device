import random
import math
import uasyncio as asyncio
import colorsys


def map_val(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


MAX_STEPS = 100
MAX_BRIGHTNESS = 0.1
UPDATE_MS = 10
TASK_SPAWN_DELAY_MS = 200


async def flake_tick(val, pos, color, saturation, np):
    np[pos] = colorsys.hsv_to_rgb(color, saturation, val)
    await asyncio.sleep_ms(UPDATE_MS)


def get_value(step):
    t = step / MAX_STEPS  # фаза 0..1
    return map_val(math.sqrt(t), 0, 1, 0, MAX_BRIGHTNESS)


async def one_led_task(pos, color, saturation, np):
    for step in range(MAX_STEPS):
        await flake_tick(get_value(step), pos, color, saturation, np)
    for step in reversed(range(MAX_STEPS)):
        await flake_tick(get_value(step), pos, color, saturation, np)


def get_rand_color():
    r = (
        (200, 1),
        (180, 1),
        (180, 0.3),
    )
    end = len(r) - 1
    return r[random.randint(0, end)]


async def flake_effect(np, loop):
    pos = random.randint(0, 29)
    if not any(np[pos]):
        print(f"task for led {pos} created")
        loop.create_task(one_led_task(pos, *get_rand_color(), np))
    else:
        print(f"led {pos} already taken")
    await asyncio.sleep_ms(TASK_SPAWN_DELAY_MS)
