
from typing import Any, Optional, Callable, Iterable, Mapping, Literal, Sized


class Getter:
    """
       Utility class providing strict and controlled access to object attributes and iterable values.

       The `Getter` class defines static methods for safely retrieving attributes or elements
       from objects and iterables. It ensures that if a target is missing or a retrieval operation
       fails, the behavior can be explicitly controlled via custom exceptions or fallback values.

       Features:
           - Fine-grained control over `getattr` behavior via `strict_getattr`
           - Safe item lookup from containers with optional filtering via `strict_getitem`
           - Fail-fast or silent-fallback handling, based on developer intent
           - Designed for use in core libraries, validation pipelines, and meta-programming contexts

       Methods:
           strict_getattr(obj: object, name: str, exception: Exception | None = None) -> Any:
               Retrieves an attribute from an object. Raises the given exception if missing,
               or returns None.

           strict_getitem(__o: Iterable, __value: str, __key_value: str | Any,
                          __filter: Callable[[Any], bool] | None = None,
                          exception: Exception | None = None) -> Any:
               Retrieves a value from an iterable (e.g., dict, list, set), optionally filtering it first.
               If the item is missing or the access fails, raises the given exception or returns None.

       Use Cases:
           - Dynamic property access in frameworks or plugins
           - Validating input structures with fallback/error logic
           - Controlled access in configuration parsing or adapter layers"""

    @staticmethod
    def strict_getattr(__o: object, __name: str, key_value: str| int, __filter: Callable[[Any],bool] | None = None, exception: Exception | None = None ) -> Optional[Any]:

       if not isinstance(__o, Iterable):
           try:
               return getattr(__o, __name)
           except AttributeError:
               if exception:
                   raise exception
               return exception
       return Getter.strict_getitem(__o, __name, key_value, __filter, exception)


    @staticmethod
    def strict_getitem(__o: Iterable, __value: Any, __key_value: str| Any, __filter: Callable[[Any],bool] | None = None, exception: Exception | None = None) -> Optional[Any]:
        """
            Safely retrieves a value from an iterable after optional filtering and existence checking.

            This method allows for controlled access to values within an iterable object (e.g., dict, list, set),
            with optional filtering logic applied beforehand. It first optionally filters the iterable using
            `__filter`, then checks whether `__value` exists in the (filtered) iterable. If it exists, it
            attempts to retrieve a value using `__getitem__` with the key `__key_value`.

            If `__getitem__` fails or the key is not found, a provided `exception` is raised if available.
            Otherwise, the original error is re-raised (if applicable), or `None` is returned.

            Parameters:
                __o (Iterable): The target data structure (e.g., dict, list, set, etc.).
                __value (str): The value to look for in the (filtered) iterable.
                __key_value (str | Any): The key to pass to `__getitem__` if `__value` is found.
                __filter (Callable[[Any], bool], optional): A callable used to filter the original iterable.
                    - For mappings: filters by keys
                    - For sequences/sets: filters by element
                exception (Exception | None, optional): Custom exception to raise on failure.

            Returns:
                Any: The value retrieved via `__getitem__`, or `None` if not found and no exception is provided.

            Raises:
                Exception: If key lookup or retrieval fails and a custom exception is provided.

            Notes:
                - This method distinguishes between `__value` (the presence check key) and `__key_value` (the actual retrieval key).
                - Filtering is non-destructive and only affects the current access logic.
            """

        if callable(__filter):
            if isinstance(__o,Mapping):
                __o = {key:value for key,value  in __o.items() if __filter(key)}
            elif isinstance(__o,(tuple,list,set)):
                __o = filter(__filter,__o)

        if __value in __o:
            if _getitem:=getattr(type(__o),"__getitem__",None):
                    try:
                        return _getitem(__o, __key_value)
                    except Exception as e:
                        if exception:
                            raise exception from e
                        raise e

        if isinstance(exception, Exception):
            raise exception
        return None

    @staticmethod
    def strict_conditional_getitem(__o: Iterable, __value:Any, __key_value: str| int, __filter: Callable[[],bool] | None = None, exception: Exception | None = None) -> Optional[Any]:
        """
            Conditionally retrieves a value from an iterable, based on a runtime boolean predicate.

            If a filter callable (`__filter`) is provided, it is evaluated:
                - If True: proceeds with value lookup using `strict_getitem`.
                - If False: raises the provided exception (if any), or returns it.
            If no filter is provided, lookup is attempted directly.

            Parameters:
                __o (Iterable): The source iterable or mapping-like structure.
                __value (Any): Key or identifier to check for existence in the iterable.
                __key_value (str | int): The key used to retrieve the value via `__getitem__`.
                __filter (Callable[[], bool], optional): A condition function to determine whether lookup is permitted.
                exception (Exception | None, optional): Exception to raise or return if condition fails.

            Returns:
                Optional[Any]: The retrieved value, or the exception object if skipped and no raise occurs.

            Raises:
                Exception: If `__filter` returns False and an Exception is provided."""
        if callable(__filter):
            if __filter():
                return Getter.strict_getitem(__o, __value, __key_value, exception= exception)
            if isinstance(exception, Exception):
                raise exception
            return exception
        return Getter.strict_getitem(__o, __value, __key_value, exception= exception)

    @staticmethod
    def strict_multi_getitem(__o: Sized,validate: Literal["first","second","mid","after mid","before last","last"],exception: Exception | None = None) -> Optional[Any]:
        """
            Dynamically retrieves a positional element from a sized iterable based on a semantic access keyword.

            This method allows for structured access to elements in a sequence using predefined
            semantic positions (e.g., "first", "mid", "before last") instead of hard-coded indexes.
            It ensures safer, more readable, and fallback-compatible index access in varying iterable lengths.

            Parameters:
                __o (Sized): The target iterable structure (list, tuple, set, dict, etc.).
                             If the object is not indexable (e.g., set, dict), it is converted to a list.
                validate (Literal): A semantic keyword indicating the desired position:
                    - "first":        Index 0
                    - "second":       Index 1, requires at least 2 elements
                    - "mid":          Middle index (n // 2)
                    - "after mid":    One after the middle (n // 2 + 1), requires n ≥ 3
                    - "before last":  One before the last, requires n ≥ 2
                    - "last":         Last element, index -1
                exception (Exception | None): Optional fallback exception to raise
                                              if the requested position is invalid
                                              or iterable is too short.

            Returns:
                Any: The value found at the resolved index, or the fallback exception if the condition fails.

            Raises:
                Exception: If the iterable does not meet the required condition for the selected semantic keyword,
                           and a fallback exception is provided.

            Notes:
                - Improves readability compared to magic indexes like [-2], [1], etc.
                - Useful for deterministic element selection in user-facing code or internal APIs.
                - Guaranteed safe access with custom fallback behavior.
            """

        # acces to dataBase
        from Data import getters_constants

        #if __o is set,frozenset,dict change list
        if isinstance(__o, (set,dict,frozenset)):
            __o = list(__o)

        # pure to map
        rule = getters_constants.LookUpTableConstants.Formulas.formulas[validate]
        if rule.condition(len(__o)):
            search_index = rule.index_fn(len(__o))
            return __o[search_index]

        # fallback
        if isinstance(exception, Exception):
            raise exception
        return exception

    @staticmethod
    def strict_multi_getitems(__o: Sized,
        validate: Literal["first to last", "second to last", "first to before last", "mid to last", "first to mid", "mid to before last", "second to before last","second to mid"],
        step : int = 1,
        exception: Exception | None = None) -> Optional[Any]:

        """
            Retrieves a range of items from a sized iterable using semantic slice descriptors.

            This function provides dynamic and readable access to slices within an iterable structure
            using predefined semantic rules such as "first to mid", "second to last", etc.
            It converts non-indexable iterables (e.g., sets, dicts) to a list before slicing.

            Parameters:
                __o (Sized): The target iterable (e.g., list, tuple, set, dict, etc.).
                             If not indexable, it will be converted into a list.
                validate (Literal): Semantic keyword describing the desired range:
                    - "first to last":        All elements
                    - "second to last":       From 2nd element to end
                    - "mid to last":          From middle index to end
                    - "first to mid":         From start to middle (exclusive)
                    - "mid to before last":   From mid to the element before the last
                    - "second to before last":From second element to the one before last
                    - "second to mid":        From second element to mid
                step (int, optional): Step size for slicing. Defaults to 1.
                exception (Exception | None, optional): A custom exception to raise
                                                        if the iterable is too short
                                                        for the requested slice.

            Returns:
                Optional[Any]: A sliced view of the iterable if the slice rule is valid;
                               otherwise returns the exception if provided.

            Raises:
                Exception: If the iterable doesn't meet the required length for the rule,
                           and a fallback exception is provided.

            Notes:
                - Ensures safer, documented access compared to manual index slicing.
                - Handles unordered data structures by converting them to indexable lists.
                - Each slice rule is backed by a condition function to ensure safety.
            """

        # acces to dataBase
        from Data import getters_constants

        # if __o is set,frozenset,dict change list
        if isinstance(__o, (set, dict, frozenset)):
            __o = list(__o)

        # pure to map
        rule = getters_constants.LookUpTableConstants.Formulas.range_formulas[validate]
        if rule.condition(len(__o)):
            return __o[rule.start_fn(len(__o)): rule.stop_fn(len(__o)): step]

        # fallback
        if isinstance(exception, Exception):
            raise exception
        return exception

    @staticmethod
    def strict_get_dict(__o: Mapping, __filter: Callable[[Any], bool] | None = None, exception: Exception | None = None) -> Optional[Mapping[Any, Any]]:
        """
           Returns a filtered mapping from the given source, with optional error handling.

           This method allows selective retrieval of key-value pairs from a mapping-like object (e.g., dict),
           using a custom filter function applied to keys. If the filter is applied and the resulting mapping
           is empty, an exception can be raised or returned as a fallback.

           Parameters:
               __o (Mapping): The original mapping to process.
               __filter (Callable[[Any], bool], optional): A function used to filter keys.
                   If None, the mapping is returned as-is.
               exception (Exception | None, optional): An exception to raise or return
                   if the filtered result is empty.

           Returns:
               Mapping[Any, Any] | Exception | None: The filtered mapping if non-empty.
               If the mapping is empty:
                   - Raises the provided exception if it's an Exception.
                   - Otherwise returns the exception (useful for fallback values).

           Raises:
               Exception: If the filtered mapping is empty and an Exception instance is passed.

           """
        if callable(__filter):
            __o = {k:v for k,v in __o.items() if __filter(k)}

        if not __o:
            if isinstance(exception, Exception):
                raise exception
            return exception
        return __o

