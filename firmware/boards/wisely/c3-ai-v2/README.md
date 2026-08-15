# Wisely C3 AI V2 board port

This directory is an overlay for the upstream `78/xiaozhi-esp32` firmware. It gives the legacy `C3_AI_V2` hardware a unique OTA/build identity instead of pretending to be an upstream `Kevin C3` board.

## Identity

- Manufacturer: `wisely`
- Board type: `wisely-c3-ai-v2`
- Target: `esp32c3`
- Upstream baseline: see `/UPSTREAM_VERSION`

## Pin map

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

The mapping is intentionally inherited from the legacy project so existing boards can be migrated without rewiring.

## Important hardware gate

GPIO11/12/13 have package/flash-related restrictions on ESP32-C3 designs. Do **not** use this overlay as proof that a newly manufactured PCB is electrically valid. Before a new production run, verify the exact ESP32-C3 part number, flash topology and schematic against the current Espressif datasheet. See `/hardware/README.md`.

## Behavior

- BOOT click during startup: enter Wi-Fi configuration.
- BOOT press/hold: push-to-talk.
- AUX click: toggle chat state.
- GPIO20: single status LED.
- ES8311 is probed at boot; a missing codec fails loudly instead of continuing with broken audio.
- No eFuse is written by this board port.
