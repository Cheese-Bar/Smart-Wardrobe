timeanddate.onMinuteChanged(function () {
    basic.showIcon(IconNames.No)
    dht11_dht22.queryData(
    DHTtype.DHT11,
    DigitalPin.P0,
    true,
    false,
    true
    )
    temp = dht11_dht22.readData(dataType.temperature)
    radio.sendValue("temp", temp)
    humidity = dht11_dht22.readData(dataType.humidity)
    radio.sendValue("humidity", humidity)
    pressure = BMP280.pressure()
    radio.sendValue("pressure", pressure)
    basic.showIcon(IconNames.Yes)
})
let pressure = 0
let humidity = 0
let temp = 0
radio.setGroup(1)
BMP280.Address(BMP280_I2C_ADDRESS.ADDR_0x76)
