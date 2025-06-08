# Crypto Telegram Bot

Welcome to the Crypto Telegram Bot repository! This Python-based Telegram bot provides cryptocurrency-related functions, such as real-time referral, airdrops, and more.

## Features

- Real-time cryptocurrency referral.
- Airdrops and statistics.
- Customizable commands for users.

## Getting Started

Follow these steps to set up and run the Crypto Telegram Bot:

### Prerequisites

- Python 3.x installed.
- Telegram Bot Token (obtain from the [BotFather](https://core.telegram.org/bots#botfather)).

### Installation

1. Clone the repository:

    ```bash
        git clone https://github.com/yourusername/crypto-telegram-bot.git
        cd crypto-telegram-bot
    ```

2. Install dependencies:

    ```bash
        pip install -r requirements.txt
    ```

3. Create a `.env` file in the project root and add your Telegram Bot Token:

    ```env
        BOTTOKEN =Telegram Token from `BotFather`
        SUCCESS_MESSAGE = '👍 Welcome To the Crypto World
        RAILWAY_HOST = localhost
        RAILWAY_DB = railway
        RAILWAY_USER = root
        RAILWAY_PASSWORD = 
        RAILWAY_PORT = 3306
    ```

### Usage

1. Run the bot:

    ```bash
        python bot.py
    ```

2. Open Telegram and start a conversation with your bot.
3. Interact with the bot using the available commands.

## Commands

- `/start`: Start the bot.

## Contributing

If you'd like to contribute to the project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b master`).
3. Make changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin master`).
5. Create a pull request.

## License

This project is licensed under the [MIT License](./LICENSE). See the LICENSE file for details.
