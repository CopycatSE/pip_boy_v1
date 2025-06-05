# Fallout Radio: Bunker-FM

## Overview

This script retrieves the latest news headlines from a Russian news RSS feed, uses Google Gemini to generate a fictional daily broadcast-style message (in Russian), converts the message into audio using ElevenLabs, and sends both the text and audio to a specified Telegram chat.

## Features

- Fetches the latest 5 news headlines from Delfi.lv RSS feed
- Generates a fictional, Russian-language daily report using Google Gemini
- Converts the text to speech using ElevenLabs
- Sends both text and audio to a Telegram bot chat
- Can be scheduled to run automatically

## Requirements

- Python 3.10 or higher
- Required Python packages:
  - requests
  - schedule
  - python-dotenv

You can install the required packages using:

    pip install -r requirements.txt

## Environment Configuration

Create a `.env` file in the root directory of the project and include the following variables:

    GEMINI_API_KEY=your_google_gemini_api_key
    ELEVENLABS_API_KEY=your_elevenlabs_api_key (optional)
    VOICE_ID=your_elevenlabs_voice_id (optional, default is '2EiwWnXFnvU5JabPnv8n')
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token (optional)
    TELEGRAM_CHAT_ID=your_telegram_chat_id (optional)

You can copy `backend/.env.example` and fill in the values. If Telegram or ElevenLabs credentials are omitted, the script will skip sending messages and audio.

## How to Run

To run the script once manually:

    python bunker_radio.py

To schedule automatic daily runs, you can use Python’s schedule module or a system cron job.

Example using schedule module:

    import schedule
    import time
    import bunker_radio as br

    schedule.every().day.at("09:00").do(br.job)

    while True:
        schedule.run_pending()
        time.sleep(60)

Example using cron (Linux/macOS):

    0 9 * * * /usr/bin/python3 /path/to/bunker_radio.py

## Customizable Settings

- `RSS_FEED_URL` – Change this to use a different RSS feed source.
- `BASE_PROMPT_TEXT` – Customize the prompt that is sent to Gemini to control the style and content of the generated message.
- `VOICE_ID` – Change to use a different ElevenLabs voice.
- Audio settings such as speech speed, stability, and similarity can be adjusted in the `generate_audio_from_text` function.

## Troubleshooting

- Gemini response errors: Check if the API key is valid and your quota is available.
- Telegram errors: Ensure the bot is added to the chat and has permission to send messages.
- Empty or silent audio: Verify that the selected ElevenLabs voice supports the Russian language.

## Project Structure

The project consists of the following modules:

- **`main.py`**: The entry point of the application. It orchestrates the workflow by fetching news, generating a broadcast message, converting it to audio, and sending it to Telegram.
- **`telegram_client.py`**: Handles sending text and audio messages to a Telegram chat using the Telegram Bot API.
- **`el_labs_client.py`**: Integrates with ElevenLabs API to convert text into audio with customizable voice settings.
- **`gemini_client.py`**: Communicates with Google Gemini API to generate creative, Russian-language broadcast-style messages.
- **`news_parser.py`**: Fetches the latest news headlines from an RSS feed and formats them for use in the broadcast.
- **`prompts.py`**: Contains the base prompt text for generating the broadcast message in the style of a Fallout universe DJ.
- **`config.py`**: Loads environment variables and defines constants like the RSS feed URL.

Each module is designed to handle a specific aspect of the workflow, making the project modular and easy to maintain.

## License

This project is provided without any warranty or guarantees. Use it at your own discretion.
