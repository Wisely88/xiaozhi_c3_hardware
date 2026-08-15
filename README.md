# Wisely C3 AI V2 — XiaoZhi ESP32-C3 voice terminal

A maintainable modernization of the legacy `C3_AI_V2` XiaoZhi hardware project.

The goal is simple: **keep the custom ESP32-C3 + ES8311 hardware, stop carrying a frozen copy of XiaoZhi firmware, and make every firmware build reproducible.**

## Status

- Hardware baseline: existing `C3_AI_V2` PCB/schematic in this repository
- Board identity: `wisely-c3-ai-v2`
- MCU target: ESP32-C3
- Audio codec: ES8311
- Firmware upstream: `78/xiaozhi-esp32`
- Pinned stable baseline: `v2.4.2`
- Pinned upstream commit: `e8d8a4010788afd60f0c8aa3b2e3d0a7bb8f02e5`
- ESP-IDF: `v6.0.2`

See `UPSTREAM_VERSION` for the machine-readable baseline.

## Why this repository changed

The old `Firmware/` directory is a December 2024-era XiaoZhi snapshot. It works as historical reference, but maintaining a full fork caused the project to miss years of upstream changes in audio, state management, MCP, OTA, board packaging and build tooling.

The new model is:

```text
this repository
├── custom board overlay ───────┐
├── hardware sources            │
├── validation/docs             │
└── prepare_firmware.py         │
                               ▼
                     pinned 78/xiaozhi-esp32
                               │
                               ▼
                     reproducible firmware
```

The complete upstream firmware is generated under `.work/` and is never committed here.

## Quick start

### 1. Verify the project

```bash
python3 tools/verify_project.py
```

### 2. Install/activate ESP-IDF v6.0.2

Use Espressif's normal ESP-IDF installation flow, then make sure `idf.py --version` works in the current shell.

### 3. Prepare the pinned XiaoZhi source

```bash
python3 tools/prepare_firmware.py --clean
```

### 4. Build

```bash
make build
```

Equivalent upstream command:

```bash
cd .work/xiaozhi-esp32
python scripts/build.py wisely/c3-ai-v2 \
  --name wisely-c3-ai-v2 \
  --language zh-CN \
  --wake-word nihaoxiaozhi \
  --zip
```

### 5. Flash

```bash
make flash PORT=/dev/tty.usbmodemXXXX
make monitor PORT=/dev/tty.usbmodemXXXX
```

See `docs/BUILD_AND_FLASH.md` for the full procedure.

## Board pin map

| Function | GPIO |
|---|---:|
| ES8311 I2C SDA | 0 |
| ES8311 I2C SCL | 1 |
| AUX button | 6 |
| I2S DIN | 7 |
| I2S BCLK | 8 |
| BOOT button | 9 |
| I2S MCLK | 10 |
| I2S DOUT | 11 |
| I2S WS | 12 |
| PA enable | 13 |
| Status LED | 20 |

This mapping is preserved from the legacy project for compatibility with already-built C3_AI_V2 boards.

## Important hardware warning

A successful firmware build is **not** sufficient approval for a new PCB production run. The legacy pin map uses ESP32-C3 pins with package/flash restrictions, especially GPIO11/12/13. Before manufacturing more boards, confirm the exact ESP32-C3 part number and flash topology against the current Espressif datasheet and review the existing schematic/PCB.

Read `hardware/README.md` and complete `docs/VALIDATION.md` before calling a hardware revision production-ready.

## Repository layout

```text
.
├── Firmware/                     # legacy 2024 firmware snapshot (reference only)
├── PCB/                          # existing Altium PCB source
├── 原理图/                        # existing schematic PDF
├── firmware/
│   └── boards/wisely/c3-ai-v2/   # maintained board overlay
├── tools/
│   ├── prepare_firmware.py       # clone/pin/apply overlay
│   └── verify_project.py         # static project checks
├── docs/
│   ├── BUILD_AND_FLASH.md
│   ├── MIGRATION.md
│   └── VALIDATION.md
├── hardware/README.md            # manufacturing gate
├── UPSTREAM_VERSION              # reproducible source lock
└── .github/workflows/            # CI firmware build
```

## Updating to a future XiaoZhi release

Do not merge upstream wholesale into this repository. Instead:

1. Review the new XiaoZhi release.
2. Update `UPSTREAM_VERSION` (`ref`, exact `commit`, and `idf`).
3. Run `make refresh`.
4. Fix the small overlay registration only if upstream Kconfig/CMake changed.
5. Pass CI.
6. Run the real-device checklist in `docs/VALIDATION.md`.
7. Only then promote the new baseline.

This keeps upstream changes replaceable and the hardware-specific delta small.

## Attribution and licensing

See `NOTICE.md`. The firmware follows its upstream open-source lineage. The legacy PCB/schematic licensing is not clearly established in the imported snapshot, so commercial hardware redistribution/manufacture should not be assumed until those rights are confirmed.
