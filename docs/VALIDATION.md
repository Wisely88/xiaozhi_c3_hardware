# Validation plan

Use this checklist before calling a firmware or hardware revision releasable.

## Firmware CI

- [ ] `python3 tools/verify_project.py` passes.
- [ ] Pinned upstream commit matches `/UPSTREAM_VERSION`.
- [ ] ESP-IDF v6.0.2 build completes for `wisely/c3-ai-v2`.
- [ ] `merged-binary.bin` is produced.

## Bench test

- [ ] 3.3 V rail is stable at idle and during Wi-Fi TX.
- [ ] ES8311 responds at `0x18`.
- [ ] Microphone capture has no clipping or persistent DC offset.
- [ ] Speaker output is free of oscillation and excessive idle noise.
- [ ] PA enable/disable does not cause damaging pops.
- [ ] BOOT and AUX buttons behave correctly after repeated reset cycles.
- [ ] GPIO20 LED works without breaking the chosen debug/serial path.
- [ ] Wake word works at 0.5 m, 1 m and 3 m in a normal room.
- [ ] Five-minute continuous conversation test passes.
- [ ] Two-hour idle/periodic-use soak test has no reset or heap exhaustion.

## OTA safety

- [ ] Reported manufacturer is `wisely`.
- [ ] Reported type/name is `wisely-c3-ai-v2`.
- [ ] OTA service has a dedicated channel for this identity.
- [ ] A deliberately incompatible `kevin-c3` image is never selected for this device.
- [ ] Rollback or recovery flashing procedure is documented and tested.

## Hardware release gate

- [ ] Exact ESP32-C3 part number and package recorded.
- [ ] External/in-package flash topology recorded.
- [ ] GPIO11/12/13 usage checked against that exact part and flash topology.
- [ ] GPIO9 strap network checked for reliable normal boot and download mode.
- [ ] Antenna keep-out reviewed.
- [ ] USB/UART debug path reviewed.
- [ ] Schematic ERC reviewed.
- [ ] PCB DRC reviewed.
- [ ] BOM exported with manufacturer part numbers.
- [ ] Gerbers/drill files generated and independently viewed.
- [ ] Assembly drawing and pick-and-place exported if SMT assembly is planned.
