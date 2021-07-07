import os
from collections import defaultdict
from typing import Dict

def get_fixtures(root_dir='tests/data') -> Dict[str, str]:
    """ Read the test case assertion input/output.

        Args:
            root_dir(str):
                testing fixtures folder

        Returns:
            fixtures(dict):
                {
                    'fixture 1':{ 
                        'input': str,
                        'output': str
                    },
                    'fixture 2':{ 
                        'input': str,
                        'output': str
                    },
                    ...
                }

    """
    
    fixtures = defaultdict(dict)
    for fname in os.listdir(root_dir):
        key = fname.replace('.txt', '').replace('_answer', '')
        with open(f'{root_dir}/{fname}', encoding='utf8') as f:
            text = ''.join(f.readlines())
            if '_answer' in fname:
                fixtures[key]['output'] = text
            else:
                fixtures[key]['input'] = text
    
    return fixtures
