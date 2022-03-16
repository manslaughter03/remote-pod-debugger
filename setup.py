from setuptools import setup, find_packages


REQUIREMENTS = [
    "kubernetes==v23.3.0"
]

setup(
    name="remote-pod-debugger",
    version="0.0.1",
    install_requires=REQUIREMENTS,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        "console_scripts": [
            "remote-pod-debugger = remote_pod_debugger.__main__:main"
        ]
    },
)
