$(function() {
    function BluetoothTempHumSensorViewModel(parameters) {
        var self = this;

        self.global_settings = parameters[0];
        self.currentTemp = ko.observable("- °C");
        self.currentBattery = ko.observable("- %");
        self.currentHumidity = ko.observable("- %");

        self.devices = ko.observableArray();

        self.blueprintUrl = OctoPrint.getBlueprintUrl("bluetooth_temp_hum_sensor")

        self.onDataUpdaterPluginMessage = function(plugin, message) {
            if (plugin !== "bluetooth_temp_hum_sensor") {
                return;
            }
            if (message.temperature) {
                self.currentTemp(message.temperature);
                self.currentBattery(message.battery);
                self.currentHumidity(message.humidity);
            } else {
                self.devices.push(message.device)
            }
            
        };

        self.onBeforeBinding = function() {
            self.local_settings = self.global_settings.settings.plugins.bluetooth_temp_hum_sensor;
        };

        self.searchDevices = function() {
            self.devices.removeAll();
            OctoPrint.post(self.blueprintUrl + "scan-devices")
                .done(function(response) {
                    console.log("API:", response)
                })
        }

        self.stop = function() {
            OctoPrint.post(self.blueprintUrl + "stop-scan")
                .done(function(response) {
                    console.log("API:", response)
                })
        }
        
    };

    OCTOPRINT_VIEWMODELS.push({
        construct: BluetoothTempHumSensorViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#navbar_plugin_bluetooth_temp_hum_sensor", "#settings_plugin_bluetooth_temp_hum_sensor"]
    });
});