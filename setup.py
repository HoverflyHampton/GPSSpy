import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

print(setuptools.find_packages('src'))

setuptools.setup(
    name="gpsspy",  # Replace with your own username
    version="0.0.2",
    author="William Hampton",
    author_email="william.hampton@hoverflytech.com",
    description="An implementation of GPS jamming detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HoverflyHampton/Qwiic_Ublox_Gps_Py",
    packages=setuptools.find_packages('src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Development Status:: 4 - Beta",
    ],
    python_requires='>=3.6',
)
