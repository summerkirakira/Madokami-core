from fastapi import APIRouter, HTTPException, Depends
from .models import SettingsAllResponse, InfoMessage, UpdateSettingBody
from madokami.drivers.deps import SessionDep, get_client_id
from madokami.crud import get_plugin_config, add_plugin_config
from sqlmodel import Session


settings_router = APIRouter(tags=["Settings"])


def convert_settings(session: Session, key: str, name: str, description: str) -> SettingsAllResponse.SettingRecord.Setting:
    config = get_plugin_config(session=session, key=key)
    return SettingsAllResponse.SettingRecord.Setting(
        key=key,
        name=name,
        description=description,
        value=config
    )


@settings_router.get("/settings/all", response_model=SettingsAllResponse, dependencies=[Depends(get_client_id)])
def get_settings(session: SessionDep):
    from madokami import get_app
    app = get_app()
    config_dict = app.plugin_manager.settings
    setting_records = []
    try:
        for namespace, configs in config_dict.items():
            setting_records.append(
                SettingsAllResponse.SettingRecord(
                    namespace=namespace,
                    settings=[convert_settings(session=session, key=config.key, name=config.name, description=config.description) for config in configs]
                )
            )
        return SettingsAllResponse(data=setting_records)
    except Exception as e:
        return SettingsAllResponse(message=f'Failed to retrieve settings: {e}', success=False)


@settings_router.post("/settings/update", response_model=InfoMessage, dependencies=[Depends(get_client_id)])
def update_settings(session: SessionDep, new_setting: UpdateSettingBody):
    try:
        add_plugin_config(session=session, key=new_setting.key, value=new_setting.value)
        return InfoMessage(message="Setting updated successfully")
    except Exception as e:
        return InfoMessage(message=f"Failed to update setting: {e}", success=False)


