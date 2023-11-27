from typing import Any, Mapping

from rest_framework.renderers import BaseRenderer

class CSVRenderer(BaseRenderer):
    media_type: str
    format: str
    charset: str | None
    render_style: str
    def render(
        self, data: Any,
        accepted_media_type: str | None = ...,
        renderer_context: Mapping[str, Any] | None = ...,
        writer_opts: Mapping[str, Any] | None = ...,
    ) -> Any: ...
