import octoprint.plugin

from octoprint_bluetooth_temp_hum_sensor.constants import AdvertisingFormat

class BluetoothTempAndHumDataPlugin(octoprint.plugin.StartupPlugin,
                                    octoprint.plugin.TemplatePlugin,
                                    octoprint.plugin.SettingsPlugin):
    
    def on_after_startup(self):
        self._logger.info("Hello World!")

    def get_settings_defaults(self):
        return dict(
            config_version_key=1,
            mac_address="",
            show_temperature=True,
            show_humidity=True,
            show_battery=True,
            advertising_format=AdvertisingFormat.BTHOME_ENCRYPTED.name,
            binding_key=""
        )

    def on_settings_save(self, data):
        old_mac = self._settings.get(["mac_address"])

        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        new_mac = self._settings.get(["mac_address"])
        if old_mac != new_mac:
            self._logger.info("mac_address changed from {old_mac} to {new_mac}", old_mac, new_mac)

    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False),
        ]

    def get_template_vars(self):
        return dict(
            advertising_formats=[e.name for e in AdvertisingFormat]
        )

__plugin_pythoncompat__ = ">=3.7,<4"
__plugin_implementation__ = BluetoothTempAndHumDataPlugin()