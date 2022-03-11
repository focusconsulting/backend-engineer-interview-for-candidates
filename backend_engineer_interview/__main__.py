import logging
import os
from backend_engineer_interview.app import (
    create_app,
    get_project_root_dir,
    openapi_filenames,
)

logger = logging.getLogger(__name__)


def main():
    connexion_app = create_app()
    openapi_files = list(
        map(lambda f: os.path.join(get_project_root_dir(), f), openapi_filenames())
    )
    connexion_app.run(
        port=1550,
        use_reloader=True,
        extra_files=openapi_files,
        reloader_type="stat",
    )


main()
