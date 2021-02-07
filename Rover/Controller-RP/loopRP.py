"""
loop dosyası içerisinde raspberry pi programımızın akışı sağlanacaktır..
resimler webSocketsOpencvServer üzerinden akışı sağlanacaktır..
roboSocketCom üzerinden pyserial kütüphanesi sayesinde verilerimizin akışı mikrokontrolcüye gidecektir.
"""
import socket,serial,threading,_thread,asyncio
from roboSocketCom import RoboSocketCom
from webSocketsOpencvServer import WebSocketsOpencvServer
from displayStabilizeServer import DisplayStabilizeServer

port = serial.Serial("COM5"  # com girilmesi gerekli
                         , baudrate=115200  # baund rate
                         , timeout=0
                         ,parity=serial.PARITY_NONE,
                         bytesize=serial.EIGHTBITS,
                         stopbits=serial.STOPBITS_ONE
                     )  # zaman aşım
# except serial.SerialException as exp:
#     print(f"""
#     -------------------------------Serial Kütühanesi COM Hatası --------------------------------------
#     |
#     | Serial Kütüphanesinden COM Bulunamadı Takılı olmayabilir ya da Kabloda Sorun olabilir...      |
#     | Hata Kodu : {exp}
#     |
#     ---------------------------------------------------------------------------------------------------
#     """)

async def roboRUN(serverHost,roboServerPort,roboOpencvServerPort,roboArmOpencvServerPort,roboDisplayStabilizeServerPort,loop):
    roboControl = RoboSocketCom(serverHost=serverHost, serverPort=roboServerPort,serialPort=port)
    roboOpencv = WebSocketsOpencvServer(serverHost=serverHost, serverPort=roboOpencvServerPort, camId=1)
    roboArmOpencv = WebSocketsOpencvServer(serverHost=serverHost, serverPort=roboArmOpencvServerPort, imutilsCamId=Ture,camPiState=True)
    roboDisplayStabilize = DisplayStabilizeServer(serverHost=serverHost, serverPort=roboDisplayStabilizeServerPort,)

    t1= loop.create_task(roboControl.socketRun())
    # t2= loop.create_task(roboOpencv.socketRun())
    # t3= loop.create_task(roboArmOpencv.socketRun())
    t4= loop.create_task(roboDisplayStabilize.socketRun())

    await t1,t4

def mainLoop():
    serverHost="0.0.0.0"
    roboServerPort=5000
    roboOpencvServerPort=5001
    roboArmOpencvServerPort=5002
    roboDisplayStabilizeServerPort=5003
    "---------------------------"
    loop = asyncio.get_event_loop()
    # cihazın isimini çekiyoruz
    hostname = socket.gethostname()
    # cihazın ip adresini çekiyoruz
    ip_address = socket.gethostbyname(hostname)
    print(f""" 

                                                            ``                                            
                                                        ....``                                          
                                                      ``--++``                                          
                                                      ``--++``                                          
                                                ````//``--++``                                          
                                                --hhmm----++````//                                      
                                              ..hhmmNN//--++``--dd::                                    
                                              yymmNNoo..--++``--mmhh``                                  
                                        ``  ::mmNNoo..  --++````//hh::                                  
                                        --::yyNNhh..    --++////++oo//``                                
                                      --oo++mmNN//``--++ssoooooooo++////--``                            
                                    --++yyoommmm::++ssyyyyyyyyyyyyssss++::::                            
                                    ..--ssssNNyyooyyyyyyyyyyyyyyyyyyyyss++//..                          
                                    ````++hhNNooyyyyyyyyyyyyyyyyyyyyyyyyss////                          
                                    ..//++ddNNooyyyyyyyyyyyyyyyyyyyyyyyyyyoo++``                        
                                ..//ooss++ddNNooyyyyyyyyyyyyyyyyyyyyyyyyyyss++``                        
                              ``++yyyyyyooddNNooyyyyyyyyyyyyyyyyyyyyyyyyyyyy::``                        
                            ..//yyyyyyyyoohhNNssssyyyyyyyyyyyyyyyyyyyyyyyyoo``                          
                            ::ssyyyyyyyyssssNNddooyyyyyyyyyyyyyyyyyyyyyyoo--  ``                        
                            ..:::://////++//NNmm++oossssssyyyyyyyyss++//ssss..                          
                            ````````````..++NNNNyy::----:::::://ssoo..``oomm++                          
                                      ``//hhNNmmmmoo..      ..oohh//    ..++::                          
                                    ``//ddNNhhhhNNmmss//:://ssmmyy..      ````                          
                                  ``++ddNNhh:://ddNNmmddddddmmyy--                                      
                                ``++ddmmdd//  ``//yyddmmmmhhss--                                        
                                ``hhNNdd//        --//++++::``                                          
                                  ++hh//                                                                
                                  ``//                                                                  
                                                                                                    

    ----------------------------------------GALLIPOLI ROV RASPBERRY PI CONTROLLER------------------------------------------
    |   Rov içinde ki Raspberry pi'nin ismi : {hostname}                                                             |
    |   Rov içinde ki Raspberry pi'nin ip adresi : {ip_address}                                                            |
    |---------------------------------------------------------------------------------------------------------------------|
    |   roboControl (RoboSocketCom) isimli sunucunun aldığı port ve ip_adress : {roboServerPort} -- ip {ip_address} == {serverHost}         |
    |   roboOpencv (RoboSocketCom) isimli sunucunun aldığı port ve ip_adress  : {roboOpencvServerPort} -- ip {ip_address} == {serverHost}         |
    -----------------------------------------------------------------------------------------------------------------------    
    """)


    loop.run_until_complete(roboRUN(serverHost, roboServerPort, roboOpencvServerPort,roboArmOpencvServerPort,roboDisplayStabilizeServerPort,loop))
    loop.run_forever()
    # loop.run_until_complete(roboRUN(serverHost, roboServerPort, roboOpencvServerPort))
if __name__ == '__main__':
    mainLoop()