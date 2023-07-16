import json
import logging

logging.basicConfig(
    format='[%(asctime)s] %(levelname)-8s {%(filename)s:%(lineno)d} : %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S', level=logging.WARNING
)

def cache_to_file(dir_name, _hash):
    def decorator(original_func):
        logger = logging.getLogger(__name__)

        def new_func(self, params, force_reload = False):
            hash_result = _hash(params)
            file_name = dir_name + "/{}.csv".format(hash_result)
            logger.debug("Reading data from file: {}. Force reload set to {}".format(file_name, force_reload))
            try:
                f = open(file_name, 'r')
                cache = json.load(f)
                f.close()
            except (IOError, ValueError):
                cache = {}

            if hash_result not in cache or not cache[hash_result] or force_reload:
                logger.debug("Could not find results in cache. Calling the function to get results")
                cache[hash_result] = original_func(self, params)
                logger.debug("Saving data to file: {}".format(file_name))
                f = open(file_name, 'w')
                json.dump(cache, f)
                f.close()
            else:
                logger.debug("Results already exist. Fetching from cache")
            return cache[hash_result]

        return new_func

    return decorator
