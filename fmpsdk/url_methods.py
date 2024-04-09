import logging
import typing
import datetime as dt

import requests

from .settings import (
    INDUSTRY_VALUES,
    PERIOD_VALUES,
    SECTOR_VALUES,
    SERIES_TYPE_VALUES,
    STATISTICS_TYPE_VALUES,
    TECHNICAL_INDICATORS_TIME_DELTA_VALUES,
    TIME_DELTA_VALUES,
    BASE_URL_v3,
    BASE_URL_v4,
)

CONNECT_TIMEOUT = 5
READ_TIMEOUT = 30

# Disable excessive DEBUG messages.
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def __return_json_v3(
    path: str, query_vars: typing.Dict
) -> typing.Optional[typing.List]:
    """
    Query URL for JSON response for v3 of FMP API.

    :param path: Path after TLD of URL
    :param query_vars: Dictionary of query values (after "?" of URL)
    :return: JSON response
    """
    url = f"{BASE_URL_v3}{path}"
    return_var = None
    try:
        response = requests.get(
            url, params=query_vars, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
        )
        if len(response.content) > 0:
            return_var = response.json()

        if len(response.content) == 0 or (
            isinstance(return_var, dict) and len(return_var.keys()) == 0
        ):
            logging.warning("Response appears to have no data.  Returning empty List.")
            return_var = []

    except requests.Timeout:
        logging.error(f"Connection to {url} timed out.")
    except requests.ConnectionError:
        logging.error(
            f"Connection to {url} failed:  DNS failure, refused connection or some other connection related "
            f"issue."
        )
    except requests.TooManyRedirects:
        logging.error(
            f"Request to {url} exceeds the maximum number of predefined redirections."
        )
    except Exception as e:
        logging.error(
            f"A requests exception has occurred that we have not yet detailed an 'except' clause for.  "
            f"Error: {e}"
        )

    return return_var


def __return_json_v4(
    path: str, query_vars: typing.Dict
) -> typing.Optional[typing.List]:
    """
    Query URL for JSON response for v4 of FMP API.

    :param path: Path after TLD of URL
    :param query_vars: Dictionary of query values (after "?" of URL)
    :return: JSON response
    """
    url = f"{BASE_URL_v4}{path}"
    return_var = None
    try:
        response = requests.get(
            url, params=query_vars, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
        )
        if len(response.content) > 0:
            return_var = response.json()

        if len(response.content) == 0 or (
            isinstance(return_var, dict) and len(return_var.keys()) == 0
        ):
            logging.warning("Response appears to have no data.  Returning empty List.")
            return_var = []

    except requests.Timeout:
        logging.error(f"Connection to {url} timed out.")
    except requests.ConnectionError:
        logging.error(
            f"Connection to {url} failed:  DNS failure, refused connection or some other connection related "
            f"issue."
        )
    except requests.TooManyRedirects:
        logging.error(
            f"Request to {url} exceeds the maximum number of predefined redirections."
        )
    except Exception as e:
        logging.error(
            f"A requests exception has occurred that we have not yet detailed an 'except' clause for.  "
            f"Error: {e}"
        )
    return return_var


def __validate_period(value: str) -> str:
    """
    Check to see if passed string is in the list of possible time periods.
    :param value: Period name.
    :return: Passed value or No Return
    """
    valid_values = PERIOD_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(f"Invalid period value: {value}.  Valid options: {valid_values}")


def __validate_sector(value: str) -> str:
    """
    Check to see if passed string is in the list of possible Sectors.
    :param value: Sector name.
    :return: Passed value or No Return
    """
    valid_values = SECTOR_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(f"Invalid sector value: {value}.  Valid options: {valid_values}")


def __validate_industry(value: str) -> str:
    """
    Check to see if passed string is in the list of possible Industries.
    :param value: Industry name.
    :return: Passed value or No Return
    """
    valid_values = INDUSTRY_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(
            f"Invalid industry value: {value}.  Valid options: {valid_values}"
        )


def __validate_time_delta(value: str) -> str:
    """
    Check to see if passed string is in the list of possible Time Deltas.
    :param value: Time Delta name.
    :return: Passed value or No Return
    """
    valid_values = TIME_DELTA_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(
            f"Invalid time_delta value: {value}.  Valid options: {valid_values}"
        )


def __validate_series_type(value: str) -> str:
    """
    Check to see if passed string is in the list of possible Series Type.
    :param value: Series Type name.
    :return: Passed value or No Return
    """
    valid_values = SERIES_TYPE_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(
            f"Invalid series_type value: {value}.  Valid options: {valid_values}"
        )


def __validate_statistics_type(value: str) -> str:
    """
    Check to see if passed string is in the list of possible Statistics Type.
    :param value: Statistics Type name.
    :return: Passed value or No Return
    """
    valid_values = STATISTICS_TYPE_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(
            f"Invalid statistics_type value: {value}.  Valid options: {valid_values}"
        )


def __validate_technical_indicators_time_delta(value: str) -> str:
    """Exactly like set_time_delta() method but adds 'daily' as an option.
    :param value: Indicators Time Delta name.
    :return: Passed value or No Return
    """
    valid_values = TECHNICAL_INDICATORS_TIME_DELTA_VALUES
    if value in valid_values:
        return value
    else:
        logging.error(
            f"Invalid time_delta value: {value}.  Valid options: {valid_values}"
        )


def __query_dates_generator(interval, from_date=None, to_date=None):
    """
    A generator that yields a dictionary {"from", "to"} covering the range from start_date to end_date.
    Each range is interval apart, except the remainder at the end. If from_date or to_date date is not provided,
    function returns the same date(s) and/or None.

    :param from_date: The start date as a datetime.date object or str (YYYY-MM-DD).
    :param to_date: The end date as a datetime.date object or str (YYYY-MM-DD).
    :param interval: Number of days for each date range segment.
    :return: Yields (from_date, to_date) tuples as str (YYYY-MM-DD).
    """
    query_dates = {}

    if isinstance(from_date, str):
        from_date = dt.datetime.strptime(from_date, '%Y-%m-%d').date()
    if isinstance(to_date, str):
        to_date = dt.datetime.strptime(to_date, '%Y-%m-%d').date()

    if from_date is None or to_date is None:
        if from_date:
            query_dates["from"] = from_date.strftime('%Y-%m-%d')
        if to_date:
            query_dates["to"] = to_date.strftime('%Y-%m-%d')
        yield query_dates
        return
    
    current_from_date = from_date
    while current_from_date < to_date:
        current_to_date = min(current_from_date + dt.timedelta(days=interval), to_date)
        query_dates["from"] = current_from_date.strftime('%Y-%m-%d')
        query_dates["to"] = current_to_date.strftime('%Y-%m-%d')
        yield query_dates
        current_from_date = current_to_date + dt.timedelta(days=1)

def __query_by_date_range(interval, path, query_vars, from_date=None, to_date=None, depth=0):
    """Queries API by date range broken into equal length + remainder intervals. If a limit
    is provided in query_vars and returned by api, function will call itself recursively to
    divide and retry query

    Args:
        from_date (_type_): The start date as a datetime.date object or str (YYYY-MM-DD).
        to_date (_type_): The start date as a datetime.date object or str (YYYY-MM-DD).
        interval (int): number of days to subdivide query into
        path (str): url path of api
        query_vars (Dict[str,str...]): vars to include in query
        depth (int, optional): Function recursion depth. Defaults to 0.

    Returns:
        List[Dict]: query data
    """
    results = []
    for query_dates in __query_dates_generator(interval, from_date, to_date):
        query_vars = query_vars | query_dates
        query_data = __return_json_v4(path=path, query_vars=query_vars)
        query_return_len = len(query_data)
        if 'limit' in query_vars and query_return_len >= query_vars['limit'] and depth < 5:
            logging.info(
                f"Query depth {depth} dates: {query_dates} "
                f"returned api limit {query_vars['limit']} results, retrying with shorter date range"
            )
            query_data = __query_by_date_range(interval/2, path, query_vars, query_dates["from"], query_dates["to"], depth+1)

        logging.debug(
            f"Query depth {depth} dates: {query_dates} "
            f"returned {query_return_len} results"
        )
        results.extend(query_data)
    
    return results