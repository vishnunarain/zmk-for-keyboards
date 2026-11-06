# Shared Corne layout and layer cycling

## One layout for both computers

This restores the seven-layer keymap from commit
`170d2ec405b4d7b8af7cf011a2f4b8be52eba5c7`, before the Mac/Windows
duplication, with the changes described below. There are no OS modes.

| ZMK modifier | macOS | Windows |
| --- | --- | --- |
| GUI | Command | Windows key |
| ALT | Option | Alt |
| CTRL | Control | Ctrl |
| SHIFT | Shift | Shift |

Modifiers are interpreted by the host; shortcuts are not translated.
For example, copy is Command+C on Mac and Ctrl+C on Windows.
The original clipboard combos and the NAV clipboard row still send
Command/GUI shortcuts, so those conveniences are Mac-oriented.
On Windows use the Ctrl home-row modifier with the letter on BASE.
No system-wide Ctrl/GUI remapping is required.

## Tap to change layers

The **far-right home-row key**, immediately right of the quote key,
is **NEXT LAYER** on every layer (physical position 23).
Each tap selects and latches the next layer:

**BASE -> NAV -> NUM -> MEDIA -> SYM -> FUN -> MOUSE -> BASE**

You do not need to keep a key held. On every utility layer, the
**far-right bottom-row key** (position 35, Escape on BASE) returns directly
to BASE. This gives a quick exit without cycling through the whole list.

The selected layer stays until another layer action changes it or the
keyboard restarts. It is not saved across a power cycle; startup is BASE.
The built-in layer display and ZMK Studio show the current layer name.

## QWERTY typing and original shortcuts

BASE has all QWERTY letters in their original positions.
It retains the original home-row modifiers: tap for a letter,
hold for the modifier below.

| Hold | Modifier |
| --- | --- |
| A / quote | Left / right GUI |
| S / L | Left / right Alt |
| D / K | Left / right Ctrl |
| F / J | Left / right Shift |
| Outer home-row Escape | Left Ctrl |

This is the original Miryoku-style typing layer, not an unmodified
desktop keyboard layout. The six original thumb layer-taps remain
available from BASE:

| Thumb, left to right | Tap | Hold |
| --- | --- | --- |
| Left outer | Escape | MEDIA |
| Left middle | Space | NAV |
| Left inner | Tab | MOUSE |
| Right inner | Enter | SYM |
| Right middle | Backspace | NUM |
| Right outer | Delete | FUN |

The tap-to-cycle route is an alternative to holding a thumb.
After latching a utility layer, use NEXT or BASE to change layers;
the original utility layers keep their specialized keys and blanks.

## Changes from the original layout

- Replace the BASE Hyper key with NEXT, and put NEXT at that same position
  on all seven layers. Hyper moves to the T position on MEDIA.
- Add the BASE return key on all six utility layers.
- Restrict the original 14 letter combos to BASE so they do not intercept
  numbers, symbols or navigation keys when a utility layer is latched.
  Their bindings, timing and physical key positions are unchanged.
- Add **Bootloader Reset** at the top-left and top-right corners of MEDIA.
  Each resets the half containing that key, for firmware installation.
- Move Bluetooth clear from the MEDIA bottom-right corner to its
  bottom-left corner, making room for the BASE return key.
- Keep QWERTY, home-row timing, six thumb layer-taps, utility content,
  Bluetooth, RGB, mouse and display configuration otherwise unchanged.

## Firmware installation without a reset button

Before replacing the currently installed firmware, retain a way to enter
the bootloader on **both** halves. In the currently running ZMK Studio
layout, assign Bootloader Reset to an available key on each side and save.
Do not restore stock settings until the replacement firmware is installed,
or you may lose your temporary bootloader assignments.

1. Download the `firmware` ZIP from a successful **Build ZMK firmware** run
   on this branch. Extract it.
2. Choose one matching pair:
   - OLED: left and right filenames without `nice_view`.
   - Nice!View: left and right filenames containing `nice_view`.
   The matrix targets `nice_nano//zmk`; verify it matches your controller.
3. With USB connected to the right half and both halves powered and linked,
   trigger the right-hand Bootloader Reset key first. Copy the matching
   right `.uf2` to the bootloader drive. Leave CURRENT.UF2 and the other
   files on that drive alone. It restarts after copying.
4. Connect USB to the left half, trigger its Bootloader Reset key and copy
   the matching left `.uf2`. Use the same successful build for both halves.
   The `settings_reset` file is not part of a normal installation.
5. Reconnect the left half in ZMK Studio. If saved remaps override the
   compiled keymap, record anything you need and use **Restore Stock Settings**,
   saving as prompted. This discards the old saved layout and loads the new one.
6. Test all seven NEXT transitions, the utility BASE return, QWERTY, home-row
   modifiers, Bluetooth and both computers.

Right-first installation preserves the old central keymap while using its
temporary right-side bootloader binding. Once the new layout is active,
MEDIA has built-in bootloader keys at both top corners for future updates.
If a half does not reconnect between updates, use its physical reset access
as documented by the builder; firmware alone cannot recover an unreachable half.

## Visual reference and validation

The generated `corne_keymap.svg` shows the new layout after Draw Keymap
succeeds. The two old HTML viewers are static references to the original
layout and do not show NEXT/BASE/bootloader changes. Use the generated SVG
or ZMK Studio for the current bindings.

Run `python3 tests/check_keymap.py` for checks covering seven 42-key layers,
the complete cycle, direct return, QWERTY/modifiers, combo scoping, and
bootloader controls. GitHub Actions runs these checks before compiling
the full firmware matrix. Physical behavior still needs keyboard testing.
