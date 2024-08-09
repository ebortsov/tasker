# Tasker

<a href="https://t.me/limbo_tasker_bot">Link to the bot</a>

**Tasker** — is a simple task manager created as Telegram bot.

The users simply create and finish the tasks. After that, the users view through the completed tasks and track their progress.

## Screenshots of the bot:

<img alt="Screenshot 1" src="https://github.com/user-attachments/assets/f74338f9-790a-4082-9a23-e675c3db3a2e" width="300px"/>
<img alt="Screenshot 1" src="https://github.com/user-attachments/assets/3b3b7a68-97e2-4ac4-a0bf-71c05e078e6a" width="300px"/>
<br/>
<img alt="Screenshot 1" src="https://github.com/user-attachments/assets/ab16a2f5-d4b4-42ab-9c91-94529d29e047" width="300px"/>
<img alt="Screenshot 1" src="https://github.com/user-attachments/assets/ba507a5f-da1f-4bc1-8af7-57c3c0449e77" width="300px"/>

## Deploy

To deploy the Tasker bot, follow these steps:

1) Clone the repository.
2) Create `.env` file in the root and fill it according to `.env.example`.
3) Create directories `databases` and `logs` in the root.
4) Launch the bot with command `docker compose up -d` (ensure the Docker is installed on you system).

## Technologies

This project is built using the following technologies:

1) [aiogram](https://aiogram.dev/) - The library for working with Telegram API
2) [SQLite](https://sqlite.org/) - A lightweight and self-contained SQL database engine.
3) [Ruff](https://docs.astral.sh/ruff/) - A fast Python linter and formatter.
4) [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) - Tools for containerizing and deploying the bot in an isolated environment.

## Other
The bot was developed using [vscode](https://code.visualstudio.com/) as a primary code editor. 

The `.vscode` folder was preserved in the repo. In the folder one can find the basic settings to run the code, and some setup for quick formatting and linting. (WARNING: `tasks.json` will work only on Windows, for Linux minor changes are required).