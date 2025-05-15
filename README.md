## Casdoor OSS

使用此插件前，请首先了解 [Casdoor](https://casdoor.org/)

## 配置

1. 在环境变量文件 `.env` 中添加以下内容:

    ```dotenv
    # Casdoor
    CASDOOR_CLIENT_ID='Casdoor 应用 client_id'
    CASDOOR_CLIENT_SECRET='Casdoor 应用 client_secret'
    ```
2. 在 `core/conf.py` 中添加以下内容:

    ```python
    # Plugin Casdoor
    # .env Casdoor
    CASDOOR_CLIENT_ID: str
    CASDOOR_CLIENT_SECRET: str
   
    # Casdoor
    CASDOOR_CERTIFICATE: str = ''
    CASDOOR_ENDPOINT: str = 'http://localhost:8080'
    CASDOOR_ORG_NAME: str = 'casdoor'
    CASDOOR_APPLICATION_NAME: str = 'Casdoor'
    CASDOOR_FRONT_ENDPOINT: str = 'http://localhost:8080'  # Casdoor UI 地址
    CASDOOR_FRONTEND_REDIRECT_URI: str = ''  # 成功后的重定向 URI，可参考：backend/app/admin/conf.py
    ```
   
3. 更新配置，参考：[casdoor-python-sdk](https://github.com/casdoor/casdoor-python-sdk/blob/master/README.md)
