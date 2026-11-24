"""Sparse decorative pauses; shared selection for web rendering and offline assets.

Keep artwork outside passage cards. Source JPGs remain unchanged; presentation
belongs to .reading-plate in css/style.css. Section IDs are language-independent.
"""

BEFORE = {
    "38": "eye.jpg",
}
AFTER = {
    "8a": "handseyeman.jpg",
    "23": "hug.jpg",
    "30": "path.jpg",
}
ASSETS = tuple(f"pics/{name}" for name in dict.fromkeys([*BEFORE.values(), *AFTER.values()]))


def render(number, position):
    name = {"before": BEFORE, "after": AFTER}[position].get(number)
    if not name:
        return ""
    return (
        f'<figure class="reading-plate" data-reading-art="{number}" aria-hidden="true">'
        f'<img src="pics/{name}" alt="" width="1024" height="1024" '
        'loading="lazy" decoding="async" draggable="false"></figure>'
    )
