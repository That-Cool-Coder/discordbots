# discordbots

Some discord bots I made

## Miscellanious information

All of the bots extend from the class `Bot`, defined in `abstract_bot.py`. It handles things like login and message recieve.

To make this program highly configurable, all of the bots can be run with command line arguments, or if they are not provided, you will be prompted for them.

## Autorunning

To ease in deployment of these bots, it is possible to create a config file called `autorun_conf.json` which determines which bots to run, what account they should log into, and additional parameters specific to that bot. A template has been provided in `autorun_conf_template.json`. IMPORTANT: Do not post your `autorun_conf.json` online as it contains the bot tokens for your bots!

## List of bots

#### BotBot

This is a basic chatbot, based of an old JavaScript project of mine. Because I'm too lazy to convert languages, it just runs a node file (`node_chatbot/chatbotRunner.mjs`). The chatbot is designed to provide entertainment - no practical purpose. There is nothing configurable through `autorun_conf.json`, although it can be configured at runtime through Discord messages (see `botbot.py` for information).

#### CounterBot

This is a chatbot designed for use in counting channels (where each message = previous message + 1). It's pretty self explanatory. Through `autorun_conf.json`, you can configure how likely it is to reply to a counting message (0 means that it will never reply, 1 means that it will always reply).

#### BruhBot

This is a chatbot designed for use in bruh-chain channels (where all messages are a variation on `bruh`), although it can also be useful in other channels as well. If it recieves a message based on `bruh`, it will generate a random `bruh` and send it back. Through `autorun_conf.json`, you can configure how likely it is to reply to a counting message (0 means that it will never reply, 1 means that it will always reply).

#### ImageScraperBot

This is a chatbot designed to liven up Discord channels with images. When it recieves a message, it searches google for a matching image and sends the result. It achieves this using Pyppeteer. Through `autorun_conf.json`, you can configure whether it requires a trigger to scrape an image and whether it will run in debug mode.

## Creating a new bot

To create a new bot in this repo, first create a file to contain the bot. Import `Bot` from`abstract_bot` and import `run_bot` from `common`. Then create a class in that file extending from `Bot`. At the bottom of the file, in a `if __name__ == '__main__'` clause, do `run_bot(YourNewBotClass, conf_fields)` (see inside `common.py` for comments explaining conf_fields). In `autorun.py`, add an entry in `BOT_FILES` so the autorunner knows where to find it. Optionally, you can create an entry in your `autorun_conf.json` to make it automatically run.