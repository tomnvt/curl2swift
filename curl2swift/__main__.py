# __main__.py
from curl2swift.handle_options import handle_options
from curl2swift.run_main_processing import run_main_processing
import curl2swift.utils.logger as logger


def main():
    logger.setup()
    handle_options()
    run_main_processing()


if __name__ == "__main__":
    main()
