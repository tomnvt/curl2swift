# __main__.py
import sys

from curl2swift.handle_options import handle_options
from curl2swift.generate_output import generate_ouput
import curl2swift.utils.logger as logger


def main():
    if len(sys.argv) == 1:
        from curl2swift.layers.presentation.application import Application

        Application.run()

    logger.setup()
    handle_options()
    generate_ouput(should_make_request=True)


if __name__ == "__main__":
    main()
