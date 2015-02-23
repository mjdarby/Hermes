from hermes.models import Board
from ipware.ip import get_real_ip
from hermes.settings import get_hermes_setting

def hermes_context_processor(request):
    board_list = Board.objects.all().order_by('title')
    user_is_superuser = (request.user.is_superuser)
    captcha_sitekey = get_hermes_setting('recaptcha_sitekey')
    context = {'hermes_board_list': board_list,
               'hermes_authenticated': user_is_superuser,
               'hermes_user_ip': str(get_real_ip(request)),
               'hermes_recaptcha_sitekey': captcha_sitekey}
    return context
