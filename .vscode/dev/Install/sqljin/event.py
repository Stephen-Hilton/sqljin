from collections import defaultdict

subscriptions = defaultdict(list)

def subscribe(event_name:str, func) -> None:
    """subscribes a function to a specific event name, allowing it to be triggered by later processes

    Args:
        event_name (str): name of the event
        func ([type]): function to be called in the event the event_name is triggered
    """
    subscriptions[event_name].append(func)


def trigger(event_name:str, data) -> any:
    """triggers execution of all subscriptions for the supplied event_name, with data as parameter

    Args:
        event_name (str): name of the event
        data ([type]): parameters, if any
    """
    if event_name in subscriptions:
        for func in subscriptions[event_name]:
            return func(data)
