# import pytest
#
#
# ENABLE_RECURRING_JOB_OPT = "--enable-recurring-job-test"
# ENABLE_CSI_OPT = "--enable-csi-test"
#
#
# def pytest_addoption(parser):
#     parser.addoption(ENABLE_RECURRING_JOB_OPT, action="store_true",
#                      default=False,
#                      help="enable recurring job test or not")
#     parser.addoption(ENABLE_CSI_OPT, action="store_true",
#                      default=False,
#                      help="enable CSI test or not")
#
#
# def pytest_collection_modifyitems(config, items):
#     if not config.getoption(ENABLE_RECURRING_JOB_OPT):
#         skip_upgrade = pytest.mark.skip(reason="need " +
#                                         ENABLE_RECURRING_JOB_OPT +
#                                         " option to run")
#         for item in items:
#             if "recurring_job" in item.keywords:
#                 item.add_marker(skip_upgrade)
#
#     if not config.getoption(ENABLE_CSI_OPT):
#         skip_upgrade = pytest.mark.skip(reason="need " +
#                                         ENABLE_CSI_OPT +
#                                         " option to run")
#         for item in items:
#             if "csi" in item.keywords:
#                 item.add_marker(skip_upgrade)
