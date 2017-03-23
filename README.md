To use: insert correct Twitter dev keys into the `config.ini` file (no quotation marks around keys necessary), then run `main.py`, which is a (WIP) menu interface. Make sure all files are in the same directory.

Install mongoDB and run with `mongod --dbpath=/path/to/db`.

Requires Python 3.x, tested on 3.5/3.6.

1. Twitter tweet streaming [x]  - queue system found to be unnecessary, on occasion tweets will be skipped to catch up.
2. Set up MongoDB system [x]
3. Check tweet duplicates [x] - Checks for exact duplicates and by similarity user can modify (default 55%) within same collection.
4. Sentiment analaysis [x] - Basic SA implemented. Want to improve setup process at some point.
5. Associate characteristics using neural networks to tweets + users. 
6. Put resulting data somewhere
7. Create nice UI (HTML/Qt/Excel/graphing util) to present data if desired.
