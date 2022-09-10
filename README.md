# Narrator

Narrator is a karma bot we use for our Slack workspace. Narrator is book/reading themed because we're all huge lit nerds.

I built Narrator using the Slack's [Bolt for Python](https://slack.dev/bolt-python/tutorial/getting-started). Narrator stores karma entries in a pyMongo database.

## Narrator functionality

| Command      | Description |
| ------------ | ----------- |
| `<item> ++`, `<item>++` | Adds karma to an item. You can use `@` notation for a user. If you want to add karma to a phrase, encapsulate the phrase in parentheses. For example, `(Everyone in this channel)++`.|
| `<item> --`, `<item>--` | Removes karma from an item. You can use `@` notation for a user. If you want to remove karma from a phrase, encapsulate the phrase in parentheses. For example, `(Entire python ecosystem)--`.|
| `!karma <item>` | Prints the karma for an item if it's found in the karma database. |
| `!best` | Prints a list of the top 5 karma entries. |
| `!worst` | Prints a list of the bottom 5 karam entries. |
| `!list` | This command returns a list of all karma entries to the console. It's mostly used for debugging and doesn't print anything to the Slack channel. |