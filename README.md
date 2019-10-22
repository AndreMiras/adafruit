# adafruit
Playing around with Adafruit Circuit Playground Express

## Install and usage
You first need to deploy the [CircuitPython firmware](https://circuitpython.org/board/circuitplayground_express/) to the board.

Then deploy the code to the board via:
```sh
make deploy
```
Then use buttons A and B to select a program to run.

## Troubleshooting
### Read-only file system
I sometimes got a read-only file system.
Simply formatting the device made it for me.
Make sure you're formatting the correct device and not your disk.
```
sudo fsck.msdos -aw /dev/sda1
```
