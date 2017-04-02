To use: insert correct Twitter (tweet streaming) and/or Kairos (image analysis) API keys into the `config.py` file, then run `menu_main.py`, which is a menu interface.

Install mongoDB and run with `mongod --dbpath=/path/to/db`.

Requires Python 3.x, tested on 3.5/3.6.

1. Twitter tweet streaming [x]  - queue system found to be unnecessary, rarely tweets will be skipped to catch up.
2. Set up MongoDB system [x]
3. Check tweet duplicates [x] - Checks for exact duplicates and by similarity user can modify (default 55%) within same collection.
4. Sentiment analaysis [x] - Basic Vader SA implemented.
5. Associate characteristics using neural networks to tweets + users. [WIP!]
6. Present data in meaningful way
7. Historical tweet gathering (if possible)
