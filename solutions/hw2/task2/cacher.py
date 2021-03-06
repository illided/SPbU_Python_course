from typing import Any, Tuple, Callable
from collections import OrderedDict
import functools


def FunctionCacher(function=None, *, maximum_num_of_caches: int = 0):
    if function:
        return _FunctionCallsCacher(function, maximum_num_of_caches=maximum_num_of_caches)

    def wrapper(func):
        return _FunctionCallsCacher(func, maximum_num_of_caches=maximum_num_of_caches)

    return wrapper


class FunctionCallArgumentsCache:
    nameless_args: Tuple
    named_args: frozenset

    def __init__(self, args: Tuple, kwargs: dict):
        self.nameless_args = args
        self.named_args = frozenset(sorted(kwargs.items()))

    def __hash__(self):
        return hash((self.named_args, self.nameless_args))

    def __eq__(self, other):
        if not isinstance(other, FunctionCallArgumentsCache):
            raise NotImplementedError("Can't compare function call argument cache to other objects")
        return self.named_args == other.named_args and self.nameless_args == other.nameless_args


class _FunctionCallsCacher:
    function: Callable
    maximum_num_of_caches: int
    is_caching_enabled: bool
    cache: "OrderedDict[FunctionCallArgumentsCache, Any]"

    def __init__(self, function=None, *, maximum_num_of_caches):
        self.function = function

        self.maximum_num_of_caches = maximum_num_of_caches
        self.is_caching_enabled = self.check_for_working_statement()

        self.cache = OrderedDict()

        functools.update_wrapper(self, function)

    def check_for_working_statement(self) -> bool:
        if self.maximum_num_of_caches < 0:
            raise TypeError("Maximum number of caches can't be negative")
        elif self.maximum_num_of_caches == 0:
            return False
        else:
            return True

    def __call__(self, *args, **kwargs):
        if self.is_such_call_cached(args, kwargs):
            return self.get_cached_result(*args, **kwargs)

        result = self.function(*args, **kwargs)
        if self.is_caching_enabled:
            self.delete_oldest_cached_call_if_necessary()
            self.add_to_cache(args, kwargs, result)
        return result

    def delete_oldest_cached_call_if_necessary(self):
        if self.is_cache_full():
            self.cache.popitem(last=False)

    def add_to_cache(self, args: Tuple, kwargs: dict, result):
        self.cache[FunctionCallArgumentsCache(args, kwargs)] = result

    def is_cache_full(self) -> bool:
        return len(self.cache) == self.maximum_num_of_caches

    def get_cached_result(self, *args, **kwargs):
        if not self.is_such_call_cached(args, kwargs):
            raise ValueError("Call with such arguments is not cached")
        return self.cache[FunctionCallArgumentsCache(args, kwargs)]

    def is_such_call_cached(self, args, kwargs) -> bool:
        return FunctionCallArgumentsCache(args, kwargs) in self.cache

    def clear_cache(self):
        self.cache.clear()
