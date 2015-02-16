from hermes.models import Board
from ipware.ip import get_real_ip

def hermes_context_processor(request):
    board_list = Board.objects.all().order_by('title')
    user_is_superuser = (request.user.is_superuser)
    context = {'hermes_board_list': board_list,
               'hermes_authenticated': user_is_superuser,
               'hermes_user_ip': str(get_real_ip(request))}
    return context
