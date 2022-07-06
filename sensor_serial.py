import serial
import time


def read_flux():
    with serial.Serial("COM5", 9600, xonxoff=True, write_timeout=1, timeout=1) as ser:
        # ser.write(b" EEE")
        # time.sleep(5)
        # ser.write(b" O")
        # time.sleep(5)
        # ser.write(b" K" + (1).to_bytes(1, byteorder="big"))
        flux = 0
        while True:
            ser.write(b"  ")
            # ser.read_until(expected=(2).to_bytes(1, "big"))
            b = ser.read_until(expected=(3).to_bytes(1, "big"))
            b = list(b)
            if len(b) != 4:
                print("Fail", b)
                continue
            high, low = b[1:3]
            hundred = high & 8
            denary = high & 7
            digit = low >> 3
            decimal = low & 7
            print(
                hundred,
                denary,
                digit,
                decimal,
                hundred * 100 + denary * 10 + denary + decimal / 10.0,
            )


read_flux()
