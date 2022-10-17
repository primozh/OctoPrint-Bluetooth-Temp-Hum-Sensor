$(function() {
    function BluetoothTempHumSensorViewModel(parameters) {
        var self = this;

        self.global_settings = parameters[0];
        self.currentTemp = ko.observable("");
        self.currentBattery = ko.observable("");
        self.currentHumidity = ko.observable("");

        self.onDataUpdaterPluginMessage = function(plugin, message) {
            if (plugin !== "bluetooth_temp_hum_sensor") {
                return;
            }
            self.currentTemp(message.Temperature);
            self.currentBattery(message.Battery);
            self.currentHumidity(message.Humidity);
        };

        self.onBeforeBinding = function() {
            self.local_settings = self.global_settings.settings.plugins.bluetooth_temp_hum_sensor;
        };
        
    };

    OCTOPRINT_VIEWMODELS.push({
        construct: BluetoothTempHumSensorViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#navbar_plugin_bluetooth_temp_hum_sensor"]
    });
});