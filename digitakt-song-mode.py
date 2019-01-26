#!/usr/bin/env python3

import logging

from controller import SongModeController
from view import SongModeView

if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s][%(levelname)s] %(message)s',
        level=logging.INFO
    )
    controller = SongModeController()
    view = SongModeView(controller)
    view.mainloop()
