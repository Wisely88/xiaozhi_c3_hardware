# Build and flash Wisely C3 AI V2

This project does not keep a second, stale copy of the entire XiaoZhi firmware. Instead it pins a known upstream release and applies the local board overlay at build time.

## 1. Prerequisites

- Git
- Python 3
- ESP-IDF **v6.0.2** activated in your shell
- USB serial/JTAG access to the ESP32-C3 board

The pinned XiaoZhi baseline and IDF version are recorded in `/UPSTREAM_VERSION`.

## 2. Verify the repository

```bash
python3 tools/verify_project.py
```

This checks board identity, required files, duplicate GPIO assignments and verifies that the new port contains no irreversible eFuse write.

## 3. Prepare the upstream worktree

```bash
python3 tools/prepare_firmware.py --clean
```

The script clones the pinned XiaoZhi release into `.work/xiaozhi-esp32`, verifies its exact commit, copies `firmware/boards/wisely/c3-ai-v2`, and registers the board in upstream Kconfig/CMake.

## 4. Build

After activating ESP-IDF v6.0.2:

```bash
cd .work/xiaozhi-esp32
python scripts/build.py wisely/c3-ai-v2 \
  --name wisely-c3-ai-v2 \
  --language zh-CN \
  --wake-word nihaoxiaozhi \
  --zip
```

Or from the repository root:

```bash
make build
```

Expected outputs include:

- `.work/xiaozhi-esp32/build/merged-binary.bin`
- `.work/xiaozhi-esp32/releases/v2.4.2_wisely-c3-ai-v2.zip`

## 5. Flash

Find the serial port, then:

```bash
make flash PORT=/dev/tty.usbmodemXXXX
make monitor PORT=/dev/tty.usbmodemXXXX
```

On Linux the port is commonly `/dev/ttyACM0` or `/dev/ttyUSB0`.

## 6. First-boot acceptance test

A successful first boot should pass these checks in order:

1. ESP32-C3 boots without reset loops.
2. ES8311 probe at I2C address `0x18` succeeds.
3. Wi-Fi provisioning can be entered with BOOT during startup.
4. Microphone audio reaches the server.
5. Speaker output is clean and PA enable works.
6. BOOT press/hold starts and stops listening.
7. AUX button toggles chat state.
8. GPIO20 status LED follows application state.
9. `nihaoxiaozhi` wake word works when enabled.
10. Device reports board identity `wisely-c3-ai-v2` and does not receive a `kevin-c3` OTA image.

Do not enable unattended OTA for a production batch until item 10 is verified on a real device.

## 7. Updating upstream later

Do not change `UPSTREAM_VERSION` blindly. For each new upstream release:

1. Review XiaoZhi release notes.
2. Update `ref`, `commit`, and `idf` together.
3. Run `make refresh`.
4. If `prepare_firmware.py` reports a missing anchor, upstream changed its board build system; update the overlay integration deliberately.
5. Run CI and a real-device audio/OTA smoke test before merging.
