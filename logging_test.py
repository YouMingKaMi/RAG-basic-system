import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("abd")

logger.debug("调试废话")
logger.info("正常事件")
logger.warning("有点不对劲")
logger.error("出事了")