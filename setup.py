from setuptools import setup, find_packages


setup(
    name='blogsite',
    version='${version}',
    description='Django博客系统',
    author='wang',
    author_email='wang@123.com',
    url='https://github.com/LowSing3721/blogsite',
    license='MIT',
    packages=find_packages('blogsite'),
    package_dir={'': 'blogsite'},
    package_data={'': [
        'themes/*/*/*/*',
    ]},
    # include_package_data=True,
    install_requires=[
        'Django==3.2.4',
        'gunicorn==20.1.0',
        'supervisor==4.2.2',
        # 'xadmin==2.0.1',
        'mysqlclient==2.0.3',
        'django-ckeditor==6.1.0',
        'djangorestframework==3.12.4',
        'django-redis==5.0.0',
        'django-autocomplete-light==3.8.2',
        'mistune==0.8.4',
        # 'Pillow==4.3.0',
        'coreapi==2.3.3',
        # 'hiredis==0.2.0',
        # debug
        'django-debug-toolbar==3.2.1',
        # 'django-silk==2.0.0',
    ],
    # extra_require={
    #     'ipython': ['ipython==6.2.1']
    # },
    scripts=['blogsite/manage.py'],
    entry_points={'console_scriptss': [
        'blogsite_manage = manage:main'
    ]},
    classifiers=[
        # 开发状态
        'Development Status :: 3 - Alpha',
        # 项目受众
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        # 许可证
        'License :: OSI Approved :: MIT License',
        # 项目所需Python版本
        'Programming Language :: Python :: 3.9',
    ]
)
