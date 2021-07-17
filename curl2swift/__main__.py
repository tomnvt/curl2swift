# __main__.py
import sys

from curl2swift.handle_options import handle_options
from curl2swift.generate_output import generate_ouput
import curl2swift.utils.logger as logger


def main(user_input=None, is_windowed=True, should_make_request=False):
    if len(sys.argv) == 1:
        from curl2swift.layers.presentation.application import Application

        Application.run()

    logger.setup()
    handle_options()
    return generate_ouput(user_input, is_windowed=is_windowed, should_make_request=should_make_request)


if __name__ == "__main__":
    main()
