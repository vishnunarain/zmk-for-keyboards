"""Check the shared Corne keymap and its persistent layer cycle."""
from pathlib import Path
import re
import unittest

SOURCE = (Path(__file__).resolve().parents[1] / "config/corne.keymap").read_text()
CLEAN = re.sub(r"//[^\n]*|/\*[\s\S]*?\*/", "", SOURCE)
LAYERS = re.findall(
    r'(\w+_layer)\s*\{\s*display-name\s*=\s*"([^"]+)";\s*bindings\s*=\s*<([\s\S]*?)>;',
    CLEAN,
)
BANKS = [[" ".join(b.split()) for b in re.findall(r"&\w+[^&]*", body)]
         for _, _, body in LAYERS]
NAMES = ["BASE", "NAV", "NUM", "MEDIA", "SYM", "FUN", "MOUSE"]

class KeymapChecks(unittest.TestCase):
    def test_shared_layers(self):
        self.assertEqual([name for _, name, _ in LAYERS], NAMES)
        self.assertNotIn("WIN_", CLEAN)
        self.assertNotIn("MAC ", CLEAN)
        for i, row in enumerate(BANKS):
            self.assertEqual(len(row), 42, f"layer {i}")

    def test_cycle_and_escape(self):
        edges = {}
        for i, row in enumerate(BANKS):
            self.assertEqual(row[23], "&to " + NAMES[(i + 1) % 7])
            edges[i] = NAMES.index(row[23].split()[1])
            if i:
                self.assertEqual(row[35], "&to BASE")
        current = 0
        visited = []
        for _ in range(7):
            visited.append(current)
            current = edges[current]
        self.assertEqual(visited, list(range(7)))
        self.assertEqual(current, 0)

    def test_qwerty_and_modifiers(self):
        base = BANKS[0]
        self.assertEqual(base[1:11], ["&kp " + k for k in "QWERTYUIOP"])
        self.assertEqual(base[13:23], [
            "&mt LGUI A", "&mt LALT S", "&mt LCTRL D", "&mt LSHFT F",
            "&kp G", "&kp H", "&mt RSHFT J", "&mt RCTRL K",
            "&mt RALT L", "&mt RGUI SQT"])
        self.assertEqual(base[25:35], ["&kp " + k for k in
            ["Z","X","C","V","B","N","M","COMMA","DOT","FSLH"]])
        self.assertEqual(base[12], "&mt LCTRL ESC")
        self.assertEqual(base[36:], ["&lt MEDIA ESC", "&lt NAV SPACE",
            "&lt MOUSE TAB", "&lt SYM RET", "&lt NUM BSPC", "&lt FUN DEL"])

    def test_combos_only_on_typing_layer(self):
        combos = re.findall(r"combo_(\w+)\s*\{([^}]+)\}", CLEAN)
        self.assertEqual(len(combos), 14)
        for _, body in combos:
            self.assertIn("layers = <BASE>;", body)
            positions = re.search(r"key-positions = <([^>]+)>", body)[1].split()
            self.assertTrue(all(int(p) not in [23, 35] for p in positions))
        for action, key in [("copy","C"), ("paste","V"), ("cut","X")]:
            body = dict(combos)[action]
            self.assertIn(f"bindings = <&kp LG({key})>;", body)

    def test_firmware_access_and_media(self):
        media = BANKS[3]
        self.assertEqual(media[0], "&bootloader")
        self.assertEqual(media[11], "&bootloader")
        self.assertEqual(media[5], "&hyper")
        self.assertEqual(media[24], "&bt BT_CLR")
        self.assertEqual(media[31:35],
            [f"&bt BT_SEL {i}" for i in range(4)])
        self.assertEqual(BANKS[6][39:], ["&mkp MCLK", "&mkp LCLK", "&mkp RCLK"])

if __name__ == "__main__":
    unittest.main()
