# Casdoor SSO

通过 Casdoor 实现 SSO 单点登录集成，支持通过 Casdoor 用户信息自动创建并登录系统用户

使用此插件前，请首先了解 [Casdoor](https://casdoor.org/)

## 插件类型

- 扩展级插件
- 扩展目标：`admin`

## 配置说明

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

在 `backend/.env` 中添加以下内容：

```env
# [ Plugin ] casdoor_sso
CASDOOR_SSO_CLIENT_ID=''
CASDOOR_SSO_CLIENT_SECRET=''
```

插件目录下 `plugin.toml` 的 `[settings]` 中包含以下内容：

```toml
[settings]
CASDOOR_SSO_CERTIFICATE = ''
CASDOOR_SSO_ENDPOINT = 'http://localhost:8080'
CASDOOR_SSO_ORG_NAME = 'casdoor'
CASDOOR_SSO_APPLICATION_NAME = 'Casdoor'
CASDOOR_SSO_ACCESS_ENDPOINT = 'http://localhost:8080'
CASDOOR_SSO_FRONTEND_REDIRECT_URI = 'http://localhost:8080/casdoor/callback'
```

## 使用方式

1. 在 Casdoor 中创建应用并配置回调地址
2. 将 Casdoor 应用的 Client ID、Client Secret 写入项目环境变量
3. 安装并启用插件后，重启后端服务
4. 前端获取授权链接并跳转 Casdoor，回调接口会完成用户创建和登录
5. 更多配置参考：[casdoor-python-sdk](https://github.com/casdoor/casdoor-python-sdk/blob/master/README.md)

## 卸载说明

- 卸载插件后，建议同步移除 Casdoor 相关环境变量和插件基础配置
- 如前端登录页已集成 Casdoor 登录入口，请同步清理对应集成

## 联系方式

- 作者：`wu-clan`
- 反馈方式：提交 Issue 或 PR
