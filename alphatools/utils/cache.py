import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)-8s [%(asctime)s] : %(message)s'
)

def cache_to_file(dir_name, _hash):
    def decorator(original_func):
        logger = logging.getLogger(__name__)

        def new_func(self, params):
            hash_result = _hash(params)
            file_name = dir_name + "/{}.csv".format(hash_result)
            try:
                f = open(file_name, 'r')
                cache = json.load(f)
                f.close()
            except (IOError, ValueError):
                cache = {}

            if hash_result not in cache or not cache[hash_result]:
                logger.debug("Could not find results in cache. Calling the function to get results")
                cache[hash_result] = original_func(self, params)
                f = open(file_name, 'w')
                json.dump(cache, f)
                f.close()
            logger.debug("Results already exist. Fetching from cache")
            return cache[hash_result]

        return new_func

    return decorator
