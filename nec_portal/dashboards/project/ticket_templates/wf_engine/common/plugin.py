#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#

from abc import ABCMeta
from abc import abstractmethod
from exceptions import NotImplementedError
import six


@six.add_metaclass(ABCMeta)
class BasePlugin(object):
    """Plugin base class of of workflow view form engine"""

    @abstractmethod
    def set_context_data(
            self, called_object, context, form_template, **kwargs):

        raise NotImplementedError()
