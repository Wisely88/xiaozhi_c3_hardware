#include "wifi_board.h"
#include "codecs/es8311_audio_codec.h"
#include "application.h"
#include "button.h"
#include "config.h"
#include "led/gpio_led.h"

#include <driver/i2c_master.h>
#include <esp_err.h>
#include <esp_log.h>

#define TAG "WiselyC3AiV2"

class WiselyC3AiV2Board : public WifiBoard {
private:
    i2c_master_bus_handle_t codec_i2c_bus_ = nullptr;
    Button boot_button_;
    Button aux_button_;

    void InitializeCodecI2c() {
        i2c_master_bus_config_t i2c_bus_cfg = {
            .i2c_port = I2C_NUM_0,
            .sda_io_num = AUDIO_CODEC_I2C_SDA_PIN,
            .scl_io_num = AUDIO_CODEC_I2C_SCL_PIN,
            .clk_source = I2C_CLK_SRC_DEFAULT,
            .glitch_ignore_cnt = 7,
            .intr_priority = 0,
            .trans_queue_depth = 0,
            .flags = {
                .enable_internal_pullup = 1,
            },
        };
        ESP_ERROR_CHECK(i2c_new_master_bus(&i2c_bus_cfg, &codec_i2c_bus_));

        const esp_err_t probe = i2c_master_probe(
            codec_i2c_bus_, AUDIO_CODEC_ES8311_ADDR, 1000);
        if (probe != ESP_OK) {
            ESP_LOGE(TAG,
                     "ES8311 probe failed at 0x%02x. Check 3V3, I2C SDA/SCL and codec address.",
                     AUDIO_CODEC_ES8311_ADDR);
            ESP_ERROR_CHECK(probe);
        }
    }

    void InitializeButtons() {
        // BOOT: click during startup enters Wi-Fi provisioning; hold-to-talk afterwards.
        boot_button_.OnClick([this]() {
            auto& app = Application::GetInstance();
            if (app.GetDeviceState() == kDeviceStateStarting) {
                EnterWifiConfigMode();
            }
        });
        boot_button_.OnPressDown([]() {
            Application::GetInstance().StartListening();
        });
        boot_button_.OnPressUp([]() {
            Application::GetInstance().StopListening();
        });

        // AUX: preserve the legacy GPIO6 behavior as chat toggle.
        aux_button_.OnClick([]() {
            Application::GetInstance().ToggleChatState();
        });
    }

public:
    WiselyC3AiV2Board()
        : boot_button_(BOOT_BUTTON_GPIO),
          aux_button_(AUX_BUTTON_GPIO) {
        InitializeCodecI2c();
        InitializeButtons();

        // Intentionally no eFuse writes here. C3_AI_V2 must not inherit
        // irreversible flash/GPIO configuration from unrelated Kevin C3 boards.
    }

    Led* GetLed() override {
        static GpioLed led(BUILTIN_LED_GPIO, BUILTIN_LED_OUTPUT_INVERT);
        return &led;
    }

    AudioCodec* GetAudioCodec() override {
        static Es8311AudioCodec audio_codec(
            codec_i2c_bus_, I2C_NUM_0,
            AUDIO_INPUT_SAMPLE_RATE, AUDIO_OUTPUT_SAMPLE_RATE,
            AUDIO_I2S_GPIO_MCLK, AUDIO_I2S_GPIO_BCLK, AUDIO_I2S_GPIO_WS,
            AUDIO_I2S_GPIO_DOUT, AUDIO_I2S_GPIO_DIN,
            AUDIO_CODEC_PA_PIN, AUDIO_CODEC_ES8311_ADDR);
        return &audio_codec;
    }
};

DECLARE_BOARD(WiselyC3AiV2Board);
