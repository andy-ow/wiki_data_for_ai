from setuptools import setup

setup(name='wiki_data_for_ai',
      version='0.1',
      description='Get articles from wikipedia, prepare them to be used for openai model training. Based on '
                  'https://github.com/openai/openai-cookbook/blob/main/examples/fine-tuned_qa/olympics-1-collect-data.ipynb',
      url='https://github.com/andy-ow/wiki_data_for_ai',
      author='ao',
      author_email='ajoinfinity@gmail.com',
      license='MIT',
      packages=['wiki_data_for_ai'],
      zip_safe=False)
