import requests
from api.login import login
from api.update_metric_project_settings import update_metric_project_settings
from api.projectkeywords import update_project_keywords
from api.systemframework import get_projects_in_system
from config import project_keywords_settings, username,systemID

if __name__ == '__main__':
    session = requests.Session()
    token = login(session)

    for project_name in get_projects_in_system(session,token,systemID,"metric"):
        update_metric_project_settings(session, token, project_name, username)
    for project_name in get_projects_in_system(session, token, systemID, "alert"):
        update_project_keywords(session,token,project_name,project_keywords_settings)
