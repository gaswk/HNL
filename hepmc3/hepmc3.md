# HepMC3

## HepMC3

### Installation

- Initialisation script:

```jsx
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc700
cd CMSSW_10_6_9
eval ‘scramv1 runtime -sh‘
export EDITOR=’emacs -nw ’
```

```jsx
# cmake
export LD_LIBRARY_PATH=/cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/cmake/3.17.2/share:$LD_LIBR
export PATH=/cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/cmake/3.17.2/bin:$PATH
```

- Create a working folder:

```jsx
mkdir WorkingFolder
cd WorkingFolder
```

- Download HepMC3:

```jsx
wget http://hepmc.web.cern.ch/hepmc/releases/HepMC3-3.2.6.tar.gz
tar -xzf HepMC3-3.2.6.tar.gz
```

- Building HepMC3

```jsx
mkdir hepmc3-build
cd hepmc3-build
cmake -DHEPMC3_ENABLE_ROOTIO=OFF -DHEPMC3_ENABLE_PYTHON=OFF \
-DCMAKE_INSTALL_PREFIX=../hepmc3-install ../HepMC3-3.2.6
cd -
```

- Download Pythia8

```jsx
wget https://pythia.org/download/pythia83/pythia8310.tgz
tar -xzf pythia8310.tgz
```

- Building Pythia8

```jsx
cd pythia8310/
./configure --with-hepmc3-bin=/AbsPathToWorkingFolder/hepmc3/hepmc3-install/bin/ \
--with-hepmc3-include=/AbsPathToWorkingFolder/hepmc3/hepmc3-install/include \
--with-hepmc3-lib=/AbsPathToWorkingFolder/hepmc3/hepmc3-install/lib64/
make -j8
```

### Running example

- Go to folder

```jsx
WorkingFolder/pythia8310/examples
```

```jsx
export PYTHIA8DATA=/AbsPathToWorkingFolder/pythia8310/share/Pythia8/xmldoc
```

- Replace files ```main42.cc```and ```main42.cmnd``` by the ones in this repository
- Build 

```jsx
make main42
```

- Running

```jsx
./main42 main42.cmnd input.lhe output.hepmc
```