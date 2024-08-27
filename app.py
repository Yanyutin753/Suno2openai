import uvicorn

from log.log import initialize_json_file
from util.config import update_version, SAVE_DATA
from util.utils import update_clerk_js_version

log_config = uvicorn.config.LOGGING_CONFIG
default_format = "%(asctime)s | %(levelname)s | %(message)s"
access_format = r'%(asctime)s | %(levelname)s | %(client_addr)s: %(request_line)s %(status_code)s'

log_config["formatters"]["default"]["fmt"] = default_format
log_config["formatters"]["access"]["fmt"] = access_format

if SAVE_DATA:
    initialize_json_file()

update_version(update_clerk_js_version())
uvicorn.run("main:app", host="0.0.0.0", port=8000)
