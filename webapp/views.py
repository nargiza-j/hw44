from django.shortcuts import render
from webapp.check import Check
# Create your views here.


secret_numbers = Check.generate_numbers(4)
print(secret_numbers)


def index_view(request):
    if request.method == "GET":
        return render(request, 'index.html')
    elif request.method == "POST":
        global secret_numbers
        context = {}
        try:
            user_numbers = list(map(int, request.POST.get('numbers')))
            check = Check(user_numbers, secret_numbers)
            error = check.validation()
            if error:
                context = {'message': error}
                return render(request, 'index.html', context)
            else:
                result = check.get_result()
                check.add_history(result)
                if result == "Win":
                    secret_numbers = Check.generate_numbers(4)
                    print(secret_numbers)
                context = {'message': result}
                return render(request, 'index.html', context)
        except ValueError:
            context = {'message': "The value should be integers"}
            return render(request, 'index.html', context)


def history_view(request):
    value = Check.get_history()
    context = {'history': value}
    return render(request, 'history.html', context)
