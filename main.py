from website import create_app
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

app = create_app()

if __name__ == '__main__':
    logger.debug("starting program")
    app.run(debug=True)
