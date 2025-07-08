import multiprocessing

max_requests = 1000
max_requests_jitter = 50
log_file = "-"
bind = "0.0.0.0:8000"
# Optimized worker count: Use CPU cores + 1 for I/O bound FastAPI apps
workers = min(multiprocessing.cpu_count() + 1, 4)  # Cap at 4 workers max

worker_class = "my_uvicorn_worker.MyUvicornWorker"

# Reduced timeout for faster startup/shutdown
timeout = 120
graceful_timeout = 30
keepalive = 5
