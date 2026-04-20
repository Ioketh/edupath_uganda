# edupath/monkey_patch.py
import sys
from django.template import context
from django.template.context import RequestContext

if sys.version_info >= (3, 14):
    # Fix base Context copying
    _orig_context_copy = context.Context.__copy__

    def _patched_context_copy(self):
        new = context.Context(self.dicts, autoescape=self.autoescape)
        # Copy all extra attributes that Django might rely on
        for attr in ('use_l10n', 'use_tz', 'render_context', 'current_app'):
            if hasattr(self, attr):
                setattr(new, attr, getattr(self, attr))
        return new

    context.Context.__copy__ = _patched_context_copy

    # Fix RequestContext copying
    _orig_request_copy = RequestContext.__copy__

    def _patched_request_copy(self):
        new = RequestContext(
            self.request,
            self.dicts,
            processors=self.processors,
            current_app=getattr(self, 'current_app', None),
            use_l10n=getattr(self, 'use_l10n', None),
            use_tz=getattr(self, 'use_tz', None)
        )
        if hasattr(self, 'render_context'):
            new.render_context = self.render_context
        return new

    RequestContext.__copy__ = _patched_request_copy