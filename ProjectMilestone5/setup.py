from setuptools import setup, find_packages

setup(
    name="uvsim",  # Name of your package
    version="0.1",  # Version of your package
    packages=find_packages(where="src"),  # Finds all packages inside 'src' directory
    package_dir={"": "src"},  # Specify where the source code is located
    install_requires=[  # Dependencies your project needs to run
        "tk",  # Tkinter for GUI
    ],
    entry_points={  # This section defines command line scripts to run the app
        "console_scripts": [
            "uvsim=uvsim.gui:main",  # Runs the main() function in gui.py
        ],
    },
    # Optional: Add metadata
    author="Your Name",  
    author_email="your.email@example.com",
    description="A BasicML Simulator with GUI",
    long_description=open('README.md').read(),  # If you have a README file
    long_description_content_type="text/markdown",  # If it's a markdown file
    url="https://github.com/yourusername/uvsim",  # Project URL
    classifiers=[  # Classifiers help people find your package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version required
)
