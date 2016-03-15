# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms import widgets
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.widgets import TextEditorWidget
from django.utils.safestring import mark_safe
from django.utils.text import unescape_entities
try:
    from html.parser import HTMLParser  # py3
except ImportError:
    from HTMLParser import HTMLParser  # py2
import markdown
from cms.plugin_pool import plugin_pool
from cmsplugin_cascade.fields import PartialFormField
from cmsplugin_cascade.plugin_base import CascadePluginBase


class RevealSectionPlugin(CascadePluginBase):
    name = _("Section")
    module = 'Reveal'
    render_template = 'reveal/section.html'
    require_parent = True
    parent_classes = ('RevealSectionPlugin',)
    allow_children = True
    child_classes = None
    alien_child_classes = True
    glossary_fields = (
        PartialFormField('hide',
            widgets.CheckboxInput(),
            label=_("Hide this slide")
        ),
    )

    @classmethod
    def get_identifier(cls, instance):
        identifier = super(RevealSectionPlugin, cls).get_identifier(instance)
        if instance.glossary.get('hide'):
            return format_html('{} hidden', identifier)
        return identifier

plugin_pool.register_plugin(RevealSectionPlugin)


class RevealFragmentPlugin(CascadePluginBase):
    name = _("Fragment")
    module = 'Reveal'
    render_template = 'reveal/fragment.html'
    require_parent = True
    parent_classes = ('RevealSectionPlugin',)
    allow_children = True
    child_classes = None
    alien_child_classes = True

plugin_pool.register_plugin(RevealFragmentPlugin)


class RevealMarkDownPlugin(CascadePluginBase):
    name = _("Mark Down")
    module = 'Reveal'
    render_template = 'reveal/mark-down.html'
    require_parent = True
    parent_classes = ('RevealSectionPlugin',)
    allow_children = True
    child_classes = None
    alien_child_classes = True
    glossary_fields = (
        PartialFormField('markdown',
            widgets.Textarea(attrs={'cols': 150, 'rows': 30, 'style': 'width: 100%;'}),
            label=_("Enter text in markdown syntax")
        ),
    )

    def render(self, context, instance, placeholder):
        context = super(RevealMarkDownPlugin, self).render(context, instance, placeholder)
        content = unescape_entities(instance.glossary.get('markdown', ''))
        context['html_content'] = mark_safe(markdown.markdown(content))
        print context['html_content']
        return context

plugin_pool.register_plugin(RevealMarkDownPlugin)


class RevealSpeakerNotePlugin(CascadePluginBase):
    name = _("Speaker Note")
    module = 'Reveal'
    render_template = 'reveal/speaker-note.html'
    require_parent = True
    parent_classes = ('RevealSectionPlugin',)
    allow_children = False
    child_classes = ()
    html_parser = HTMLParser()

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            notes = self.html_parser.unescape(obj.glossary.get('notes', ''))
            obj.glossary.update(notes=notes)
        # define glossary fields on the fly, because the TextEditorWidget requires the plugin_pk
        text_editor_widget = TextEditorWidget(installed_plugins=[], pk=self.parent.pk,
            placeholder=self.parent.placeholder, plugin_language=self.parent.language)
        kwargs['glossary_fields'] = (
            PartialFormField('notes', text_editor_widget, label=_("Speaker Notes")),
        )
        return super(RevealSpeakerNotePlugin, self).get_form(request, obj, **kwargs)

plugin_pool.register_plugin(RevealSpeakerNotePlugin)
