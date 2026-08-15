# C3_AI_V2 hardware status

The repository currently contains the original design artifacts in their legacy locations:

- `PCB/C3_AI_V2.PcbDoc` — Altium PCB source
- `原理图/C3_AI_V2.pdf` — schematic PDF

They are intentionally not moved in this modernization branch because the PCB file is binary and existing links/history should remain intact.

## Production gate: verify the ESP32-C3 flash/pin topology

The legacy firmware maps audio/control signals onto GPIO11, GPIO12 and GPIO13. Those pins have flash/VDD_SPI restrictions that depend on the exact ESP32-C3 chip/package and how flash is implemented. Therefore:

**Do not order a new production PCB batch solely because the firmware compiles.**

Before manufacturing, record and verify:

1. Exact ESP32-C3 ordering code used by `C3_AI_V2`.
2. Whether flash is in-package or external.
3. Flash power/routing and whether GPIO11 is legally usable as GPIO.
4. Whether GPIO12/GPIO13 are available or consumed by flash on that exact part.
5. GPIO9 boot-strapping resistor/button network.
6. GPIO20 UART0-RX trade-off when used as an LED output.

The modern board port intentionally performs **no eFuse writes**. If a future hardware revision truly needs VDD_SPI-to-GPIO eFuse configuration, that must be reviewed as a separate, explicitly documented manufacturing decision because eFuse programming is irreversible.

## Files still required for turnkey manufacturing

For a genuinely reproducible hardware release, add these generated artifacts after reviewing the Altium source:

- BOM with MPNs and approved alternates
- Gerber/ODB++ fabrication package
- NC drill files
- Pick-and-place/CPL file
- Assembly drawing
- Board dimensions and stack-up notes
- Test-point map and factory test procedure

Do not fabricate these files by guesswork; export them from the reviewed PCB source.

## Licensing note

The firmware lineage is open-source, but this repository snapshot does not clearly establish a separate hardware-design license for the PCB/schematic. Confirm the rights/attribution for the legacy hardware design before commercial redistribution or mass manufacture.
