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

    # Compile fortran programs (inside CL environment)
    cd /path/Ureka/iraf/extern/beacon/pccd
    # chmod -R 777 ../pccd
    del pccd2000gen05.mac.e 
    del ccdrap_e.e
    fc pccd2000gen05.mac.f -o pccd2000gen05.mac.e
    fc ccdrap_e.f -o ccdrap_e.e

    # On Ubuntu, one may install the packages 
    # libgcc-4.8-dev:i386 lib32gcc-4.8-dev


Complementary scripts
-----------------------

Additional tools are available in the ``pyhdust`` Python package:

    https://pypi.python.org/pypi/pyhdust

Lamps
-------
Description of the files: 

- `ecavg_lamp_a.ms` - azul/blue lamp file for  MUSICOS 
- `ecavg_lamp_b.ms` - idem 
- `ecavg_lamp_r.ms` - red/vermelho lamp file for MUSICOS 
- `ecavg_lamp_v.ms` - idem
- `mus_ap_b.pdf` - lines catalog at azul/blue wavelengths for MUSICOS 
- `mus_ap_r.pdf` - lines catalog at red/vermelho wavelengths for MUSICOS 
- `ref_ecass_b.tiff` - azul/blue lamp lines for a configuration of CASSEGRAIN
- `ref_ecass_r.tiff` - red/vermelho lamp lines for a configuration of CASSEGRAIN
- `ref_thar_3600-9300.pdf` - lines catalog of Th-Ar lamp
