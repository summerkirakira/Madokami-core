from .models import User, PluginConfig, Plugin, Oauth2Client, EngineSchedulerConfig, DownloadHistory, MediaInfo, Content
from sqlmodel import Session, create_engine, select, SQLModel, delete
from typing import Optional
from .db import engine


def create_user(*, session: Session, user: User) -> User:

    old_user = session.exec(select(User).where(User.username == user.username)).first()
    if old_user:
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


def get_engine_scheduler_config(*, session: Session, namespace: str) -> Optional[EngineSchedulerConfig]:
    engine_scheduler_config = session.exec(select(EngineSchedulerConfig).where(EngineSchedulerConfig.namespace == namespace)).first()
    if engine_scheduler_config:
        return engine_scheduler_config
    else:
        return None


def add_engine_scheduler_config(*, session: Session, engine_scheduler_config: EngineSchedulerConfig) -> EngineSchedulerConfig:
    old_engine_scheduler_config = session.exec(select(EngineSchedulerConfig).where(EngineSchedulerConfig.namespace == engine_scheduler_config.namespace)).first()
    if old_engine_scheduler_config:
        session.delete(old_engine_scheduler_config)
    session.add(engine_scheduler_config)
    session.commit()
    session.refresh(engine_scheduler_config)
    return engine_scheduler_config


def get_engines_schedule_by_plugin_namespace(*, session: Session, namespace: str) -> list[EngineSchedulerConfig]:
    engine_scheduler_configs = session.exec(select(EngineSchedulerConfig).where(EngineSchedulerConfig.plugin_name == namespace)).all()
    return [engine_scheduler_config for engine_scheduler_config in engine_scheduler_configs]


def get_download_histories() -> list[DownloadHistory]:
    with Session(engine) as session:
        download_histories = session.exec(select(DownloadHistory)).all()
        return [download_history for download_history in download_histories]


def get_download_history_by_link(link: str) -> Optional[DownloadHistory]:
    with Session(engine) as session:
        download_history = session.exec(select(DownloadHistory).where(DownloadHistory.link == link)).first()
        if download_history:
            return download_history
        else:
            return None


def add_download_history(download_history: DownloadHistory) -> DownloadHistory:
    with Session(engine) as session:
        old_download_history = get_download_history_by_link(download_history.link)
        if old_download_history:
            session.delete(old_download_history)
        session.add(download_history)
        session.commit()
        session.refresh(download_history)
        return download_history


def add_media_info(media_info: MediaInfo) -> MediaInfo:
    with Session(engine) as session:
        session.add(media_info)
        session.commit()
        session.refresh(media_info)
        return media_info


def get_median_info_by_id(id: str) -> Optional[MediaInfo]:
    with Session(engine) as session:
        media_info = session.exec(select(MediaInfo).where(MediaInfo.id == id)).first()
        if media_info:
            return media_info
        else:
            return None


def add_content(content: Content) -> Content:
    with Session(engine) as session:
        session.add(content)
        session.commit()
        session.refresh(content)
        return content

