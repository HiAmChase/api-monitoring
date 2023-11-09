from prometheus_client import Counter, Histogram, Gauge
from prometheus_client.core import REGISTRY as registry
from prometheus_client.exposition import generate_latest


def configure_metrics(app, metrics=None):
    app.ctx.metrics = {}

    app.ctx.metrics[metrics.COUNT.name] = Counter(
        metrics.COUNT.value,
        "Sanic Request Count",
    )

    app.ctx.metrics[metrics.LATENCY.name] = Histogram(
        metrics.LATENCY.value,
        "Sanic Request Latency Histogram",
    )

    app.ctx.metrics[metrics.CPU_USAGE.name] = Gauge(
        metrics.CPU_USAGE.value,
        "CPU Usage",
    )
    app.ctx.metrics[metrics.RAM_USAGE_PCT.name] = Gauge(
        metrics.RAM_USAGE_PCT.value,
        "Ram Memory Usage (%)",
    )
    app.ctx.metrics[metrics.RAM_USAGE_GB.name] = Gauge(
        metrics.RAM_USAGE_GB.value,
        "Ram Memory Usage (GB)",
    )


def get_metrics_data():
    data = generate_latest(registry)
    return data
