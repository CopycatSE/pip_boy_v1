import asyncio
from prompts.prompts import build_prompt

async def run_bunker_sequence(container: dict) -> tuple[str, str]:
    headlines = container["rss_parser"].get_headlines()
    prompt = build_prompt(headlines)
    response = container["gemini"](prompt)
    await asyncio.sleep(0)
    return headlines, response