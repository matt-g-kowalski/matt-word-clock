import argparse
import time
from clock_display_hal import ClockDisplayHAL
from datetime import datetime
from word_clock import WordClock


# Color definitions


def main(pin, max_brightness, gif_path):
    clock_display_hal = ClockDisplayHAL(pin, max_brightness)
    word_clock = WordClock(clock_display_hal, gif_path)

    try:
        while True:
            clock_display_hal.pixels.brightness = get_brightness(max_brightness)
            word_clock.display_time()
            time.sleep(10)
    except KeyboardInterrupt:
        clock_display_hal.clear_pixels()



def get_brightness(max_brightness):
    hour = datetime.now().hour

    if 7 <= hour < 19:
        return max_brightness   # Day
    elif 19 <= hour < 22:
        return max_brightness / 2   # Evening
    else:
        return max_brightness / 8   # Night

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Word Clock.")
    parser.add_argument("--pin", type=str, required=True, help="The PIN number for the clock display.")
    parser.add_argument("--max_brightness",
                        type=float,
                        required=False, help="The max day brightness of the clock display.",
                        default=0.8)
    parser.add_argument("--gif", type=str, required=False, help="The path to the GIF image.")
    args = parser.parse_args()
    main(args.pin, args.max_brightness, args.gif)
