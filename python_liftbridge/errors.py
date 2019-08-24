from functools import wraps

import grpc


class ErrNoSuchStream(Exception):
    def __init__(self, message=None):
        message = message or 'Given stream does not exist'
        super().__init__(message)


class ErrStreamExists(Exception):
    def __init__(self, message=None):
        message = message or 'Given stream already exists'
        super().__init__(message)


class ErrChannelClosed(Exception):
    def __init__(self, message=None):
        message = message or 'Given channel has been closed'
        super().__init__(message)


def handle_rpc_errors(fnc):
    """Decorator to add more context to RPC errors"""

    @wraps(fnc)
    def wrapper(*args, **kwargs):
        try:
            return fnc(*args, **kwargs)

        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise ErrNoSuchStream from None
            elif e.code() == grpc.StatusCode.ALREADY_EXISTS:
                raise ErrStreamExists from None
            elif e.code() == grpc.StatusCode.CANCELLED:
                raise ErrChannelClosed from None
            else:
                print('Failed with {1}: {2}'.format(e.code(), e.details()))
    return wrapper


def handle_rpc_errors_in_generator(fnc):
    """Decorator to add more context to RPC errors"""

    @wraps(fnc)
    def wrapper(*args, **kwargs):
        try:
            yield from fnc(*args, **kwargs)

        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise ErrNoSuchStream from None
            elif e.code() == grpc.StatusCode.ALREADY_EXISTS:
                raise ErrStreamExists from None
            elif e.code() == grpc.StatusCode.CANCELLED:
                raise ErrChannelClosed from None
            else:
                print('Failed with {1}: {2}'.format(e.code(), e.details()))
    return wrapper
