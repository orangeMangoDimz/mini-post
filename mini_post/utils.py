from uuid import uuid4

def get_fileupload_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid4(), ext)
    directory = instance._meta.model_name
    print("directory: ", directory)
    return "{0}/{1}".format(directory, filename)

