#!/bin/bash

# Help text
usage="
$(basename "$0") [-hcpn] [-v VERSION(S)]

Run pytest for empymod locally in an isolated venv before submitting to
GitHub/Travis-CI; by default for all supported python versions of empymod.

where:
    -h : Show this help text.
    -v : Python 3.x version, e.g. '-v 5' for Python 3.5. Default: '4 5 6'.
    -c : Use channel 'conda-forge' instead of channel 'defaults'.
    -p : Print output of conda.

"

# Set default values
CHAN=defaults
PYTHON3VERSION="4 5 6"
PRINT="/dev/null"
PCKGS="numpy scipy pytest pytest-cov"
NMXPR="numexpr matplotlib IPython"
STR2="**  WITH numexpr/matplotlib/IPython  "
PROPS="--mpl --flake8"
INST="pytest-flake8 pytest-mpl"

# Get Optional Input
while getopts "hv:cpn" opt; do
  case $opt in
    h) echo "$usage"
       exit
       ;;
    v) PYTHON3VERSION=$OPTARG
       ;;
    c) CHAN=conda-forge
       ;;
    p) PRINT="/dev/tty"
       ;;
    n) NMXPR=""
       STR2="**  NO numexpr/matplotlib/IPython  "
       PROPS="--flake8"
       INST="pytest-flake8"
       ;;
    :) printf "missing argument for -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
   \?) printf "illegal option: -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
  esac
done

# Loop over Python versions
for i in ${PYTHON3VERSION[@]}; do

  # Print info
  STR="  PYTHON 3."${i}"  **  Channel "$CHAN"  $STR2"
  LENGTH=$(( ($(tput cols) - ${#STR}) / 2 - 2 ))
  printf "\n  "
  printf '\e[1m\e[34m%*s' "${LENGTH}" '' | tr ' ' -
  if [ $((${#STR}%2)) -ne 0 ];
  then
      printf "-"
  fi
  printf "${STR}"
  printf '%*s\n' "${LENGTH}" '' | tr ' ' -
  printf "\e[0m\n"

  # Create venv, with channel CHAN
  conda create -y -n test_3${i} -c $CHAN python=3.${i} $PCKGS $NMXPR &> $PRINT

  # Activate venv
  source activate test_3${i}

  # Install flake8
  pip install $INST &> $PRINT

  # Install empymod
  conda install -y -c prisae empymod &> $PRINT

  # Run tests
  pytest --cov=empyscripts $PROPS

  # De-activate venv
  source deactivate test_3${i}

  # Remove venv
  conda remove -y -n test_3${i} --all &> $PRINT

done
