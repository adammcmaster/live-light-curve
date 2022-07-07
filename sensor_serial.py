import datetime
import serial
import time


def read_flux():
    while True:
        with serial.Serial(
            "COM5", 9600, xonxoff=True, write_timeout=0.1, timeout=0.1
        ) as ser:
            flux = 0
            next_write = datetime.datetime.now()
            last_read = datetime.datetime.now()

            while True:
                if last_read < datetime.datetime.now() - datetime.timedelta(seconds=5):
                    print(datetime.datetime.now(), "Resetting connection...")
                    break
                if datetime.datetime.now() >= next_write:
                    print(datetime.datetime.now(), "Writing")
                    written = ser.write(b"  ")
                    next_write = datetime.datetime.now() + datetime.timedelta(
                        seconds=0.2
                    )
                    if written != 2:
                        print(datetime.datetime.now(), "Write failed")

                b = ser.read_until(size=5)

                b = list(b)
                if len(b) < 4:
                    if len(b) > 0:
                        print("failed", b)
                    yield flux
                    continue
                high, low = b[2:4]
                # Zero out the first three bits; not quite right as the reading might be negative, but good enough
                high = high & 31
                hundred = high >> 4
                denary = high & 15
                digit = low >> 4
                decimal = low & 15
                flux = hundred * 100 + denary * 10 + digit + decimal / 10.0
                status = b[1]
                last_read = datetime.datetime.now()
                print(datetime.datetime.now(), "Read succeeded, flux =", flux)
                yield flux
