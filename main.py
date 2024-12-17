import requests
from api.login import login
from api.update_metric_project_settings import update_metric_project_settings

if __name__ == '__main__':
    session = requests.Session()
    token = login(session)
    update_metric_project_settings(session,token)
