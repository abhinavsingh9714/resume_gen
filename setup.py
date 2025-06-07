from setuptools import setup, find_packages

setup(
    name='resume_gen',
    version='0.1',
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    install_requires=[
        'fastapi',
        'uvicorn',
        'openai',
        'python-dotenv',
        'pydantic',
        'sentence-transformers',
        'faiss-cpu'
    ],
    entry_points={
        'console_scripts': [
            'resgen=resume_gen.main:main'
        ]
    },
    author='Abhinav Singh',
    description='An AI-powered resume bullet generator with RAG and ATS optimization',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
