from os import makedirs, path
from urllib3 import PoolManager, disable_warnings
from bs4 import BeautifulSoup
from config import basedir
from app import db
from app.models import Tasks, Paths
from concurrent.futures import ThreadPoolExecutor, as_completed


disable_warnings()


def get_texts(task):

    destiny = basedir + "/taken_files/text/" + str(task.id) + ".txt"

    task.status = "started"
    db.session.commit()

    try:
        with open(destiny, "w") as file:
            page = PoolManager().request("GET", task.url)
            content_page = page.data
            # coding = page.getheader['charset']
            soup = BeautifulSoup(content_page,
                                 "html.parser")
                                 # from_encoding=coding)

            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            text = soup.get_text()

            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())

            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines
                      for phrase in line.split("  "))

            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)

            file.writelines(text)

        p = Paths(task_id=task.id, path=destiny)
        db.session.add(p)
        db.session.commit()

        task.status = "finished"

    except Exception as e:
        task.status = "error: {}".format(e)


def get_images(task):

    destiny = basedir + "/taken_files/image/" + str(task.id)

    if not path.exists(destiny):
        makedirs(destiny)

    task.status = "started"
    db.session.commit()

    http = PoolManager()
    page = http.request("GET", task.url)
    content_page = page.data
    coding = page.getheader('charset')
    soup = BeautifulSoup(content_page,
                         "html.parser",
                         from_encoding = coding)
    images_list = soup.find_all('img')

    for image in images_list:
        file_name = image['src'].split("/")[-1]
        path_file = destiny + "/" + file_name

        p = Paths(task_id=task.id, path=str(path_file))
        db.session.add(p)
        db.session.commit()

        try:
            with open(path_file, "wb") as out_image:
                http = PoolManager().request("GET",
                                             task.url + image['src'],
                                             preload_content = False)
                for chunk in http.stream(1024):
                    out_image.write(chunk)

        except Exception as e:
            task.status = "error: {}".format(e)

    task.status = "finished"


text_tasks_list = Tasks.query.filter_by(
        status='added').filter_by(task_type=0).all()

image_tasks_list = Tasks.query.filter_by(
        status='added').filter_by(task_type=1).all()

# if text_tasks_list:
#     for task in text_tasks_list:
#         get_texts(task)

with ThreadPoolExecutor() as executor:
    futures_que = 0
    if text_tasks_list:
        futures_que = {executor.submit(get_texts, task):
                           task for task in text_tasks_list}
    if image_tasks_list:
        futures_que = {executor.submit(get_images, task):
                           task for task in image_tasks_list}

    if futures_que:
        for future in as_completed(futures_que):
            task = futures_que[future]

db.session.commit()
# if image_tasks_list:
#     with Pool() as image_pool:
#         image_multiple_results = [
#             image_pool.apply_async(get_images, ()) for i in image_tasks_list]
#


