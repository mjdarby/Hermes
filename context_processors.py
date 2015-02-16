from hermes.models import Board
from ipware.ip import get_real_ip

def hermes_context_processor(request):
    board_list = Board.objects.all().order_by('title')
    context = {'board_list': board_list,
               'authenticated': request.user.is_authenticated(),
               'user_ip': str(get_real_ip(request))}
    return context
