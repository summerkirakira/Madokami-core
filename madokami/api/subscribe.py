from fastapi import APIRouter, HTTPException, Depends
from .models import SubscriptionsAllResponse, AddSubscriptionBody, InfoMessage, RemoveSubscriptionBody
from madokami.drivers.deps import SessionDep, get_client_id
from madokami.plugin.subscription import SubscriptionManager
from sqlmodel import Session


subscribe_router = APIRouter(tags=["Subscribe"])


def convert_subscribe_to_record(session: Session, namespace: str, subscription: SubscriptionManager) -> SubscriptionsAllResponse.SubscriptionRecord:
    subscriptions = subscription.get_subscriptions(session=session)
    return SubscriptionsAllResponse.SubscriptionRecord(
        namespace=namespace,
        subscriptions=[SubscriptionsAllResponse.SubscriptionRecord.Subscription(
            id=subscription.id,
            name=subscription.name,
            data=subscription.data
        ) for subscription in subscriptions]
    )


@subscribe_router.get("/subscribe/all", response_model=SubscriptionsAllResponse, dependencies=[Depends(get_client_id)])
def get_downloads(session: SessionDep):
    from madokami import get_app
    app = get_app()
    subscription_managers = app.plugin_manager.subscription_managers
    try:
        return SubscriptionsAllResponse(
            data=[convert_subscribe_to_record(session=session, namespace=namespace, subscription=manager) for namespace, manager in subscription_managers.items()]
        )
    except Exception as e:
        return SubscriptionsAllResponse(message=f'Failed to retrieve subscriptions: {e}', success=False)


@subscribe_router.post("/subscribe/add", response_model=InfoMessage, dependencies=[Depends(get_client_id)])
def add_subscription(subscription: AddSubscriptionBody, session: SessionDep):
    from madokami import get_app
    app = get_app()
    subscription_manager = app.plugin_manager.subscription_managers.get(subscription.namespace)
    if not subscription_manager:
        raise HTTPException(status_code=404, detail="Subscription manager not found")
    try:
        subscription_manager.subscribe(session=session, subscription=subscription)
        return InfoMessage(message="Subscription added successfully")
    except Exception as e:
        return InfoMessage(message=f"Failed to add subscription: {e}", success=False)


@subscribe_router.post("/subscribe/remove", response_model=InfoMessage, dependencies=[Depends(get_client_id)])
def remove_subscription(subscription: RemoveSubscriptionBody, session: SessionDep):
    from madokami import get_app
    app = get_app()
    subscription_manager = app.plugin_manager.subscription_managers.get(subscription.namespace)
    if not subscription_manager:
        raise HTTPException(status_code=404, detail="Subscription manager not found")
    try:
        subscription_manager.unsubscribe(session=session, subscription_id=subscription.id)
        return InfoMessage(message="Subscription removed successfully")
    except Exception as e:
        return InfoMessage(message=f"Failed to remove subscription: {e}", success=False)

