import asyncio
from backend.prompts.prompts import build_prompt

async def run_bunker_sequence(container: dict) -> tuple[str, str]:
    headlines = container["rss_parser"].get_headlines()
    prompt = build_prompt(headlines)
    response = container["gemini"](prompt)
    await asyncio.sleep(0)
    return headlines, response


if __name__ == "__main__":
    import asyncio
    from backend.dependencies import register_dependencies

    container = register_dependencies()
    headlines, response = asyncio.run(run_bunker_sequence(container))


    print("\n🤖 GEMINI RESPONSE:")
    print(response)