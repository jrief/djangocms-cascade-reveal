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
from cmsplugin_cascade.mixins import ImagePropertyMixin
from cmsplugin_cascade.plugin_base import CascadePluginBase
from cmsplugin_cascade.widgets import CascadingSizeWidget
from cmsplugin_cascade.bootstrap3.image import ImageForm


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

    class Media:
        css = {'all': ('reveal/css/admin.css',)}

    def render(self, context, instance, placeholder):
        context = super(RevealMarkDownPlugin, self).render(context, instance, placeholder)
        content = unescape_entities(instance.glossary.get('markdown', ''))
        context['html_content'] = mark_safe(markdown.markdown(content))
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


class RevealImagePlugin(CascadePluginBase):
    name = _("Image")
    module = 'Reveal'
    model_mixins = (ImagePropertyMixin,)
    render_template = 'reveal/image.html'
    require_parent = True
    parent_classes = ('RevealSectionPlugin',)
    allow_children = False
    raw_id_fields = ('image_file',)
    text_enabled = True
    admin_preview = False
    form = ImageForm
    glossary_fields = (
        PartialFormField('image-width',
            CascadingSizeWidget(allowed_units=['px', '%'], required=False),
            label=_("Image Width"),
            help_text=_("Set a fixed image width in pixels."),
        ),
        PartialFormField('image-height',
            CascadingSizeWidget(allowed_units=['px', '%'], required=False),
            label=_("Image Height"),
            help_text=_("Set a fixed height in pixels, or percent relative to the image width."),
        ),
    )

    def render(self, context, instance, placeholder):
        glossary = dict(instance.get_complete_glossary())
        #    extra_styles = tags.pop('extra_styles')
        inline_styles = instance.glossary.get('inline_styles', {})
        # inline_styles.update(extra_styles)
        # instance.glossary['inline_styles'] = inline_styles
        size = (960, 600)
        src = {'size': size, 'crop': False}
        context.update(dict(instance=instance, src=src, placeholder=placeholder))
        return context

plugin_pool.register_plugin(RevealImagePlugin)
