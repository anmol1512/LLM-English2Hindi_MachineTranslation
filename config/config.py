''' A lightweight configuration system inspired by yacs[yet another configuration system] '''
class CfgNode:
    #Below are the target of this class
    # 1. Able to represent current configuration in a human redable block style manner like in yaml file config
    # 2. Able to represent current configuration in a nested dictionary format similar to yaml.load()
    # 3. Able to ovewrite the configuration using command line.
    def __init__(self, **kwargs):
        vars(self).update(kwargs)

    def __str__(self):
        return self._block_repr(0)

    def _block_repr(self, indent):
        lines = []
        for key, value in vars(self).items():
            if isinstance(value, CfgNode):
                lines.append(f"{'  ' * indent}{key}:")
                lines.append(value._block_repr(indent + 1))
            else:
                lines.append(f"{'  ' * indent}{key}: {value}")
        return "\n".join(lines)

    def dict_repr(self):
        return {key: value.dict_repr() if isinstance(value, CfgNode) else value for key, value in vars(self).items()}

    def update_dict(self, d):
        vars(self).update(d)