"""Decorative pauses; shared selection for web rendering and offline assets.

Keep artwork outside passage cards. Source JPGs remain unchanged; presentation
belongs to .reading-plate in css/style.css. Section IDs are language-independent.
"""

BEFORE = {
    "38": "eye.jpg",
}
AFTER = {
    "6": "hand.jpg",
    "8a": "handseyeman.jpg",
    "10": "eyes.jpg",
    "12": "chains.jpg",
    "14": "hyptno.jpg",
    "17": "personflowers.jpg",
    "23": "hug.jpg",
    "25": "ank.jpg",
    "27": "eyeshandssun.jpg",
    "30": "path.jpg",
    "35": "hands-and-eyes.jpg",
    "37": "hang.jpg",
}
ASSETS = tuple(f"pics/{name}" for name in dict.fromkeys([*BEFORE.values(), *AFTER.values()]))

# Reserve the actual aspect ratio before loading, including the tall portrait.
DIMENSIONS = {
    "ank.jpg": (896, 1344),
}


def render(number, position):
    name = {"before": BEFORE, "after": AFTER}[position].get(number)
    if not name:
        return ""
    width, height = DIMENSIONS.get(name, (1024, 1024))
    return (
        f'<figure class="reading-plate" data-reading-art="{number}" aria-hidden="true">'
        f'<img src="pics/{name}" alt="" width="{width}" height="{height}" '
        'loading="lazy" decoding="async" draggable="false"></figure>'
    )
