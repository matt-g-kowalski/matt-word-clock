import random
from datetime import datetime
from gif import display_gif
from clock_display_hal import ClockDisplayHAL

class WordClock:
    COLORS = [
        (255, 0, 0),  # Red
        (0, 255, 0),  # Green
        (0, 0, 255),  # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
        (255, 255, 255),  # White
        (165, 42, 42),  # Brown
        # Pastels
        #(255, 160, 180), # Pink
        #(255, 140, 140), # Red
        #(255, 190, 140), # Orange
        #(255, 235, 140), # Yellow
        #(140, 235, 170), # Green
        #(120, 220, 190), # Mint
        #(140, 190, 255), # Blue
        #(200, 160, 255), # Lavender
        #(185, 150, 220), # Purple
    ]

    def __init__(self, clock_display_hal,gif_path):
        self.last_hour = -1
        self.all_last_highlighted_words = ""
        self.clock_display_hal = clock_display_hal
        self.gif_path=gif_path

    def highlight_word(self, word, color=(255, 255, 255)):
        if word in ClockDisplayHAL.WORDS_TO_LEDS:
            self.clock_display_hal.display_word(word, color)

    def get_minutes_word(self, seconds_past):
        if seconds_past < 2 * 60 + 30:
            return "OCLOCK"
        elif seconds_past < 7 * 60 + 30:
            return "FIVE"
        elif seconds_past < 12 * 60 + 30:
            return "TEN"
        elif seconds_past < 17 * 60 + 30:
            return "FIFTEEN"
        elif seconds_past < 22 * 60 + 30:
            return "TWENTY"
        elif seconds_past < 27 * 60 + 30:
            return "TWENTYFIVE"
        elif seconds_past < 32 * 60 + 30:
            return "THIRTY"
        elif seconds_past < 37 * 60 + 30:
            return "TWENTYFIVE"
        elif seconds_past < 42 * 60 + 30:
            return "TWENTY"
        elif seconds_past < 47 * 60 + 30:
            return "FIFTEEN"
        elif seconds_past < 52 * 60 + 30:
            return "TEN"
        elif seconds_past < 57 * 60 + 30:
            return "FIVE"
        else:
            return "OCLOCK"

    def get_random_color(self):
        return random.choice(WordClock.COLORS)

    def get_transition_colour(self, minutes_into_increment):
        if minutes_into_increment < 1:
            return (0, 0, 255)
        if minutes_into_increment < 2:
            return (0, 128, 128)
        if minutes_into_increment < 3:
            return (0, 255, 0)
        if minutes_into_increment < 4:
            return (128, 128, 0)
        else:
            return (255, 0, 0)
            
    def display_time(self):
        now = datetime.now()
        hour = now.hour % 12 or 12  # Ensure hour is 1-12
        minute = now.minute
        second = now.second
        seconds_past = now.minute * 60 + now.second
        self.clock_display_hal.clear_pixels(show=False)
        if False and hour != self.last_hour and self.gif_path:
            if minute == 0:
                display_gif(self.gif_path,self.clock_display_hal)
                self.clock_display_hal.clear_pixels(show=False)
                self.last_hour = hour

        self.highlight_word("IT", self.get_random_color())
        self.highlight_word("IS", self.get_random_color())
        all_highlighted_words = "ITIS"

        seconds_into_increment = (seconds_past + 150) % 300
        #print("Seconds into increment = " + str(seconds_into_increment))
        minutes_into_increment = seconds_into_increment / 60
        #print("Minutes into increment = ", str(minutes_into_increment))

        transition_colour = self.get_transition_colour(minutes_into_increment)

        if (seconds_past > 57 * 60 + 30) or (seconds_past < 2 * 60 + 30):
            self.highlight_word("OCLOCK", transition_colour)
            all_highlighted_words = "OCLOCK"
            if (seconds_past > 57 * 60 + 30):
                hour = (hour + 1) % 12 or 12  # Adjust hour for "to" display
        elif seconds_past < 32 * 60 + 30:
            self.highlight_word("PAST", self.get_random_color())
            all_highlighted_words += "PAST"
            self.highlight_word("MINUTES", self.get_random_color())
            all_highlighted_words += "MINUTES"
        else:
            self.highlight_word("TO", self.get_random_color())
            all_highlighted_words += "TO"
            self.highlight_word("MINUTES", self.get_random_color())
            all_highlighted_words += "MINUTES"
            hour = (hour + 1) % 12 or 12  # Adjust hour for "to" display

        hour_word = f"HOUR_{hour}"
        self.highlight_word(self.get_minutes_word(seconds_past), transition_colour)
        all_highlighted_words += self.get_minutes_word(seconds_past) + str(transition_colour)
        self.highlight_word(hour_word, self.get_random_color())
        all_highlighted_words += hour_word

        if self.all_last_highlighted_words != all_highlighted_words:
            self.clock_display_hal.show()
            self.all_last_highlighted_words = all_highlighted_words
