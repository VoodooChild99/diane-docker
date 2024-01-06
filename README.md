# diane-eval

## 环境配置
方便起见，使用`docker`配置`DIANE`的运行环境
1. 安装 `docker`：参考[这里](https://docs.docker.com/engine/install/)
2. 构建docker镜像:
```shell
# 把example.com:port换成自己的代理地址，注意不能是本地代理，
# 可以打开自己代理软件的“允许本地连接”，然后用自己的主机ip
export PROXY_ADDRESS=http://example.com:port
# 这会构建一个名为`diane`的docker镜像
./build_docker.sh
```

## 运行
运行`docker`：`./run.sh`，后续操作都在`docker`中完成

**！！注意！！**
进入docker后，材料都在`/root`目录下，需要注意以下目录：
* `/root/diane`：`DIANE`的源码，后面需要运行里面的`Python`脚本
* `/root/android_sdk`：内含全版本Android SDK
* `/root/workdir`：存放数据的工作目录，用于数据持久化，由host的workdir目录挂载，最好保证一切数据材料（输入或输出）都在这个目录


## `DIANE`使用方法
