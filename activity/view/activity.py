"""
activity views

:author: gexuewen
:date: 2019/12/28
"""
from rest_framework import mixins, generics

from activity.constant.activity_state import CLOSED
from activity.models import Activity, ActivityStudent
from activity.serializers import ActivitySerializer
from util import result_util
from util.pagination import CustomPageNumberPagination


class ActivityViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      generics.GenericAPIView):
    """
    activity view set

    :author: gexuewen
    :date: 2020/01/01
    """
    serializer_class = ActivitySerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        params = self.request.query_params
        query_set = Activity.objects.all()
        activity_state = params.get('activity_state')
        query_set = query_set.filter(state=activity_state)
        student_id = params.get('student_id')
        if student_id:
            activity_student_set = ActivityStudent.objects.filter(student_id=student_id)
            activity_id_list = activity_student_set.values_list('activity_id', flat=True)
            query_set = query_set.filter(id__in=activity_id_list)
        return query_set

    def get(self, request):
        """
        get activity list

        :author: gexuewen
        :date: 2020/01/01
        """
        res = self.list(request)
        return result_util.success(res.data)

    def post(self, request):
        """
        create activity

        :author: gexuewen
        :date: 2020/01/01
        """
        res = self.create(request)
        return result_util.success(res.data)


class ActivityDetailViewSet(mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView):
    """
    activity detail view set

    :author: gexuewen
    :date: 2020/01/02
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'primary_key'

    def put(self, request, primary_key):
        """
        update activity

        :author: gexuewen
        :date: 2020/01/02
        """
        res = self.partial_update(request, primary_key)
        return result_util.success(res.data)

    def delete(self, request, primary_key):
        """
        cancel activity

        :author: gexuewen
        :date: 2020/01/02
        """
        self.destroy(request, primary_key)
        return result_util.success_empty()

    def perform_destroy(self, instance):
        instance.state = CLOSED
        instance.save()
