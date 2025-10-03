import sys
import logging
import coloredlogs

def setup():
    format_string = "[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s"
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)

    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("disnake").setLevel(logging.WARNING)

    coloredlogs.DEFAULT_LEVEL_STYLES = {
        **coloredlogs.DEFAULT_LEVEL_STYLES,
        "trace": {"color": 246},
        "critical": {"background": "red"},
        "debug": coloredlogs.DEFAULT_LEVEL_STYLES["debug"],
    }

    coloredlogs.DEFAULT_LOG_FORMAT = format_string

    coloredlogs.install(
        level=logging.INFO, stream=sys.stdout
    )