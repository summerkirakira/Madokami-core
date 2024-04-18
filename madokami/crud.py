from .models import User, PluginConfig, Plugin, Oauth2Client
from sqlmodel import Session, create_engine, select, SQLModel, delete
from typing import Optional


def create_user(*, session: Session, user: User) -> User:

    user = session.exec(select(User).where(User.username == user.username)).first()
    if user:
        raise ValueError("User already exists")

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def add_plugin_config(*, session: Session, key: str, value: str) -> None:
    plugin_config = session.exec(select(PluginConfig).where(PluginConfig.key == key)).first()
    if plugin_config:
        plugin_config.value = value
    else:
        plugin_config = PluginConfig(key=key, value=value)

    session.add(plugin_config)
    session.commit()
    session.refresh(plugin_config)


def get_plugin_config(*, session: Session, key: str) -> str | None:
    plugin_config = session.exec(select(PluginConfig).where(PluginConfig.key == key)).first()
    if plugin_config:
        return plugin_config.value
    else:
        return None


def get_plugins(*, session: Session) -> list[Plugin]:
    plugins = session.exec(select(Plugin)).all()
    return [plugin for plugin in plugins]


def get_plugin_by_namespace(*, session: Session, namespace: str) -> Optional[Plugin]:
    plugin = session.exec(select(Plugin).where(Plugin.namespace == namespace)).first()
    if plugin:
        return plugin
    else:
        return None


def add_plugin(*, session: Session, plugin: Plugin) -> Plugin:
    old_plugin = session.exec(select(Plugin).where(Plugin.namespace == plugin.namespace)).first()
    if old_plugin:
        session.delete(old_plugin)
    session.add(plugin)
    session.commit()
    session.refresh(plugin)
    return plugin


def active_plugin(*, session: Session, namespace: str) -> Plugin:
    plugin = session.exec(select(Plugin).where(Plugin.namespace == namespace)).first()
    if plugin:
        plugin.is_active = True
        session.add(plugin)
        session.commit()
        session.refresh(plugin)
        return plugin
    else:
        raise ValueError("Plugin not found")


def deactivate_plugin(*, session: Session, namespace: str) -> Plugin:
    plugin = session.exec(select(Plugin).where(Plugin.namespace == namespace)).first()
    if plugin:
        plugin.is_active = False
        session.add(plugin)
        session.commit()
        session.refresh(plugin)
        return plugin
    else:
        raise ValueError("Plugin not found")


def get_oauth2_client(*, session: Session, token: str) -> Optional[Oauth2Client]:
    oauth2_client = session.exec(select(Oauth2Client).where(Oauth2Client.client_secret == token)).first()
    if oauth2_client:
        return oauth2_client
    else:
        return None
