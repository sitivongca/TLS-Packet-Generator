# Compiling Guide

## This guide will show how to compile OpenSSL and Cryptography for SSLv3 support

## OpenSSL

Make sure to have the python venv already set up


#### Dependencies

- [Perl](https://strawberryperl.com/)
- [VS 2022 Installer](https://visualstudio.microsoft.com/downloads/) (if not already installed)
  - VS 2022 build tools
  - MSVC
  - Windows 10 SDK (Have not tested Windows 11 SDK)

If you want SSLv2 and weak ciphers you must install [OpenSSL 1.0.2](https://openssl-library.org/source/)
I do not have a config for 1.0.2 yet.
1. C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat x86_amd64 or wherever your path goes
2. cd d:/path/to/project_name/.venv/openssl-1.0.2(u or version you downloaded)
3. perl Configure VC-WIN64A --prefix=d:/path/to/project_name/.venv/openssl --openssldir=d:/path/to/project_name/.venv/openssl enable-ssl3 enable-ssl2 enable-md5 enable-weak-ssl-ciphers enable-rc5
4. ms\do_win64a
5. nmake -f ms\ntdll.mak
6. nmake -f ms\ntdll.mak install

-----------------------Only for SSLv3-------------------------------------
1. Download [OpenSSL 3.0.16](https://openssl-library.org/source/)
cd into /configs and run ./config.ps1 to install or do it manually with guide below
1. Remove the two no-ssl3 options directly from /configdata.pm at the options array in OpenSSL source folder
2. C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat x86_amd64 or wherever your path goes
3. perl Configure VC-WIN64A --prefix="abs-path-to/project-path/.venv/openssl" --openssldir="abs-path-to/project-path/.venv/openssl" enable-ssl3 enable-ssl3-method
4. nmake
5. nmake install
6. OpenSSL should be installed as /.venv/openssl
7. Replace Activate.ps1 with config/Activate.ps1
8. Replace /.venv/openssl/openssl.cnf

--------------------------------------------------------------------------

## Cryptography

1. [Rust installer](https://www.rust-lang.org/tools/install)
2. ./Activate.ps1
3. uninstall cryptography
4. pip cache purge
5. C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat x86_amd64 or wherever your path goes
6. set OPENSSL_DIR="abs-path-to/projectRoot/.venv/openssl"
7. pip install --no-binary :all: cryptography

## PyOpenSSL

1. ./Activate.ps1
2. set OPENSSL_DIR="D:/Other/VSC projects/TLS/.venv/openssl"
3. pip install --no-binary :all: pyopenssl

## InquirerPy

1. ./Activate.ps1
2. pip install InquirerPy
