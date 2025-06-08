import os
from dotenv import load_dotenv

load_dotenv

user_airdrop = 1

SUCCESS_MESSAGE = os.environ['SUCCESS_MESSAGE']

ERROR_MESSAGE = f"""
👏 Follow <b><a href="https://x.com/auroraliteaal">us on Twitter</a></b>

👏 Join <b><a href="https://t.me/auroraliteaalchannel">us on Telegram Channel</a></b>

👏 Join <b><a href="https://t.me/auroraliteaalgroup">us on Telegram Group</a></b>

😒 Connect with us to continue
"""

TWITTER_MESSAGE = f"""
👏 Follow <b><a href="https://x.com/auroraliteaal">us on Twitter</a></b>

😒 Use `/start` to reset it

🗒️ What is your Twitter username:!!? e.g @auroralite
"""

WALLET_MESSAGE = f"""
🗒️ What is your BEP-20(BSC) wallet address!!?

<b><i> Please submit your Trustwallet or SafePal address. Address must be from a Decentralized  platform</i></b>
"""

REFERRAL_LINK_MESSAGE = f"""
👇 Forward a referrer's link. 

😒 If you've none please copy admin referral link from above
"""

WELCOME_MESSAGE = f"""
👋 Hello, Old sport! 

🌞 1 AAL = $100
⛅ Get <b>1 AAL</b> for joining and completing task
🌬️ Get <b>0.5 AAL</b> per referral 

📝 Airdrop will end soon...

🔥 Complete the task and be deemed eligible

🗒️ <b>TASK:</b>

👏 Follow <b><a href="https://x.com/auroraliteaal">us on Twitter</a></b>

👏 Join <b><a href="https://t.me/auroraliteaalchannel/">us on Telegram Channel</a></b>

👏 Join <b><a href="https://t.me/auroraliteaalgroup/">us on Telegram Group</a></b>

🧏 Use only positive words to chat in the group otherwise you will miss the big opportunity

<b>NOTE: All tasks are mandatory</b>

<b>You can use Admin referral Link: https://t.me/auroralite_bot?start={6243130914} </b>
"""

# Define the regular expression to match BSC addresses
# The above code is defining a regular expression pattern using the `re` module in Python. The pattern
# is used to match a string that represents a Binance Smart Chain (BSC) address.
BSC_ADDRESS_REGEX = r'^0x([A-Fa-f0-9]{40})$'