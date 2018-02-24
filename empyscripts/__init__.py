"""
Documentation for ``empyscripts``, the add-ons for ``empymod``.

The add-ons are all independent of each other, and have their own
documentation. You can find the information of each add-on in the respective
*Code*-section.

For more information regarding installation, usage, add-ons, contributing,
roadmap, bug reports, and much more, see https://empymod.github.io.


License
-------

Copyright 2017-2018 Dieter Werthmüller

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
# Copyright 2017-2018 Dieter Werthmüller
#
# This file is part of empyscripts.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy
# of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations under
# the License.

from . import tmtemod
from . import fdesign
from .printinfo import versions

__all__ = ['tmtemod', 'fdesign', 'versions']

# Version
__version__ = '0.3.1dev0'
