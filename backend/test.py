from dependencies import register_dependencies

container = register_dependencies()
parser = container["rss_parser"]
response = container["gemini"]("Give me post-apocalyptic news!")
print("📻 Gemini Response:\n", response)