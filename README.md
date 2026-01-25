# Casdoor SSO

通过 Casdoor 实现 SSO 单点登录集成

使用此插件前，请首先了解 [Casdoor](https://casdoor.org/)

## 全局配置

在 `backend/core/conf.py` 中添加以下内容：

```python
##################################################
# [ Plugin ] casdoor_sso
##################################################
# .env
CASDOOR_SSO_CLIENT_ID: str
CASDOOR_SSO_CLIENT_SECRET: str

# 基础配置（in plugin.toml）
CASDOOR_SSO_CERTIFICATE: str
CASDOOR_SSO_ENDPOINT: str
CASDOOR_SSO_ORG_NAME: str
CASDOOR_SSO_APPLICATION_NAME: str
CASDOOR_SSO_ACCESS_ENDPOINT: str  # Casdoor UI 地址
CASDOOR_SSO_FRONTEND_REDIRECT_URI: str
```

更多配置参考：[casdoor-python-sdk](https://github.com/casdoor/casdoor-python-sdk/blob/master/README.md)
