from madokami.db import init_db, engine
from madokami.models import User, Plugin
from madokami.crud import create_user, add_plugin_config, get_plugin_config, get_plugins, add_plugin, active_plugin, \
    deactivate_plugin
from sqlmodel import Session, select, delete


def test_init_db():
    init_db()


def test_create_user():
    test_user = User(username="test", password="test")
    with Session(engine) as session:
        try:
            user = create_user(session=session, user=test_user)
        except ValueError:
            user = session.exec(select(User).where(User.username == test_user.username)).first()

        assert user.username == "test"
        assert user.password == "test"


def test_plugin_config():
    with Session(engine) as session:
        add_plugin_config(session=session, key="test", value="test")
        add_plugin_config(session=session, key="test", value="test1")
        assert get_plugin_config(session=session, key="test") == "test1"
        assert get_plugin_config(session=session, key="test2") is None


def test_get_plugins():
    with Session(engine) as session:
        plugins = get_plugins(session=session)
        for plugin in plugins:
            session.delete(plugin)
        session.commit()
        assert get_plugins(session=session) == []
        plugin = Plugin(namespace="test.test", is_active=False, name="test", description="test")
        add_plugin(session=session, plugin=plugin)
        assert get_plugins(session=session)[0].namespace == plugin.namespace

        add_plugin(session=session, plugin=plugin)
        assert get_plugins(session=session)[0].namespace == plugin.namespace

        active_plugin(session=session, namespace=plugin.namespace)
        assert get_plugins(session=session)[0].is_active == True

        deactivate_plugin(session=session, namespace=plugin.namespace)
        assert get_plugins(session=session)[0].is_active == False
