# diane-docker

一个可以运行[`DIANE`](https://sites.cs.ucsb.edu/~vigna/publications/2021_SP_Diane.pdf)的docker环境。

* 以下步骤在`Ubuntu 20.04`环境下能够成功运行，其他环境未经测试，最后测试时间：2024-01-06
* `DIANE`比较吃内存，建议机器至少配备32GB内存

## 环境配置
1. 安装 `docker`：参考[官方指南](https://docs.docker.com/engine/install/)
2. 克隆本项目到本地：`git clone https://github.com/VoodooChild99/diane-docker.git`
2. 构建docker镜像:
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
运行脚本`./run.sh`来启动环境，后续操作都在容器中完成。可以多次运行`./run.sh`获得多个`shell`。

**！！注意！！**
进入容器后，材料都在`/root`目录下，需要注意以下目录：
* `/root/diane`：`DIANE`的源码，后面需要运行里面的`Python`脚本
* `/root/android_sdk`：内含全版本Android SDK
* `/root/workdir`：用于数据持久化的工作目录，由host的`diane-docker/workdir`目录挂载，最好保证一切数据材料（输入或输出）都在这个目录


## `DIANE`使用方法
```shell
# CONFIG：指向配置文件路径
# PHASE：可选参数，用于设置运行阶段，一般不用特别设置
python diane/run.py CONFIG [PHASE]
```

### 配置文件
为了使用`DIANE`，分析人员需要对每一个待分析目标编写`JSON`格式的配置文件，字段及其含义如下：

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
|`device_ip`                | √ | IoT设备IP地址 |
|`ip_hot_spot`              | √ | 热点IP地址 |
|`pass_ap`                  | √ | 热点口令 |
|`skip_methods`             | √ | Frida hook method黑名单 |
|`skip_classes`             | √ | Frida hook class黑名单 |
|`frida_hooker_pickle`      | √ | TODO |
|`fuzz_pcap_path`           | x | TODO |
|`pcap_path`                | x | TODO |
|`results_path`             | √ | 存放fuzz结果 |
|`fmt_data_keys`            | x | 代码中没用到 |

### 录制UI操作
