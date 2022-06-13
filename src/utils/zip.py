from fastapi.responses import StreamingResponse
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO
import os

from settings import settings

directory = settings.STATIC_DIR


def zipfile(filenames):
    s = BytesIO()
    zf = ZipFile(s, "w")

    for fpath in filenames:
        zf.write(os.path.join(directory, fpath), fpath)
    zf.close()

    return StreamingResponse(
        iter([s.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment; filename=images.zip"},
    )
