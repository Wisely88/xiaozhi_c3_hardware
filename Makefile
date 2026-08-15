PYTHON ?= python3
UPSTREAM_DIR ?= .work/xiaozhi-esp32
BOARD ?= wisely/c3-ai-v2
BOARD_NAME ?= wisely-c3-ai-v2
LANGUAGE ?= zh-CN
WAKE_WORD ?= nihaoxiaozhi
PORT ?=

.PHONY: verify prepare refresh build flash monitor clean

verify:
	$(PYTHON) tools/verify_project.py

prepare: verify
	$(PYTHON) tools/prepare_firmware.py --workdir $(UPSTREAM_DIR)

refresh: verify
	$(PYTHON) tools/prepare_firmware.py --workdir $(UPSTREAM_DIR) --clean

build: prepare
	cd $(UPSTREAM_DIR) && $(PYTHON) scripts/build.py $(BOARD) --name $(BOARD_NAME) --language $(LANGUAGE) --wake-word $(WAKE_WORD) --zip

flash: build
	@test -n "$(PORT)" || (echo "Set PORT, e.g. make flash PORT=/dev/tty.usbmodemXXXX" && exit 2)
	cd $(UPSTREAM_DIR) && idf.py -p "$(PORT)" flash

monitor:
	@test -n "$(PORT)" || (echo "Set PORT, e.g. make monitor PORT=/dev/tty.usbmodemXXXX" && exit 2)
	cd $(UPSTREAM_DIR) && idf.py -p "$(PORT)" monitor

clean:
	rm -rf $(UPSTREAM_DIR)
