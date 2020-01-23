"""
Course API Views
"""

from opaque_keys.edx.keys import CourseKey
from rest_framework.generics import RetrieveAPIView

from lms.djangoapps.course_api.api import course_detail
from openedx.core.lib.api.view_utils import DeveloperErrorViewMixin, view_auth_classes

from .serializers import CourseInfoSerializer


@view_auth_classes(is_authenticated=True)
class CoursewareInformation(DeveloperErrorViewMixin, RetrieveAPIView):
    """
    **Use Cases**

        Request details for a course

    **Example Requests**

        GET /api/courseware/course/{course_key}

    **Response Values**

        Body consists of the following fields:

        * effort: A textual description of the weekly hours of effort expected
            in the course.
        * end: Date the course ends, in ISO 8601 notation
        * enrollment_end: Date enrollment ends, in ISO 8601 notation
        * enrollment_start: Date enrollment begins, in ISO 8601 notation
        * id: A unique identifier of the course; a serialized representation
            of the opaque key identifying the course.
        * media: An object that contains named media items.  Included here:
            * course_image: An image to show for the course.  Represented
              as an object with the following fields:
                * uri: The location of the image
        * name: Name of the course
        * number: Catalog number of the course
        * org: Name of the organization that owns the course
        * short_description: A textual description of the course
        * start: Date the course begins, in ISO 8601 notation
        * start_display: Readably formatted start of the course
        * start_type: Hint describing how `start_display` is set. One of:
            * `"string"`: manually set by the course author
            * `"timestamp"`: generated from the `start` timestamp
            * `"empty"`: no start date is specified
        * pacing: Course pacing. Possible values: instructor, self
        * tabs: Course tabs
        * enrollment: Enrollment status of requested user (or authenticated user)

    **Parameters:**

        requested_fields (optional) comma separated list:
            If set, then only those fields will be returned.

    **Returns**

        * 200 on success with above fields.
        * 400 if an invalid parameter was sent or the username was not provided
          for an authenticated request.
        * 403 if a user who does not have permission to masquerade as
          another user specifies a username other than their own.
        * 404 if the course is not available or cannot be seen.
    """

    serializer_class = CourseInfoSerializer

    def get_object(self):
        """
        Return the requested course object, if the user has appropriate
        permissions.
        """
        return course_detail(
            self.request,
            self.request.user.username,
            CourseKey.from_string(self.kwargs['course_key_string']),
        )

    def get_serializer_context(self):
        """
        Return extra context to be used by the serializer class.
        """
        context = super().get_serializer_context()
        context['requested_fields'] = self.request.GET.get('requested_fields', None)
        return context
