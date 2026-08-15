# Changelog

## Unreleased — modernization baseline

- Introduce unique board identity `wisely-c3-ai-v2`.
- Pin XiaoZhi upstream stable release `v2.4.2` at commit `e8d8a4010788afd60f0c8aa3b2e3d0a7bb8f02e5`.
- Pin CI/build environment to ESP-IDF `v6.0.2`.
- Port the legacy ES8311 + button + LED hardware mapping to the current XiaoZhi board APIs.
- Remove inherited eFuse programming from the custom board path.
- Add reproducible upstream preparation script.
- Add repository static checks and GitHub Actions firmware build.
- Add migration, build/flash, hardware-gate and validation documentation.
- Mark the 2024 `Firmware/` tree as legacy reference material.
