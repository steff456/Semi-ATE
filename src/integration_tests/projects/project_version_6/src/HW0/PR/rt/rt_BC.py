# -*- coding: utf-8 -*-
"""

Do **NOT** change anything in this module, as it is automatically generated thus your changes **WILL** be lost in time!

If you have the need to add things, add it to 'rt.py' or 'common.py'

BTW : YOU SHOULD **NOT** BE READING THIS !!!
"""

from math import inf, nan
from ate_test_app.sequencers.DutTesting.TestParameters import OutputParameter
from ate_test_app.sequencers.DutTesting.DutTestCaseABC import DutTestCaseBase
from ate_test_app.sequencers.DutTesting.Result import Result
from ate_test_app.parameters.ResolverFactory import create_parameter_resolver
from ate_common.logger import (LogLevel, Logger)


class rt_OP:
    """Class definition for the output parameters of rt."""

    def __init__(self):
        self.num_outputs = 0
        self.new_parameter1 = OutputParameter('new_parameter1', -inf, nan, 0.0, nan, inf, 0)
        self.new_parameter1.set_format('.3f')
        self.new_parameter1.set_unit('˽')

    def set_parameter(self, name: str, id: int, ltl: float, utl: float, bin: int, bin_result: int, test_desc: str):
        output = getattr(self, f'{name}')
        output.set_limits(id, ltl, utl)
        output.set_bin(bin, bin_result)
        output.set_test_description(test_desc)
        self.num_outputs += 1

    def get_output_nums(self) -> int:
        return self.num_outputs

class rt_IP:
    """Class definition for the input parameters of rt."""

    def __init__(self):
        self.Temperature = None

    def set_parameter(self, name: str, type: str, value: float, min_value: float, max_value: float, power: int, context: str, shmoo: bool):
        setattr(self, f'{name}', create_parameter_resolver(type, f'{name}', shmoo, value, min_value, max_value, power, context))


class rt_BC(DutTestCaseBase):
    '''Base class definition for rt'''

    hardware = 'HW0'
    base = 'PR'
    Type = 'custom'

    def __init__(self, instance_name: str, sbin, test_num, context):
        super().__init__(None, None, instance_name, sbin, test_num, context)
        self.ip = rt_IP()
        self.op = rt_OP()

    def aggregate_test_result(self, site_num: int, exception: bool):
        stdf_data = []
        test_result = Result.Inconclusive()
        test_bin = -1
        if not exception:
            current_result = self.op.new_parameter1.get_testresult()
            test_result = self._select_testresult(test_result, current_result)
            test_bin = self._select_bin(test_bin, current_result)
            stdf_data.append(self.op.new_parameter1.generate_ptr_record(current_result[0], site_num))
        else:
            test_result = Result.Fail()
            test_bin = self.get_sbin()
            stdf_data.append(self.op.new_parameter1.generate_ptr_record(test_result, site_num))

        return (test_result, test_bin, stdf_data)

    def aggregate_tests_summary(self, head_num: int, site_num: int):
        stdf_data = []
        stdf_data.append(self.op.new_parameter1.generate_tsr_record(head_num, site_num, self.get_average_test_execution_time()))

        return stdf_data

    def get_test_nums(self) -> int:
        return self.op.get_output_nums()

    def get_input_parameter(self, parameter_name: str):
        return getattr(self.ip, parameter_name)