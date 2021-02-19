from django_jsonsaver.server_config import PROJECT_NAME


def constants(request):
    return {'PROJECT_NAME': PROJECT_NAME}
