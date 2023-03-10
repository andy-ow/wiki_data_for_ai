from setuptools import setup

setup(name='wiki_data_for_ai',
      version='0.0.1',
      description='Get articles from wikipedia, prepare them to be used for openai model training. Based on '
                  'https://github.com/openai/openai-cookbook/blob/main/examples/fine-tuned_qa/olympics-1-collect-data.ipynb',
      url='https://github.com/andy-ow/wiki_data_for_ai',
      author='ao',
      author_email='ajoinfinity@gmail.com',
      license='MIT',
      packages=['wiki_data_for_ai'],
      install_requires=[
            'wikipedia',
            'transformers',
            'nltk',
            'pandas',
      ],
      keywords='openai wikipedia',
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
      ],
      zip_safe=False)
