import re

FLAG_EMOJI = re.compile(r"🏴|🏳️|([🇦-🇿]{2})")  # 🏴|🏳️|([🇦-🇿]{2})|( ##|\n{2,}
PLACEHOLDER = '</br>' #║
HASHTAG = re.compile(r"\s*(\s*(#\w+))*\s*$")
TAG_EMPTY = re.compile(r"<(\w+)>\s*<\/\1>")
TAG_TRAILING = re.compile(r"\s+<\/(\w+)>\s*$")
