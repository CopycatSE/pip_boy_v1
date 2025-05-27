import asyncio
from backend.prompts.news_prompts import build_prompt

# This block runs the full pipeline: fetches headlines, builds a prompt, gets AI response.
async def run_bunker_sequence(container: dict) -> tuple[str, str]:
    # Fetches the latest headlines from the RSS parser dependency
    headlines = container["news_parser"].get_headlines()
    # Builds a textual prompt based on the news headlines
    prompt = build_prompt(headlines)
    # Sends the prompt to the Gemini AI model and retrieves its response
    response = container["gemini"](prompt)
    # Yields control briefly to ensure proper event loop behavior (optional, good async practice)
    await asyncio.sleep(0)
    # Returns the original headlines and the AI's response as a tuple
    return headlines, response

# This block only runs if the file is executed directly (not imported as a module).
if __name__ == "__main__":
    import asyncio
    from backend.dependencies import register_dependencies

    container = register_dependencies()
    headlines, response = asyncio.run(run_bunker_sequence(container))


    print("\n GEMINI RESPONSE:")
    print(response)