from enum import Enum


class RequestMetaData:
    TIME = "__START_TIME__"
    ROUTER = "__ROUTER_URI__"


class BaseMetrics(Enum):
    LATENCY = "sanic_request_latency_sec"
    COUNT = "sanic_request_count"
    CPU_USAGE = "cpu_usage"
    RAM_USAGE_PCT = "ram_usage_pct"
    RAM_USAGE_GB = "ram_usage_gb"
