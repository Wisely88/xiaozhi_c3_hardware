# Migration from the 2024 firmware snapshot

## What changes

The repository originally embedded a December 2024 XiaoZhi firmware snapshot under `Firmware/`. That code remains as a historical reference, but it is no longer the recommended build source.

The maintained path is now:

1. Pin a stable upstream `78/xiaozhi-esp32` release.
2. Keep only the C3_AI_V2 board-specific implementation in this repository.
3. Generate a disposable `.work/xiaozhi-esp32` tree for each upstream migration.
4. Build under the unique identity `wisely-c3-ai-v2`.

## Hardware behavior preserved

| Item | Legacy | Modern port |
|---|---|---|
| ES8311 I2C | GPIO0 / GPIO1 | same |
| I2S MCLK | GPIO10 | same |
| I2S BCLK | GPIO8 | same |
| I2S WS | GPIO12 | same |
| I2S DIN | GPIO7 | same |
| I2S DOUT | GPIO11 | same |
| PA enable | GPIO13 | same |
| BOOT | GPIO9 | same |
| AUX | GPIO6 | same |
| LED | GPIO20 | same |

## Deliberate differences

- Board identity changes from the ambiguous `kevin-c3` lineage to `wisely-c3-ai-v2`.
- The current upstream device-state API is used instead of the 2024 chat-state implementation.
- The LED uses the current upstream `GpioLed` implementation.
- ES8311 is probed explicitly at boot.
- No `esp_efuse_write_*` call is allowed in this port.
- The complete upstream firmware is not vendored here, preventing another multi-year fork drift.

## Legacy directory policy

`Firmware/` is read-only historical material. New fixes should go into the board overlay or upstream XiaoZhi, not into the frozen snapshot.
