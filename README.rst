Paul Graham: Essays
===================

Fetch and build Paul Graham's essays as a Kindle book for offline reading.

Requirements
============

The ``kindlegen`` (https://www.amazon.com/gp/feature.html?docId=1000765211
) command line tool must be installed and available in your ``PATH``.

::

    pushd /tmp
    wget http://kindlegen.s3.amazonaws.com/kindlegen_linux_2.6_i386_v2_9.tar.gz -O kindlegen.tar.gz
    tar xvzf kindlegen.tar.gz
    sudo cp kindlegen /usr/local/sbin/
    popd

Getting started
===============

::

  git clone https://github.com/razius/paul-graham-essays-ebook.git
  cd paul-graham-essays-ebook
  pip install -r requirements.txt

Building the ebook
==================

::

  python build.py
