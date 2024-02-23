# diane-docker

一个可以运行[`DIANE`](https://sites.cs.ucsb.edu/~vigna/publications/2021_SP_Diane.pdf)的docker环境。

* 以下步骤在`Ubuntu 20.04`环境下能够成功运行，其他环境未经测试，最后测试时间：2024-01-06
* `DIANE`比较吃内存，建议机器至少配备64GB内存

## 环境配置
1. 安装 `docker`：参考[官方指南](https://docs.docker.com/engine/install/)
2. 安装依赖：`sudo apt-get install android-tools-adb usbutils`
3. 使用adb连接手机，并在手机上永远允许本设备进行调试
4. 克隆本项目到本地：`git clone https://github.com/VoodooChild99/diane-docker.git`
5. 构建docker镜像:
```shell
cd diane-docker
# 如果你在墙后，请运行以下命令设置代理，否则可以忽略该命令。
# 注意：把example.com:port换成自己的代理地址，不能是localhost/127.0.0.1/0.0.0.0等，
# 可以打开自己代理软件的“允许本地连接” / “Allow LAN”，然后用自己的主机ip
export PROXY_ADDRESS=http://example.com:port
# 这会构建一个名为`diane`的docker镜像
./build_docker.sh
```

## 运行
运行脚本`./run.sh`来启动环境，后续操作都在容器中完成。可以多次运行`./run.sh`获得多个`shell`。`run.sh`中的`PHONE_MODEL`变量需要根据自己的手机型号进行调整

**！！注意！！**
进入容器后，材料都在`/root`目录下，需要注意以下目录：
* `/root/diane`：`DIANE`的源码，后面需要运行里面的`Python`脚本
* `/root/android_sdk`：内含全版本Android SDK
* `/root/workdir`：用于数据持久化的工作目录，由host的`diane-docker/workdir`目录挂载，最好保证一切数据材料（输入或输出）都在这个目录

## 运行环境
需要一台root后的android手机，一台pc，以及一台热点设备。要求android手机连接到热点设备提供的网络，android设备通过usb连接pc，pc能够ssh连接到热点设备上

## 使用方法

### 配置Frida和adb
```shell
# --arm32: 使用arm32版本的Frida server，如果不提供，默认使用ARM64版本
# --enable-bypass：开启Frida检测绕过机制，如果不提供，默认不启用该机制
python /root/workdir/script/prep_frida.py [--arm32] [--enable-bypass] <DEVICE_ID>
```
用来在手机上启动frida，并且配置adb。运行结束不会自动退出，需要ctrl+C

### 录制UI操作
```shell
python /root/workdir/script/record.py /root/workdir/PROJ_DIR
```
用来录制和设备交互的UI动作，运行DIANE前**必须**先录制

### 运行DIANE

```shell
# CONFIG：指向配置文件路径
python /root/workdir/script/run.py /root/workdir/PROJ_DIR
```

首次运行会帮你在`/root/workdir`下面创建一个`config.ini`文件，并在`/root/workdir/PROJ_DIR`下创建一个`config.json`文件，具体含义如下

| 字段 | 必需 | 描述 |
| :--- | :--- | :--- |
|`reran_record_path`        | √ | UI操作记录，用于重放 |
|`send_functions`           | x | 指定sendMessage函数，如果不提供会自动分析 |
|`fuzzing_candidates`       | x | 代码中没用到 |
|`sweet_spots`              | x | 指定sweet spots，如果不提供会自动分析 |
|`leaf_pickle`              | x | 指定分析中间结果（pickle格式），不提供会从头分析 |
|`apk_path`                 | √ | 指定要分析的APK |
|`android_sdk_platforms`    | √ | 指定Android SDK路径 |
|`bad_functions`            | √ | 静态分析method黑名单 |
|`proc_name`                | √ | Android APP进程名 |
|`device_id`                | √ | Android设备id，用于连接`adb` |
|`android_ip`               | √ | Android设备IP地址 |
|`device_ip`                | √ | IoT设备IP地址,云场景下是与手机通信的服务器IP地址 |
|`ip_hot_spot`              | √ | 热点IP地址 |
|`pass_ap`                  | √ | 热点口令 |
|`skip_methods`             | √ | Frida hook method黑名单 |
|`skip_classes`             | √ | Frida hook class黑名单 |
|`frida_hooker_pickle`      | √ | TODO |
|`fuzz_pcap_path`           | x | TODO |
|`pcap_path`                | x | TODO |
|`results_path`             | √ | 存放fuzz结果 |
|`fmt_data_keys`            | x | 代码中没用到 |
|`user_ap`                  | √ | 热点设备的用户名 |
|`if_ap`                    | √ | 热点设备的接口名 |
|`phys_ip`                  | x | 实际设备的IP，仅在云场景下有用 |
|`ip_hot_spot_cloud`        | x | 云场景下，设备连接的热点的IP |
|`user_ap_cloud`            | x | 云场景下，设备连接的热点设备的用户名 |
|`pass_ap_cloud`            | x | 云场景下，设备连接的热点设备的口令 |
|`if_ap_cloud`              | x | 云场景下，设备连接的热点设备的接口名 |
|`spawn_timeout`            | x | 等待APP启动的时间（单位是秒，默认30秒） |
|`enable_bypass`            | x | 开启Frida检测绕过机制 |
|`sweet_spots`              | x | sweet spot函数，fuzz的潜在对象，需要手动从`sweet_spot.json`中拷贝，如果不提供会再分析一遍 |
|`send_functions`           | x | senders函数，需要手动从`senders.json`中拷贝，如果不提供会再分析一遍 |
|`skip_methods`             | x | 分析过程中需要忽略的方法，需要手动从`ignore_methods.json`中拷贝 |