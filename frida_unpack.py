#-*- coding:utf-8 -*-
# coding=utf-8
import frida
import sys

def on_message(message, data):
    base = message['payload']['base']
    size = int(message['payload']['size'])
    print hex(base),size
    # print session
    # dex_bytes = session.read_bytes(base, size)
    # f = open("1.dex","wb")
    # f.write(dex_bytes)
    # f.close()

package = sys.argv[1]
print "dex 导出目录为: /data/data/%s"%(package)
device = frida.get_usb_device()
pid = device.spawn(package)
session = device.attach(pid)
src = """
Interceptor.attach(Module.findExportByName("libart.so", "_ZN3art7DexFile10OpenMemoryEPKhjRKNSt3__112basic_stringIcNS3_11char_traitsIcEENS3_9allocatorIcEEEEjPNS_6MemMapEPKNS_10OatDexFileEPS9_"), {
    onEnter: function (args) {
      
        var begin = args[1]
        
        console.log("magic : " + Memory.readUtf8String(begin))
        console.log("size : " + Memory.readUInt(args[2]))
        var address = parseInt(begin,16) + 0x20

        var dex_size = Memory.readInt(ptr(address))

        console.log("dex_size :" + dex_size)
      
        var file = new File("/data/data/%s/" + dex_size + ".dex", "wb")
        file.write(Memory.readByteArray(begin, dex_size))
        file.flush()
        file.close()

        var send_data = {}
        send_data.base = parseInt(begin,16)
        send_data.size = dex_size
        send(send_data)
    },
    onLeave: function (retval) {
        if (retval.toInt32() > 0) {
        }
    }
});
"""%(package)

script = session.create_script(src)

script.on("message" , on_message)

script.load()
device.resume(pid)
sys.stdin.read()