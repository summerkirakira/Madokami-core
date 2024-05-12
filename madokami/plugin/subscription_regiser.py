from madokami.plugin.subscription import SubscriptionManager


_registered_subscription_managers: dict[str, SubscriptionManager] = {}


def register_subscription_manager(plugin_namespace: str, subscription_manager: SubscriptionManager):
    _registered_subscription_managers[plugin_namespace] = subscription_manager


def get_registered_subscription_managers() -> dict[str, SubscriptionManager]:
    return _registered_subscription_managers
