class AnsibleError(Exception):
    pass

class AnsibleConnectionError(AnsibleError):
    pass

class AnsibleRequestError(AnsibleError):
    pass
