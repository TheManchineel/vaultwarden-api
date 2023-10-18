from requests import Session, Response
from bs4 import BeautifulSoup
from uuid import UUID
from datetime import datetime
from .models import User, Organization


def bytesize(size: str) -> int:
    units = {
        "bytes": 1,
        "KB": 2**10,
        "MB": 2**20,
        "GB": 2**30,
        "TB": 2**40,
    }  # this is not the SI definition, but it's what VW uses
    (dim, unit) = size.split(" ")
    return int(float(dim) * units[unit])


class VaultwardenAPI:
    def authenticate(self):
        response = self.session.post(self.url, data={"token": self.token})
        response.raise_for_status()

    def __init__(self, url: str, token: str):
        self.url = url + "/admin"
        self.token = token
        self.session = Session()
        self.authenticate()

    def get_page(self, path: str) -> BeautifulSoup | None:
        response = self.session.get(f"{self.url}/{path}")
        match response.status_code:
            case 401:
                self.authenticate()
                return self.get_page(path)
            case 200:
                return BeautifulSoup(response.text, "html.parser")
            case _:
                response.raise_for_status()

    def get_page_raw(self, path: str) -> Response | None:
        response = self.session.get(f"{self.url}/{path}")
        match response.status_code:
            case 401:
                self.authenticate()
                return self.get_page_raw(path)
            case 200:
                return response
            case _:
                response.raise_for_status()

    def post_data(self, path: str, data: dict) -> Response | None:
        response = self.session.post(f"{self.url}/{path}", data=data)
        match response.status_code:
            case 401:
                self.authenticate()
                return self.post_data(path, data)
            case 200:
                return response
            case _:
                response.raise_for_status()

    def get_users(self) -> list[User]:
        page = self.get_page("users/overview")
        if page is None:
            return []
        user_rows = page.select("table#users-table tbody tr")
        users = []

        for row in user_rows:
            columns = row.find_all("td")
            name = columns[0].find("strong").text
            email = columns[6].select_one("span")["data-vw-user-email"]
            created_at = datetime.strptime(columns[1].select_one("span").text, "%Y-%m-%d %H:%M:%S %Z")
            last_active = datetime.strptime(columns[2].select_one("span").text, "%Y-%m-%d %H:%M:%S %Z")
            entries_count = int(columns[3].select_one("span").text)

            attachments_info = list(columns[4].children)
            attachments_count = attachments_size = 0

            for i in attachments_info:
                match i:
                    case "\n":
                        continue
                    case _:
                        match (kv := list(map(lambda html: html.text, i.children)))[0]:
                            case "Amount:":
                                attachments_count = int(kv[1].strip())
                            case "Size:":
                                attachments_size = bytesize(kv[1].strip())
                            case _:
                                continue

            organizations = {
                UUID(org["data-vw-org-uuid"]): org["data-vw-org-name"] for org in columns[5].select("button")
            }

            users.append(
                User(
                    name=name,
                    email=email,
                    created_at=created_at,
                    last_active=last_active,
                    entries_count=entries_count,
                    attachments_count=attachments_count,
                    attachments_size=attachments_size,
                    organizations=organizations,
                )
            )

        return users

    def get_organizations(self) -> list[Organization]:
        page = self.get_page("organizations/overview")

        if page is None:
            return []

        org_rows = page.select("table#orgs-table tbody tr")
        orgs = []

        for row in org_rows:
            columns = row.find_all("td")
            name = columns[0].find("strong").text
            email = columns[0].select_one("span").text.replace("(", "").replace(")", "")
            user_count = int(columns[1].select_one("span").text)
            entries_count = int(columns[2].select_one("span").text)

            attachments_info = list(columns[3].children)
            attachments_count = attachments_size = 0

            for i in attachments_info:
                match i:
                    case "\n":
                        continue
                    case _:
                        match (kv := list(map(lambda html: html.text, i.children)))[0]:
                            case "Amount:":
                                attachments_count = int(kv[1].strip())
                            case "Size:":
                                attachments_size = bytesize(kv[1].strip())
                            case _:
                                continue

            collections_count = groups_count = events_count = 0
            misc_info = list(columns[4].children)

            for i in misc_info:
                match i:
                    case "\n":
                        continue
                    case _:
                        match (kv := list(map(lambda html: html.text, i.children)))[0]:
                            case "Collections:":
                                collections_count = int(kv[1].strip())
                            case "Groups:":
                                groups_count = int(kv[1].strip())
                            case "Events:":
                                events_count = int(kv[1].strip())
                            case _:
                                continue

            orgs.append(
                Organization(
                    name=name,
                    email=email,
                    user_count=user_count,
                    entries_count=entries_count,
                    attachments_count=attachments_count,
                    attachments_size=attachments_size,
                    collections_count=collections_count,
                    groups_count=groups_count,
                    events_count=events_count,
                )
            )

        return orgs
