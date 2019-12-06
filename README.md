# frida-unpack

Android  SDK版本8.0以下，基于Frida的脱壳工具。

## 0x0 frida环境搭建

frida环境搭建，参考：[[Android Hook工具之Frida 安装配置教程](https://www.jianshu.com/p/7be526b77bd2)

## 0x2 原理说明

利用frida hook libart.so中的OpenMemory方法，拿到内存中dex的地址，计算出dex文件的大小，从内存中将dex导出。
ps：查看OpenMemory的导出名称，可以将手机中的libart.so（存放路径为/system/lib/目录）通过adb pull命令导出到电脑，然后利用：
`nm libart.so |grep OpenMemory`命令来查看到出名。

## 0x3 脚本用法

- 在手机上启动frida server端

- 修改OpenMemory.js脚本

  ```js
  //将xxx.xxx.xxx改为要脱壳的应用的包名
  var file = new File("/data/data/xxx.xxx.xxx/" + dex_size + ".dex", "wb")
  ```

  

- 执行脱壳脚本 

```
    执行./inject.sh 要脱壳的应用的包名 OpenMemory.js
```

- 脱壳后的dex保存在`/data/data/应用包名/`目录下

## 0x4 脚本测试环境

此脚本在以下环境测试通过

- android os: 7.1.2 32bit  (64位可能要改OpenMemory的签名)
- legu: libshella-2.8.so
- 360: libjiagu.so

## 0x5 参考链接

- [Android Hook工具之Frida 安装配置教程](https://www.jianshu.com/p/7be526b77bd2)
- [Android基于OpenMemory的脱壳]([https://mabin004.github.io/2018/08/22/Android%E5%9F%BA%E4%BA%8EOpenMemory%E7%9A%84%E8%84%B1%E5%A3%B3/](https://mabin004.github.io/2018/08/22/Android基于OpenMemory的脱壳/))
- [基于Frida框架打造Art模式下的脱壳工具（OpenMemory）的原理分析](https://blog.csdn.net/QQ1084283172/article/details/80956614)

## 0x06 python脚本支持

`python frida_unpack.py 应用包名`

## 0x07 相关技巧

- 利用`c++filt`命令还原C++ name managling之后的函数名

  ```
  c++filt _ZN3art7DexFile10OpenMemoryEPKhjRKNSt3__112basic_stringIcNS3_11char_traitsIcEENS3_9allocatorIcEEEEjPNS_6MemMapEPKNS_10OatDexFileEPS9_
  
  输出：
  art::DexFile::OpenMemory(unsigned char const*, unsigned int, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, unsigned int, art::MemMap*, art::OatDexFile const*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >*)
  ```

## 0x08 遇到的问题

- 执行frida脚本时出现**Error: access violation accessing 0x….**类似的异常

解决方案： 更换模拟器或手机
