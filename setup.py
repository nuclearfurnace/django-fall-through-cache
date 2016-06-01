from setuptools import setup

setup(
    name="django-fall-through-cache",
    url="http://github.com/nuclearfurnace/django-fall-through-cache/",
    author="Toby Lawrence",
    author_email="toby@nuclearfurnace.com",
    version="1.6.5",
    packages=["fall_through_cache", "fall_through_cache.backends"],
    description="Fall Through Cache Backend for Django",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
)
