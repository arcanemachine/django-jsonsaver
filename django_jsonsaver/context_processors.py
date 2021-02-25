from django_jsonsaver import server_config as sc


def constants(request):
    return {'PROJECT_NAME': sc.PROJECT_NAME,
            'BACKEND_SERVER_URL': sc.BACKEND_SERVER_URL}
