''' A lightweight configuration system inspired by yacs[yet another configuration system] '''

from ast import literal_eval
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

    def update_args(self,args):
        '''Override an existing config attribute by getting input
        from sys.argv[1:]'''

        '''The input is of the format --arg=value,
        where arg can be nested form attribute. 
        Hence we need to handle the nested case also.'''
        
        # Note: The (.) in arg is used to denote nested  sub-attributes.
        '''eg: --config.model.drop_ratio=0.5 --config.trainer.lr=1e-3'''

        for arg in args:
            pair=arg.split('=')
            assert len(pair)==2, 'Expected override value is missing. Got {} instead'.format(arg)

            key,val=pair
            #Handling value
            try:
                val=literal_eval(val)

            except ValueError:
                exit()

            #Handling the key
            assert key[:2]=='--', 'Config attriute format is illegal. Got {} instead'.format(key)
            keys=key[2:]
            keys=keys.split('.')

            obj=self
            for attr in keys[:-1]:
                obj=getattr(obj,attr)
            
            leaf_attr=keys[-1]
            assert hasattr(obj,leaf_attr),  '{} attribute Not Found in the config setting!!'.format(key[2:])
            
            print(f'Overwritting attribute {key[2:]} from {getattr(obj,leaf_attr)} to {val} in config setting.....')
            setattr(obj,leaf_attr,val)