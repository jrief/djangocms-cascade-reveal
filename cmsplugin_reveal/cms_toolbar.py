# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cms.toolbar_pool import toolbar_pool
from cms.extensions.toolbar import ExtensionToolbar
from .models import RevealExtension


@toolbar_pool.register
class RevealToolbar(ExtensionToolbar):
    model = RevealExtension

    def populate(self):
        current_page_menu = self._setup_extension_toolbar()
        if current_page_menu:
            _, url = self.get_page_extension_admin()
            if url:
                current_page_menu.add_modal_item("Reveal", url=url,
                    disabled=not self.toolbar.edit_mode)
