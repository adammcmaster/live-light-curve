try:
    import gpiozero

    HAS_GPIO = True
except ImportError:
    HAS_GPIO = False


MAIN_LED_GPIO = 13
GREEN_LED_GPIO = 5
RED_LED_GPIO = 6

ROTATOR_BUTTON_GPIO = 25
EXOPLANET_BUTTON_GPIO = 24
LENSING_BUTTON_GPIO = 23
SHUFFLE_BUTTON_GPIO = 18


class DummyGPIO(object):
    def on(self):
        return

    def off(self):
        return


if HAS_GPIO:
    main_led = gpiozero.PWMLED(MAIN_LED_GPIO)
    green_led = gpiozero.LED(GREEN_LED_GPIO)
    red_led = gpiozero.LED(RED_LED_GPIO)
    rotator_button = gpiozero.Button(ROTATOR_BUTTON_GPIO)
    exoplanet_button = gpiozero.Button(EXOPLANET_BUTTON_GPIO)
    lensing_button = gpiozero.Button(LENSING_BUTTON_GPIO)
    shuffle_button = gpiozero.Button(SHUFFLE_BUTTON_GPIO)
else:
    main_led = green_led = red_led = DummyGPIO()
    rotator_button = exoplanet_button = lensing_button = shuffle_button = DummyGPIO()
