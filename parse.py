import requests
from bs4 import BeautifulSoup as BS


def post_request(name, surname, fathername, n_zach, learn_type):
    url_login = 'https://www.nntu.ru/content/studentam/uspevaemost'
    url_request = 'https://www.nntu.ru/frontend/web/student_info.php'

    client = requests.session()
    html = client.get(url_login)
    cookies = html.cookies.get_dict()

    payload = {
        'last_name': f'{surname}',  # должны получаться значения в функцию из бд
        'first_name': f'{name}',
        'otc': f'{fathername}',
        'n_zach': f'{n_zach}',
        'learn_type': f'{learn_type}'
    }

    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/83.0.4103.97 Safari/537.36'
    }

    r = requests.post(url_request, data=payload)
    r1 = BS(r.content, 'html.parser')

    return r1


def quantity_sem(r1):
    tables = r1.find_all('table', attrs={'class': 'table table-bordered table-sm'})
    qu = len(tables)

    return qu


def form_marks(r1, sem_n):
    try:
        string = ""
        tables = r1.find_all('table', attrs={'class': 'table table-bordered table-sm'})
        trs = tables[sem_n].find_all('tr', attrs={'class': 'tr_class'})
        for tr in trs:
            tds = tr.find_all('td')
            i = 0
            for td in tds:
                if i == 0:
                    cs = tds[i].text
                    string += '\n' + f"<b>{cs}</b>" + '\n'
                    i = 1
                while i < len(tds):
                    cs = tds[i].text
                    if cs == "":
                        string += "_ "
                    else:
                        if i == len(tds) - 1:
                            string += f"({tds[len(tds) - 1].text})"
                        else:
                            string += cs + " "
                    i += 1

        return string
    except Exception:
        return False
