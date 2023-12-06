import uasyncio as asyncio


async def led_cleanup_effect(np):
    for i in range(30):
        np[i] = (0, 0, 0)
        np.write()
        await asyncio.sleep_ms(50)


async def led_effect_1(np):
    for i in range(30):
        np[i] = (0x03, 0x17, 0x2F)
        np.write()
        await asyncio.sleep_ms(50)

    for i in range(30):
        np[i] = (0x06, 0x28, 0x44)
        np.write()
        await asyncio.sleep_ms(50)

    for i in range(30):
        np[i] = (0x30, 0x40, 0x40)
        np.write()
        await asyncio.sleep_ms(50)

    for i in range(30):
        np[i] = (0x09, 0x36, 0x57)
        np.write()
        await asyncio.sleep_ms(50)


def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)


async def rainbowCycle(np):  # sourcery skip: use-itertools-product
    for j in range(255):
        for i in range(30):
            np[i] = wheel((i+j) & 255)
            np.write()
            await asyncio.sleep_ms(1)


async def red_yellow_cycle(np):
    for i in range(30):
        np[i] = (255, 0, 0)
        np.write()
        await asyncio.sleep_ms(50)

    for i in range(30):
        np[i] = (255, 255, 0)
        np.write()
        await asyncio.sleep_ms(50)


async def green_yellow_cycle(np):
    for i in range(30):
        np[i] = (0, 255, 0)
        np.write()
        await asyncio.sleep_ms(50)

    for i in range(30):
        np[i] = (255, 255, 0)
        np.write()
        await asyncio.sleep_ms(50)


async def blue_green_cycle(np):
    for i in range(30):
        np[i] = (0, 0, 255)
        np.write()
        await asyncio.sleep_ms(50)

    for i in range(30):
        np[i] = (0, 255, 0)
        np.write()
        await asyncio.sleep_ms(50)


async def blue_yellow_cycle(np):
    for i in range(30):
        np[i] = (0, 0, 255)
        np.write()
        await asyncio.sleep_ms(50)

    for i in range(30):
        np[i] = (255, 255, 0)
        np.write()
        await asyncio.sleep_ms(50)


async def week_day_routine_effect(np, rtc_clock, minute=0):
    # change colors depending on the time of the day
    # morning: 7:00 - 9:00 - red - yellow
    # work_time: 9:00 - 13:00 - green - yellow
    # lunch: 13:00 - 14:00 - blue - gereen
    # work_time: 14:00 - 17:00 - green - yellow
    # evening: 17:00 - 18:00 - blue - yellow
    a = rtc_clock.get_time()
    hour = a[3]  # 3 - hours, 4 - minute, 5 - seconds
    if hour >= 7 and hour < 9:
        # turn on morning color
        await red_yellow_cycle(np)
    elif hour >= 9 and hour < 13 or hour >= 14 and hour < 17:
        # turn on work_time color
        await green_yellow_cycle(np)
    elif hour >= 13 and hour < 14:
        # turn on lunch color
        await blue_green_cycle(np)
    elif hour >= 17 and hour <= 18:  # change to 16 - 17
        # turn on evening color
        await blue_yellow_cycle(np)
    else:
        await led_cleanup_effect(np)

    await asyncio.sleep_ms(100)
