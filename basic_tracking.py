import os
import threading
import config as c
import db_queries as db

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.ImageHelpers import PILHelper
from StreamDeck.DeviceManager import DeviceManager


def get_key_style(deck, key, key_state, page):
    current_state = c.PAGE_KEY_CONFIGS[page]
    if key_state == True:
        return {
            "name": 0,
            "icon": '/Users/treads/CodingProjects/BabyTeeth/assets/press.png',
            "font": '/Users/treads/CodingProjects/BabyTeeth/assets/opensans.ttf',
            "label": 'Logged'
        }
    else:
        return current_state[key]


def render_key_image(deck, icon_filename, font_filename, label_text):
    icon = Image.open(icon_filename)
    image = PILHelper.create_scaled_key_image(deck, icon, margins=[0, 0, 20, 0])
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_filename, 10)
    draw.text((image.width / 2, image.height - 5), text=label_text, font=font, anchor="ms", fill="white")
    return PILHelper.to_native_key_format(deck, image)


def update_key_image(deck, key, key_state, page):
    # Determine what icon and label to use on the generated key.
    key_style = get_key_style(deck, key, key_state, page)
    # Generate the custom key with the requested image and label.
    image = render_key_image(deck, key_style["icon"], key_style["font"], key_style["label"])
    # Use a scoped-with on the deck to ensure we're the only thread using it
    # right now.
    with deck:
        # Update requested key with the generated image.
        deck.set_key_image(key, image)


def page_render(deck, screen_state):
    for key in range(deck.key_count()):
        update_key_image(deck, key, False, screen_state.page)

def update_page_state(screen_state, key):
    if screen_state.page == c.PAGE_INITIAL:
        update_initial(key, screen_state)
    elif screen_state.page == c.PAGE_HOW:
        update_how(key, screen_state)
    elif screen_state.page == c.PAGE_HOW_MUCH:
        update_how_much(key, screen_state)


def update_initial(key, screen_state):
    screen_state.page = c.PAGE_INITIAL
    screen_state.amount = 0
    screen_state.point_press = False
    if key in (2, 3, 4, 5):
        screen_state.page = c.PAGE_HOW_MUCH
        print(key)
    if key == 0:
        screen_state.page = c.PAGE_HOW
    if key == 1:
        db.write_row(screen_state.page, sleep_type="Sleep",wake_type=None)
    if key ==6 :
        db.write_row(screen_state.page, diaper_type="Pee")
    if key == 7:
        db.write_row(screen_state.page, diaper_type="Poo")
    if key == 9:
        db.write_row(screen_state.page, diaper_type="Empty")



def update_how(key, screen_state, **kwargs ):
    if key == 0:
        db.write_row(screen_state.page, wake_type="Dogs Barking", sleep_type="Sleep")
    if key == 1:
        db.write_row(screen_state.page, wake_type="Kate", sleep_type="Sleep")
    if key == 2:
        db.write_row(screen_state.page, wake_type="Craig", sleep_type="Sleep")
    if key == 3:
        db.write_row(screen_state.page, wake_type="Hangry", sleep_type="Sleep")
    if key == 14:
        update_initial(key, screen_state)


def update_how_much(key, screen_state):
    if key == 10:
        screen_state.point_press = True
    if screen_state.point_press == False and key not in (10, 14):
        screen_state.amount = screen_state.amount + (key + 1)
        #print(screen_state.amount)
    if screen_state.point_press and key not in (10, 14):
        screen_state.amount = screen_state.amount + ((key + 1) / 10)
        #print(screen_state.amount)
    if key == 14:
        feed_type = "find key later"
        side = "same with feed_type"
        db.write_row(screen_state.page, feed_type=feed_type, side=side, screen_state_amount=screen_state.amount)
        update_initial(key, screen_state)
        max(1, 2, 3, 4, 5)

def key_change_callback(deck, key, key_state, screen_state):
    # Update the key image based on the new key state.
    update_key_image(deck, key, key_state, screen_state.page)
    # Check if the key is changing to the pressed state.
    if key_state:
        update_page_state(screen_state, key)
    page_render(deck, screen_state)


class ScreenState:
    def __init__(self, starting_page):
        self.page = starting_page
        self.amount = 0
        self.point_press = False


def testing():
    streamdecks = DeviceManager().enumerate()
    screen_state = ScreenState(c.PAGE_INITIAL)
    initial_value = ScreenState(0)
    for index, deck in enumerate(streamdecks):
        deck.open()
        deck.reset()
        deck.set_brightness(90)
        page_render(deck, screen_state)
        deck.set_key_callback(lambda deck, key, key_state: key_change_callback(deck, key, key_state, screen_state))
    for t in threading.enumerate():
        try:
            t.join()
        except RuntimeError:
            pass


testing()
