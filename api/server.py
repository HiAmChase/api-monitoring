import os
import psutil
import random
import time

from time import perf_counter
from sanic import Sanic
from sanic.response import json, raw
from prometheus_client import CONTENT_TYPE_LATEST

from constants import BaseMetrics, RequestMetaData
from metrics import get_metrics_data, configure_metrics

app = Sanic("Monitoring")

base_metrics = BaseMetrics
metrics_path = "metrics"
relative_path = f"/{metrics_path}"


def rand_sleep():
    value = random.uniform(1, 3)
    time.sleep(value)


@app.listener("before_server_start")
async def setup_metrics(app, _):
    configure_metrics(app, base_metrics)


@app.on_request
async def handle_request(request):
    if request.path != relative_path and request.method != "OPTIONS":
        setattr(app.ctx, RequestMetaData.TIME, perf_counter())


@app.on_response
async def handle_response(request, response):
    if request.path != relative_path and request.method != "OPTIONS":
        if hasattr(app.ctx, RequestMetaData.TIME):
            lat = perf_counter() - getattr(app.ctx, RequestMetaData.TIME)
        else:
            return

        app.ctx.metrics[base_metrics.LATENCY.name].observe(lat)
        app.ctx.metrics[base_metrics.COUNT.name].inc()


@app.route('/')
async def hello(request):
    return json({'message': 'Hello, world!'})


@app.route('/users', methods=['GET'])
async def get_users(request):
    rand_sleep()
    users = [
        {'name': 'John', 'age': 25},
        {'name': 'Jane', 'age': 30}
    ]
    return json(users)


@app.route(metrics_path, methods=["GET"])
async def get_metrics(request):
    _, _, load15 = psutil.getloadavg()
    cpu_usage = (load15/os.cpu_count()) * 100
    ram_usage_pct = psutil.virtual_memory()[2]
    ram_usage_gb = psutil.virtual_memory()[3]/1e9

    app.ctx.metrics[base_metrics.CPU_USAGE.name].set(cpu_usage)
    app.ctx.metrics[base_metrics.RAM_USAGE_PCT.name].set(ram_usage_pct)
    app.ctx.metrics[base_metrics.RAM_USAGE_GB.name].set(ram_usage_gb)

    return raw(get_metrics_data(), content_type=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        auto_reload=True
    )
