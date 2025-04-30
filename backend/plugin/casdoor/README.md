## Casdoor OSS

使用此插件前，请首先了解 [Casdoor](https://casdoor.org/)

您还需要注意以下事项：

1. 必须在环境变量文件 .env 中添加以下内容:

    ```dotenv
    CASDOOR_CLIENT_ID='Casdoor 应用 client_id'
    CASDOOR_CLIENT_SECRET='Casdoor 应用 client_secret'
    ```

2. 在本地创建一个文件为 `CASDOOR_CERTIFICATE` 的文件，然后将 Casdoor 公钥证书填入到文件内
3. 更新插件内配置文件 conf.py 中的配置

   `secrets_dir`：刚才创建的 `CASDOOR_CERTIFICATE` 文件存放路径

   `Casdoor` 相关配置，可参考：[casdoor-python-sdk](https://github.com/casdoor/casdoor-python-sdk)
