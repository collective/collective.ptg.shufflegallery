from zope.i18nmessageid import MessageFactory
from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.plonetruegallery.browser.views.display import BaseDisplayType
from collective.plonetruegallery.interfaces import IBaseSettings
from zope import schema

_ = MessageFactory('collective.ptg.shufflegallery')

class IShufflegalleryDisplaySettings(IBaseSettings):
    shufflegallery_width = schema.TextLine(
        title=_(u"label_shufflegallery_width",
            default=u"Width of the gallery"),
        default=u"600px")
    shufflegallery_height = schema.TextLine(
        title=_(u"label_shufflegallery_height",
            default=u"Height of the gallery"),
        default=u"350px")
    shufflegallery_textwidth = schema.TextLine(
        title=_(u"label_shufflegallery_textwidth",
            default=u"Width of the (black) text box"),
        default=u"150px")
              
    shufflegallery_style = schema.Choice(
        title=_(u"label_shufflegallery_style",
                default=u"What stylesheet (css file) to use"),
        default="style.css",
        vocabulary=SimpleVocabulary([
            SimpleTerm("style.css", "style.css",
                _(u"label_shufflegallery_style_default",
                    default=u"Default")),
            SimpleTerm("custom_style", "custom_style",
                _(u"label_shufflegallery_style_custom",
                    default=u"Custom css file")
            )
        ]))
    shufflegallery_custom_style = schema.TextLine(
        title=_(u"label_custom_style",
            default=u"Name of Custom css file if you chose that above"),
        default=u"mycustomstyle.css")


class ShufflegalleryDisplayType(BaseDisplayType):
    """ A gallery with a 'phone' feel """
    name = u"shufflegallery"
    schema = IShufflegalleryDisplaySettings
    description = _(u"label_shufflegallery_display_type",
        default=u"shufflegallery")

    def javascript(self):
        return u"""
		<script type="text/javascript" src="++resource++ptg.shufflegallery/jquery.promptu-menu.js"></script>
		<script type="text/javascript">
			$(function(){
				$('ul.promptu-menu').promptumenu({width:%(width)i, height:%(height)i, rows: %(rows)i, columns: %(columns)i, direction: '%(direction)s', pages: true});
			});
		</script>
        """  % {
        'columns': 2,
		'rows': 3,
		'direction': 'horizontal',
		'width': 500,
		'height': 500,
		'duration': self.settings.delay,
		'pages': 'True',
		'inertia': 200
        }

    def css(self):
        base = '%s/++resource++ptg.shufflegallery' % (
            self.portal_url)
        style = '%(base)s/%(style)s' % {
                'base': base,
                'style': self.settings.shufflegallery_style}

        if self.settings.shufflegallery_style == 'custom_style':
            style = '%(url)s/%(style)s' % {
                'url': self.portal_url,
                'style': self.settings.shufflegallery_custom_style}

        return u"""
        <style>
</style>
<link rel="stylesheet" type="text/css" href="%(style)s"/>
""" % {
        'staticFiles': self.staticFiles,
        'style': style
       }
ShufflegallerySettings = createSettingsFactory(ShufflegalleryDisplayType.schema)