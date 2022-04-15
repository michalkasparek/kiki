from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(name="Kiki",
    version="0.4.1",
    description="Praktický nástroj pro editor(k)y (českých) textů",
    author="Michal Kašpárek",
    author_email="michal.kasparek@gmail.com",
    url="https://github.com/michalkasparek/kiki"
    packages=["Kiki"],
    install_requires=["markdown", "tk"],
    )
