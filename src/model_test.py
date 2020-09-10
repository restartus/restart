from src.restart import RestartModel

if __name__ == '__main__':
    oes_test = RestartModel(configdir='src', population='oes', state='California')
    dict_test = RestartModel(configdir='src', population='dict')
