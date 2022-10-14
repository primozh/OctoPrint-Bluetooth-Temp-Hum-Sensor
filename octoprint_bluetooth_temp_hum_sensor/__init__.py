from random import random
import octoprint.plugin
from octoprint.util import RepeatedTimer

from octoprint_bluetooth_temp_hum_sensor.constants import AdvertisingFormat

class BluetoothTempAndHumDataPlugin(octoprint.plugin.StartupPlugin,
                                    octoprint.plugin.TemplatePlugin,
                                    octoprint.plugin.SettingsPlugin,
                                    octoprint.plugin.AssetPlugin):
    
    def __init__(self):
        self.__Settings = dict(
            Temperature = "24°C",
            Humidity="58%",
            Battery="45%"
        )

    def __start_timer(self):
        self.__update_timer = RepeatedTimer(5, self.on_timer, run_first = True)
        self.__update_timer.start()

    def on_timer(self):
        # self._logger.info(self._identifier)
        self._plugin_manager.send_plugin_message(self._identifier, dict(
                Temperature= "{:.2f}".format(random() * 20),
                Humidity="{:.2f}".format(random() * 60),
                Battery=100    
            )
        )

    # OCTOPRINT 
    def on_after_startup(self):
        self._logger.info("Hello World!")
        self.__start_timer();

    def get_settings_defaults(self):
        return dict(
            config_version_key=1,
            mac_address="",
            show_temperature=True,
            show_humidity=True,
            show_battery=True,
            advertising_format=AdvertisingFormat.BTHOME_ENCRYPTED.name,
            binding_key="",
            refresh_interval=10
        )

    def on_settings_save(self, data):
        old_mac = self._settings.get(["mac_address"])

        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        new_mac = self._settings.get(["mac_address"])
        if old_mac != new_mac:
            self._logger.info("mac_address changed from %s to %s", old_mac, new_mac)

    def get_template_vars(self):
        return dict(
            advertising_formats=[e.name for e in AdvertisingFormat]
        )
    
    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False)
        ]

    def get_assets(self):
        return dict(
            js=["js/bluetooth_temp_hum.js"]
        )

__plugin_pythoncompat__ = ">=3.7,<4"
__plugin_implementation__ = BluetoothTempAndHumDataPlugin()