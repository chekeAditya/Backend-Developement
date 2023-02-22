from django.http import HttpResponse, JsonResponse


def home_page(request):
    print("Aditya")
    friends = [
        "Aditya",
        "Shivom",
        "Kunal",
        "Pawan"
    ]
    return JsonResponse(friends,safe = False)