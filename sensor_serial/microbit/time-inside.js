timeanddate.onMinuteChanged(function () {
    dht11_dht22.queryData(
    DHTtype.DHT11,
    DigitalPin.P0,
    true,
    false,
    true
    )
    Itemp = dht11_dht22.readData(dataType.temperature)
    serial.writeValue("Itemp", Itemp)
    Ihumidity = dht11_dht22.readData(dataType.humidity)
    serial.writeValue("Ihumidity", Ihumidity)
})
radio.onReceivedValue(function (name, value) {
    if (name == "temp") {
        temp = value
        serial.writeValue("Otemp", temp)
    } else if (name == "humidity") {
        humidity = value
        serial.writeValue("Ohumidity", humidity)
    } else if (name == "pressure") {
        pressure = value
        serial.writeValue("Opressure", pressure)
    } else {
        basic.showIcon(IconNames.No)
    }
})
timeanddate.onHourChanged(function () {
    if (Ihumidity < 20) {
        pins.digitalWritePin(DigitalPin.P1, 1)
    } else {
        pins.digitalWritePin(DigitalPin.P1, 0)
    }
})
let pressure = 0
let humidity = 0
let temp = 0
let Ihumidity = 0
let Itemp = 0
radio.setGroup(1)
basic.showIcon(IconNames.Happy)
