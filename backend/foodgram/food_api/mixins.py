from rest_framework import mixins, viewsets


class ListDetailViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    '''Viewset for endpoints which contain only
    List and Detail representations.'''
    pass


class GetObjectsViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    '''
    Viewset for represent model objects without
    create, update, delete abilities.
    '''
    pass
