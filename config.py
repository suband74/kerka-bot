logger_config = {
    'version': 1,
    'disable_existing_loggers': False,
   
    'formatters': {
        'main_format': {
            'format': '{asctime} - {levelname} - {filename} - {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'main_format',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'main_format',
            'filename': 'information.log'
        },
        'file1': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'formatter': 'main_format',
            'filename': 'warning.log'
        },
        },
    'loggers': {
        'main': {
            'handlers': ['console', 'file', 'file1'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}