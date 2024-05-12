from .models import Subscription
from abc import abstractmethod
from sqlmodel import Session


class SubscriptionManager:

    @abstractmethod
    def subscribe(self, session: Session, subscription: Subscription):
        ...

    @abstractmethod
    def unsubscribe(self, session: Session, subscription_id: str):
        ...

    @abstractmethod
    def get_subscription(self, session: Session, subscription_id: str):
        ...

    @abstractmethod
    def get_subscriptions(self, session: Session) -> list[Subscription]:
        ...
