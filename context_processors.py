from hermes.models import Board

def board_list(request):
    board_list = Board.objects.all().order_by('title')
    context = {'board_list': board_list}
    return context
