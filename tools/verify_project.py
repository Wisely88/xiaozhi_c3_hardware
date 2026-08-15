#!/usr/bin/env python3
"""Static sanity checks for the repository overlay and board identity."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / "firmware" / "boards" / "wisely" / "c3-ai-v2"

EXPECTED_FILES = [
    ROOT / "UPSTREAM_VERSION",
    BOARD / "config.h",
    BOARD / "config.json",
    BOARD / "wisely_c3_ai_v2_board.cc",
    ROOT / "tools" / "prepare_firmware.py",
    ROOT / "docs" / "BUILD_AND_FLASH.md",
    ROOT / "hardware" / "README.md",
]

RISK_NOTES = {
    9: "ESP32-C3 strapping pin; BOOT circuit must preserve valid reset levels.",
    11: "ESP32-C3 VDD_SPI/flash-related pin on some chip/package configurations.",
    12: "ESP32-C3 flash-interface-related pin on some chip/package configurations.",
    13: "ESP32-C3 flash-interface-related pin on some chip/package configurations.",
    20: "ESP32-C3 UART0 RX; using it as LED removes normal UART0 RX use.",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    missing = [str(path.relative_to(ROOT)) for path in EXPECTED_FILES if not path.exists()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    cfg = json.loads((BOARD / "config.json").read_text(encoding="utf-8"))
    if cfg.get("manufacturer") != "wisely":
        fail("config.json manufacturer must be 'wisely'")
    if cfg.get("type") != "wisely-c3-ai-v2":
        fail("config.json type must be 'wisely-c3-ai-v2'")
    if cfg.get("target") != "esp32c3":
        fail("config.json target must be 'esp32c3'")
    builds = cfg.get("builds") or []
    if len(builds) != 1 or builds[0].get("name") != "wisely-c3-ai-v2":
        fail("config.json must expose one stable build identity: wisely-c3-ai-v2")

    header = (BOARD / "config.h").read_text(encoding="utf-8")
    pins = {
        name: int(number)
        for name, number in re.findall(
            r"^#define\s+([A-Z0-9_]+)\s+GPIO_NUM_(\d+)\s*$",
            header,
            re.MULTILINE,
        )
    }
    required_pin_names = {
        "AUDIO_I2S_GPIO_MCLK", "AUDIO_I2S_GPIO_WS", "AUDIO_I2S_GPIO_BCLK",
        "AUDIO_I2S_GPIO_DIN", "AUDIO_I2S_GPIO_DOUT", "AUDIO_CODEC_PA_PIN",
        "AUDIO_CODEC_I2C_SDA_PIN", "AUDIO_CODEC_I2C_SCL_PIN",
        "BUILTIN_LED_GPIO", "BOOT_BUTTON_GPIO", "AUX_BUTTON_GPIO",
    }
    missing_pins = sorted(required_pin_names - pins.keys())
    if missing_pins:
        fail("missing pin definitions: " + ", ".join(missing_pins))

    by_gpio: dict[int, list[str]] = {}
    for name, gpio in pins.items():
        if name.endswith("_PIN") or name.startswith("AUDIO_I2S_GPIO_") or name == "BUILTIN_LED_GPIO":
            by_gpio.setdefault(gpio, []).append(name)
    duplicates = {gpio: names for gpio, names in by_gpio.items() if len(names) > 1}
    if duplicates:
        fail("duplicate GPIO assignments: " + repr(duplicates))

    source = (BOARD / "wisely_c3_ai_v2_board.cc").read_text(encoding="utf-8")
    if "esp_efuse_write" in source or "esp_efuse_write_field_bit" in source:
        fail("board source must not write irreversible eFuse state")

    print("Repository overlay checks: PASS")
    print("Board identity: wisely-c3-ai-v2 / esp32c3")
    print("Pin-map structural check: PASS")
    print("eFuse write check: PASS")
    print("\nHardware review warnings (not build failures):")
    for gpio in sorted(set(pins.values()) & RISK_NOTES.keys()):
        names = ", ".join(sorted(name for name, value in pins.items() if value == gpio))
        print(f"  GPIO{gpio:02d} ({names}): {RISK_NOTES[gpio]}")
    print("\nElectrical validation and a real-device smoke test are still required before production.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
