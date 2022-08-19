try:
    import gpiozero

    HAS_GPIO = True
except ImportError:
    HAS_GPIO = False


MAIN_LED_GPIO = 13
GREEN_LED_GPIO = 5
RED_LED_GPIO = 6


class DummyGPIO(object):
    def on(self):
        return

    def off(self):
        return


if HAS_GPIO:
    main_led = gpiozero.PWMLED(MAIN_LED_GPIO)
    green_led = gpiozero.LED(GREEN_LED_GPIO)
    red_led = gpiozero.LED(RED_LED_GPIO)
else:
    main_led = green_led = red_led = DummyGPIO()
