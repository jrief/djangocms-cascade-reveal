# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from jsonfield.fields import JSONField
from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool


class RevealExtension(PageExtension):
    options = JSONField(blank=True, default={})

    class Meta:
        db_table = 'cmsplugin_cascade_reveal'
        verbose_name = "Reveal Option"
        verbose_name_plural = "Reveal Options"

    def __str__(self):
        return PageExtension.__str__(self)

extension_pool.register(RevealExtension)
