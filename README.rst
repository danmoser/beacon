beacon-reduc
==============

IRAF tools for polarimetry and spectroscopy from the `BeACoN group <http://beacon.iag.usp.br/>`_.

About the instruments in this pipeline:

- `MUSICOS <http://www.lna.br/opd/instrum/musicos.html>`_
- `Cassegrain spectograph <http://www.lna.br/opd/instrum/instr.html>`_
- `IAGPOL polarimeter <http://www.astro.iag.usp.br/~polarimetria/gaveta/english.htm>`_

Installation
--------------
The suggestion is to install the package as an symbolic link. Then add it to 
the extern packages of IRAF, add the its scripts to the path:

.. code:: bash

    ln -s /path/to/beacon /path/Ureka/iraf/extern/beacon
    
    # Add the following lines to 
    # /path/Ureka/iraf/unix/hlib/extern.pkg
    #
    # reset   beacon      = iraf$extern/beacon
    # task    beacon.pkg  = beacon$beacon.cl

    # Add the scripts folder to the PATH in the $HOME/.bashrc (or equiv.)
    # PATH=$PATH:/path/to/beacon/scripts