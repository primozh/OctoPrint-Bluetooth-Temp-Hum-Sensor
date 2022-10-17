import octoprint.plugin
from flask import jsonify
from octoprint_bluetooth_temp_hum_sensor.bluetooth_analyzer import BluetoothAdvertismentAnalyzer
from octoprint_bluetooth_temp_hum_sensor.bluetooth_scanner import BluetoothScanner
from octoprint_bluetooth_temp_hum_sensor.constants import AdvertisingFormat

class BluetoothTempAndHumDataPlugin(octoprint.plugin.StartupPlugin,
                                    octoprint.plugin.ShutdownPlugin,
                                    octoprint.plugin.TemplatePlugin,
                                    octoprint.plugin.SettingsPlugin,
                                    octoprint.plugin.AssetPlugin,
                                    octoprint.plugin.BlueprintPlugin):
    
    def __init__(self):
        self.bluetoothListener = None
        self.aeskeys = {}

    # OCTOPRINT 
    def on_after_startup(self):
        mac_address = self._settings.get(["mac_address"])
        binding_key = self._settings.get(["binding_key"])

        if mac_address:
            if binding_key:
                self.aeskeys[mac_address] = binding_key
            
            self.bluetoothListener = BluetoothAdvertismentAnalyzer(self._identifier, mac_address, self.aeskeys, self._logger, self._plugin_manager)
            self._logger.info("Starting BT listener")
        else:
            self._logger.info("MAC address not provided! Could not start BT listener")

    def on_shutdown(self):
        self.bluetoothListener.stop()
        return super().on_shutdown()

    def get_settings_defaults(self):
        return dict(
            config_version_key=1,
            mac_address="",
            show_temperature=True,
            show_humidity=True,
            show_battery=True,
            advertising_format=AdvertisingFormat.BTHOME.name,
            binding_key="",
            refresh_interval=10
        )

    def on_settings_save(self, data):
        old_mac = self._settings.get(["mac_address"])

        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        new_mac = self._settings.get(["mac_address"])
        if old_mac != new_mac:
            self._logger.info("mac_address changed from %s to %s", old_mac, new_mac)
            if self.bluetoothListener != None:
                self.bluetoothListener.stop()
            self.bluetoothListener = BluetoothAdvertismentAnalyzer(self._identifier, new_mac, self.aeskeys, self._logger, self._plugin_manager)
            self._logger.info("Restarting BT listener with new MAC address %s", new_mac)


    def get_template_vars(self):
        return dict(
            advertising_formats=[e.name for e in AdvertisingFormat]
        )

    def get_assets(self):
        return dict(
            js=["js/bluetooth_temp_hum.js"]
        )

    @octoprint.plugin.BlueprintPlugin.route("/scan-devices", methods=["POST"])
    def scan_for_bt_devices(self):
        self.bluetooth_scanner = BluetoothScanner(self._identifier, self._logger, self._plugin_manager)
        return jsonify(
            {
                "started": "true"
            }
        )

    
    @octoprint.plugin.BlueprintPlugin.route("/stop-scan", methods=["POST"])
    def stop(self):
        self.bluetooth_scanner.stop()
        return jsonify(
            {
                "stopped": "true"
            }
        )

__plugin_name__ = "Bluetooth Temperature and Humidty Plugin"
__plugin_pythoncompat__ = ">=3.7,<4"
__plugin_implementation__ = BluetoothTempAndHumDataPlugin()