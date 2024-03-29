# Running the bot

To run the bot:
1. Create a Python virtual environment:
   ```bash
   python3 -m venv .venv
   ```
1. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
1. Check to make sure the virtual environment is active:
   ```bash
   which python3
   # Output: /home/<username>/repos/narrator/.venv/bin/python3
   ```
1. Export your Slack bot token:
   ```bash
   export SLACK_BOT_TOKEN=xoxb-<your-bot-token>
   ```
1. Export your Slack app token:
   ```bash
   export SLACK_APP_TOKEN=<your-app-level-token>
   ```
1. Install the slack_bolt Python package to your virtual environment:
   ```bash
   pip install slack_bolt
   ```
1. Run the app:
   ```bash
   python3 path/to/app.py
   ```

There's more information on setting up a Bolt bolt [in the Slack docs](https://slack.dev/bolt-python/tutorial/getting-started).    
