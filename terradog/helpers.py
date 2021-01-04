import logging
import os
import sys
import traceback
import jinja2
import subprocess
import hashlib

import ruyaml as yaml


logger = logging.getLogger(__name__)


def render_template(template_name, template_path, target, context, delete_template=True, overwrite=False):
    """
    Helper function to write out DRY up templating. Accepts template name (string),
    path (string), target directory (string), context (dictionary) and delete_template (boolean)
    Default behavior is to use the key of the dictionary as the template variable names, replace
    them with the value in the tempalate and delete the template if delete_template is
    True
    """

    logging.debug("Writing {}".format(target))
    logging.debug("Template Context: {}".format(context))
    logging.debug("Overwrite is {}".format(overwrite))
    if os.path.isfile(target) and overwrite is not True:
        logging.warning("Cowardly refusing to overwrite existing file {}".format(target))
        return False

    logging.debug("Attempting to write {} from template {}/{}".format(target, template_path, template_name))

    template_path = os.path.normpath(template_path)
    template_name = os.path.normpath(template_name)
    template_permissions = os.stat(template_path + '/' + template_name).st_mode

    with open(target, 'w+') as f:
        try:
            jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path), keep_trailing_newline=True)
            template = jinja_environment.get_template(template_name)
            f.write(template.render(context))
        except Exception as e:
            logging.error("Error writing {}. {}".format(target, traceback.print_exc(e)))
            return False

    os.chmod(target, template_permissions)

    if delete_template:
        logging.debug("Removing {}/{}".format(template_path, template_name))
        os.remove("{}/{}".format(template_path, template_name))


def merge_dict(d, new_data, clobber=False):
    """ accepts new_data (dict) and clobbber (boolean). Merges dictionary with dictionary 'd'. If clobber is True, overwrites value. Defaults to false """
    d = d.copy()
    for key, value in list(new_data.items()):
        if d.get(key) is None or clobber:
            logging.debug("Setting component data {}: {}".format(key, value))
            d[key] = value
    return d


def parse_yaml_file(yaml_file) -> dict:
    """ Parse yaml file into dictionary """
    try:
        with open(yaml_file, 'r') as yaml_stream:
            data = yaml.safe_load(yaml_stream)
            logging.debug("Data parsed from file {}: {}".format(yaml_file, data))
            return data
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def validate_tf(directory) -> None:
    """
    Validate terraform in the path provided by running `terraform fmt`

    Accepts:
        - directory: location to run `terrform fmt`

    Return:
        None
    """

    try:
        if len([file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file)) and file.endswith(".tf")]) > 0:
            tf = subprocess.check_output(['terraform', 'fmt', directory])
            logger.debug(tf)
            logger.debug("terraform fmt output:\n{}".format(tf))

    except subprocess.CalledProcessError as validateErr:
        logger.warning("Error validating terraform: {}".format(validateErr.output))
        logger.warning(['terraform', 'fmt', directory])
        tf = subprocess.check_output(['terraform', 'fmt', directory])
        logger.warning(tf)


def hash_directory(directory):
    SHAhash = hashlib.sha1()
    if not os.path.exists(directory):
        raise Exception(directory + " does not exist")
    for root, _, files in os.walk(directory):
        for name in files:
            filepath = os.path.join(root, name)
            f1 = open(filepath, 'rb')
            while 1:
                buf = f1.read(4096)
                if not buf:
                    break
                h = hashlib.sha1(buf).hexdigest()
                SHAhash.update(h.encode('utf-8'))
            f1.close()

    return SHAhash.hexdigest()
