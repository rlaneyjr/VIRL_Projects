# Copyright 2015 Cisco Systems, Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from __future__ import print_function
from unittest.case import TestCase
from unittest import main
from basics.render import tabulate

class Test(TestCase):

    def assert_boolean_cell_is_textual(self, cell_value):
        assert isinstance(cell_value, bool)
        table_text = tabulate([[cell_value]], tablefmt='plain')
        self.assertTrue(table_text == str(cell_value), "Expected string representation of boolean value.")

    def test_boolean_cell_is_textual(self):
        """ Does the monkey-patch of module 'tabulate' work?
        
        The standard 'tabulate' module renders boolean cell values as integers.
        The module 'basics.render' patches it to render str(boolean-value). 
        """
        self.assert_boolean_cell_is_textual(True)
        self.assert_boolean_cell_is_textual(False)

if __name__ == '__main__':
    main()
