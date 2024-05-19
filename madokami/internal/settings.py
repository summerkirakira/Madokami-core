from madokami.plugin.settings_register import register_setting
from madokami.db import Session, engine
from madokami.crud import get_plugin_config, add_plugin_config


_internal_settings = [
    {
        'key': 'madokami.config.proxy_url',
        'name': '代理地址',
        'description': '为请求设置代理地址(如http://127.0.0.1:1080)，无需代理请留空',
        'default': None
    },
    {
        'key': 'madokami.config.cache_path',
        'name': '缓存路径',
        'description': '为Madokami设置缓存路径',
        'default': './data/cache'
    },
    {
        'key': 'madokami.config.aria2_host',
        'name': 'Aria2 地址',
        'description': '为下载器指定Aria2地址 (重启生效)',
        'default': 'http://localhost'
    },
    {
        'key': 'madokami.config.aria2_port',
        'name': 'Aria2 端口',
        'description': '为下载器指定Aria2端口 (重启生效)',
        'default': 6800
    },
    {
        'key': 'madokami.config.aria2_secret',
        'name': 'Aria2 密钥',
        'description': '为下载器指定PRC密钥 (重启生效)',
        'default': 'MADOKAMI'
    },
    {
        'key': 'madokami.config.bangumi_token',
        'name': 'Bangumi秘钥',
        'description': '用于Bangumi API请求的秘钥，请勿滥用',
        'default': '8jkdHoKPLrOuI3WN8Xv5BLMp0MgAZ5Dk7KXP2i4j'
    }
]


def register_internal_settings():
    with Session(engine) as session:
        for setting in _internal_settings:
            config = get_plugin_config(session=session, key=setting['key'])
            if config is None and 'default' in setting and setting['default'] is not None:
                add_plugin_config(session=session, key=setting['key'], value=setting['default'])
            register_setting(key=setting['key'], name=setting['name'], description=setting['description'])
