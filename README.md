# Simple provable fair Bitcoin Cash Telegram gambling bot
#### Please consider using this only for educational purposes!
#### It was a project I wrote on one weekend so there could be bugs.
## Dependencies
    -   bitcash
    -   telegram

## Explanation of provable fairness
When a player initiates a round the server generates the first part of the seed for the deterministic random number generator and sends a SHA256 hash of the seed to the player.
The player then can send a Bitcoin Cash transaction to the given address.
The previously generated server seed gets concatenated to the transaction ID of the Bitcoin Cash transaction. This integer value is used as the seed for the random number generator.
After that the server generates a random number between 0 and 1.
If the number is higher than 0.52 the game is considered as won and double of the amount sent to the wallet address is sent back.
If the number is 0.777 a fix amount of Bitcoin Cash gets sent to the wallet address. (Jackpot)

After the game the player retrieves the server seed in plain text and can verify that the game was fair.

## How to run the bot

Simply enter the Telegram bot token, public and private key of your hot wallet into the scripts and run tgbot.py, worker.py and pay.py

tgbot.py will communicate with the players, worker.py will execute the games and fill the queue of won games, pay.py will send the winnings to the players.
