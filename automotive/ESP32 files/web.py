def connect():
    import network
    import time
    import machine
    
    ssid = "ssid"
    password = "password"
 
    station = network.WLAN(network.STA_IF)
    
    if station.isconnected() == True:
        print("Already connected")
        return
    
    station.active(True)
    
    if machine.reset_cause() != machine.SOFT_RESET:
        station.ifconfig(('static ip tbd', 'subnet mask', 'host ip', 'dns server')) 
        
    
    station.connect(ssid, password)
 
    while station.isconnected() == False:
        pass
    
    print("Connection successful")
    
    from machine import Pin
    p = Pin(2, Pin.OUT)
    print(station.ifconfig())
    p.on()
    time.sleep(5)
    p.off()
