# Legacy firmware snapshot

The files in this `Firmware/` directory are retained for historical comparison only. They represent an old XiaoZhi codebase and should not receive new feature development.

Use the root-level workflow instead:

```bash
python3 tools/verify_project.py
python3 tools/prepare_firmware.py --clean
make build
```

Board-specific code now lives in `firmware/boards/wisely/c3-ai-v2/` and is applied to the pinned current upstream release at build time.
