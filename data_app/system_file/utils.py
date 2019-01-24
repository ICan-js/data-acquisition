import os
import shutil


def clear_files(path):
    """Function to remove all files
    :param path:
    :return:
    """

    for folder in os.listdir(path):
        if folder == 'imagens_para_enviar.zip':
            os.remove(os.path.join(path, folder))

        if folder in ['idade_tg', 'telefone_tg', 'desculpa_tg', 'amigo_tg']:
            shutil.rmtree(os.path.join(path, folder))
            os.mkdir(os.path.join(path, folder))


def create_dir(path):
    """Function to create dir
    :param path:
    :return:
    """

    if not os.path.exists(path):
        os.mkdir(path)


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def create_zip(path):
    """Function to create ZIP
    :param path:
    :return:
    """

    shutil.make_archive(os.path.join(path, 'imagens_para_enviar'), 'zip', path)
