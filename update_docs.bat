@echo off
python --version > find /i "Python 3.8" >nul 2>&1
if errorlevel 1 (
    echo Wrong or no version of Python found :/
    echo Try downloading and installing the right version of Python from
    echo "https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe"
    echo Make sure to check "Add Python 3.8 to PATH"!
    echo Restart your computer afterwards!
) else (
    python -m pip install --upgrade pip
    python -m pip install sphinx
    python -m pip install pylint pydot Graphviz

    :: generate graphic docs with pyreverse (pylint)
    if errorlevel 1 (
        echo "dot"-command not found :/
        echo Try downloading and installing the Graphviz manually from
        echo "https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/2.48.0/stable_windows_10_cmake_Release_x64_graphviz-install-2.48.0-win64.exe"
        echo Make sure to select "Add Graphviz to the system PATH [...]"!
    ) else (
        type nul > __init__.py
        type nul > src/__init__.py
        pyreverse --all-associated ../AutoSplitter/
        dot -Tpng classes.dot -o doc/classes.png
        dot -Tpng packages.dot -o doc/packages.png
        del classes.dot
        del packages.dot
        del "__init__.py"
        cd src
        del "__init__.py"
        cd ..
    )

    :: generate text docs with sphinx
    cd doc/src
    call generate_docs.bat
    cd ..
    start "" index.html
)
