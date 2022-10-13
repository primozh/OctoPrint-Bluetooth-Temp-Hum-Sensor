import octoprint.plugin

class BluetoothTempAndHumDataPlugin(octoprint.plugin.StartupPlugin,
                                    octoprint.plugin.TemplatePlugin,
                                    octoprint.plugin.SettingsPlugin):
    
    def on_after_startup(self):
        self._logger.info("Hello World!")

        bluetoothScanner = BluetoothScanner(self._logger)
        asyncio.run(bluetoothScanner.scan())

    def get_settings_defaults(self):
        return dict(
            mac_address=""
        )

    def on_settings_save(self, data):
        old_mac = self._settings.get(["mac_address"])

        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        new_mac = self._settings.get(["mac_address"])
        if old_mac != new_mac:
            self._logger.info("mac_address changed from {old_mac} to {new_mac}", old_mac, new_mac)

    def get_template_vars(self):
        return dict(mac_address=self._settings.get(["mac_address"]))

__plugin_pythoncompat__ = ">=3.7,<4"
__plugin_implementation__ = BluetoothTempAndHumDataPlugin()