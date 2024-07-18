import pkg_resources
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Scope, String
from django.template import Context, Template
from django.views.decorators.csrf import csrf_exempt
from xblockutils.resources import ResourceLoader
from xblock.scorable import ScorableXBlockMixin
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from webob import Response
import json
from .utils import _


class FeedbackXBlock(XBlock):
    
    icon_class = String(
        default="problem",
        scope=Scope.settings,
    )
    
    display_name = String(
        display_name=_("Display Name"),
        default=_("FEEDBACK"),
        scope=Scope.settings,
        help=_("This name appears in the horizontal navigation at the top of the page.")
    )
    comments = String(
        display_name=_("Review"),
        default=_("Give your review here!"),
        scope=Scope.content,
        help=_("Type your review")
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    @method_decorator(csrf_exempt, name='dispatch')
    def student_view(self, context=None):
        """
        The primary view of the FeedbackXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("templates/html/feedbackxblock.html")
        frag = Fragment(html)
        frag.add_css(self.resource_string("static/css/feedbackxblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/feedbackxblock.js"))
        frag.initialize_js('submitFeedback')
        return frag

    @method_decorator(csrf_exempt, name='dispatch')
    def studio_view(self, context=None):
        """
        The secondary view of the XBlock, shown to teachers
        when editing the XBlock.
        """
        html = self.resource_string(
            'templates/html/studio_view.html',
        )
        frag = Fragment(html.format(display_name=self.display_name))
        frag.add_css(self.resource_string("static/css/studio_view.css"))
        frag.add_javascript(self.resource_string("static/js/src/studio_view.js"))
        frag.initialize_js('feedbackXBlockInitEdit')
        return frag

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        self.display_name = data.get('display_name')

        return Response(json_body={
            'result': 'success'
        })

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("FeedbackXBlock",
             """<feedbackxblock/>
             """),
            ("Multiple FeedbackXBlock",
             """<vertical_demo>
                <feedbackxblock/>
                <feedbackxblock/>
                <feedbackxblock/>
                </vertical_demo>
             """),
        ]
