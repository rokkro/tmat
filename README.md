To use: insert correct Twitter keys into the `config.ini` file (no quotation marks around keys necessary), then run `main.py`, which is a (WIP) menu interface. Make sure all files are in the same directory.

Requires Python 3.x, tested on 3.5/3.6.

1. twitter streaming [x]  - queue system found to be unnecessary, on occasion a few tweets will be skipped to catch up
2. Put in a DB (MongoDB) [x] - to be improved as i learn how databases work.
3. check duplicates [x] - Checks for exact duplicates and by similarity user can modify (default 55%).
4. sentiment analaysis [WIP] - Currently working on.
5. associate characteristics using neural networks to tweets + users
6. put resulting data somewhere
7. create nice UI (HTML?, Qt/QML?, Excel?) to present data or something like that
8. other stuff
