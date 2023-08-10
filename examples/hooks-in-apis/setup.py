from distutils.core import setup

setup(
    name="api",
    version="1.0",
    description="Python Distribution Utilities",
    author="Amit Assaraf",
    author_email="amit.assaraf@gmail.com",
    url="https://www.python.org/sigs/distutils-sig/",
    packages=[
        "distutils",
        "distutils.command",
        "flask",
        "requests",
        "json",
        "time",
        "redis",
        "typing",
        "flask_cors",
    ],
)
