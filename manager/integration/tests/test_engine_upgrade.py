# import pytest
#
# import common
# from common import clients, volume_name  # NOQA
# from common import SIZE
# from common import wait_for_volume_state, wait_for_volume_delete
# from common import wait_for_volume_engine_image, wait_for_engine_image_state
# from common import wait_for_engine_image_ref_count
#
# REPLICA_COUNT = 2
#
#
# def test_engine_image(clients, volume_name):  # NOQA
#     # get a random client
#     for host_id, client in clients.iteritems():
#         break
#
#     # can be leftover
#     default_img = common.get_default_engine_image(client)
#     default_img_name = default_img["name"]
#     default_img = wait_for_engine_image_ref_count(client, default_img_name, 0)
#
#     images = client.list_engine_image()
#     assert len(images) == 1
#     assert images[0]["default"]
#     assert images[0]["state"] == "ready"
#     assert images[0]["refCount"] == 0
#     assert images[0]["gitCommit"] != ""
#     assert images[0]["buildDate"] != ""
#
#     cli_v = default_img["cliAPIVersion"]
#     cli_minv = default_img["cliAPIMinVersion"]
#     ctl_v = default_img["controllerAPIVersion"]
#     ctl_minv = default_img["controllerAPIMinVersion"]
#     data_v = default_img["dataFormatVersion"]
#     data_minv = default_img["dataFormatMinVersion"]
#
#     assert cli_v != 0
#     assert cli_minv != 0
#     assert ctl_v != 0
#     assert ctl_minv != 0
#     assert data_v != 0
#     assert data_minv != 0
#
#     # delete default image is not allowed
#     with pytest.raises(Exception) as e:
#         client.delete(images[0])
#     assert "the default engine image" in str(e.value)
#
#     # duplicate images
#     with pytest.raises(Exception) as e:
#         client.create_engine_image(image=default_img["image"])
#
#     engine_upgrade_image = common.get_upgrade_test_image(cli_v, cli_minv,
#                                                          ctl_v, ctl_minv,
#                                                          data_v, data_minv)
#
#     new_img = client.create_engine_image(image=engine_upgrade_image)
#     new_img_name = new_img["name"]
#     new_img = wait_for_engine_image_state(client, new_img_name, "ready")
#     assert not new_img["default"]
#     assert new_img["state"] == "ready"
#     assert new_img["refCount"] == 0
#     assert new_img["cliAPIVersion"] != 0
#     assert new_img["cliAPIMinVersion"] != 0
#     assert new_img["controllerAPIVersion"] != 0
#     assert new_img["controllerAPIMinVersion"] != 0
#     assert new_img["dataFormatVersion"] != 0
#     assert new_img["dataFormatMinVersion"] != 0
#     assert new_img["gitCommit"] != ""
#     assert new_img["buildDate"] != ""
#
#     client.delete(new_img)
#
#
# def test_engine_offline_upgrade(clients, volume_name):  # NOQA
#     # get a random client
#     for host_id, client in clients.iteritems():
#         break
#
#     default_img = common.get_default_engine_image(client)
#     default_img_name = default_img["name"]
#     default_img = wait_for_engine_image_ref_count(client, default_img_name, 0)
#     cli_v = default_img["cliAPIVersion"]
#     cli_minv = default_img["cliAPIMinVersion"]
#     ctl_v = default_img["controllerAPIVersion"]
#     ctl_minv = default_img["controllerAPIMinVersion"]
#     data_v = default_img["dataFormatVersion"]
#     data_minv = default_img["dataFormatMinVersion"]
#     engine_upgrade_image = common.get_upgrade_test_image(cli_v, cli_minv,
#                                                          ctl_v, ctl_minv,
#                                                          data_v, data_minv)
#
#     new_img = client.create_engine_image(image=engine_upgrade_image)
#     new_img_name = new_img["name"]
#     new_img = wait_for_engine_image_state(client, new_img_name, "ready")
#     assert new_img["refCount"] == 0
#     assert new_img["noRefSince"] != ""
#
#     default_img = common.get_default_engine_image(client)
#     default_img_name = default_img["name"]
#
#     volume = client.create_volume(name=volume_name, size=SIZE,
#                                   numberOfReplicas=REPLICA_COUNT)
#     volume = wait_for_volume_state(client, volume_name, "detached")
#     default_img = wait_for_engine_image_ref_count(client, default_img_name, 1)
#
#     original_engine_image = default_img["image"]
#
#     assert volume["name"] == volume_name
#
#     volume.engineUpgrade(image=new_img["image"])
#     volume = wait_for_volume_engine_image(client, volume_name,
#                                           new_img["image"])
#     default_img = wait_for_engine_image_ref_count(client, default_img_name, 0)
#     new_img = wait_for_engine_image_ref_count(client, new_img_name, 1)
#
#     # cannot delete a image in use
#     with pytest.raises(Exception) as e:
#         client.delete(new_img)
#     assert "while being used" in str(e.value)
#
#     volume = volume.attach(hostId=host_id)
#     volume = wait_for_volume_state(client, volume_name, "healthy")
#
#     assert volume["controller"]["engineImage"] == engine_upgrade_image
#     for replica in volume["replicas"]:
#         assert replica["engineImage"] == engine_upgrade_image
#
#     volume = volume.detach()
#     volume = wait_for_volume_state(client, volume_name, "detached")
#
#     volume.engineUpgrade(image=original_engine_image)
#     volume = wait_for_volume_engine_image(client, volume_name,
#                                           original_engine_image)
#     assert volume["engineImage"] == original_engine_image
#
#     default_img = wait_for_engine_image_ref_count(client, default_img_name, 1)
#     new_img = wait_for_engine_image_ref_count(client, new_img_name, 0)
#
#     volume = volume.attach(hostId=host_id)
#     volume = wait_for_volume_state(client, volume_name, "healthy")
#
#     assert volume["controller"]["engineImage"] == original_engine_image
#     for replica in volume["replicas"]:
#         assert replica["engineImage"] == original_engine_image
#
#     client.delete(volume)
#     wait_for_volume_delete(client, volume_name)
#
#     client.delete(new_img)
#
#
# def test_engine_live_upgrade(clients, volume_name):  # NOQA
#     # get a random client
#     for host_id, client in clients.iteritems():
#         break
#
#     default_img = common.get_default_engine_image(client)
#     default_img_name = default_img["name"]
#     default_img = wait_for_engine_image_ref_count(client, default_img_name, 0)
#     cli_v = default_img["cliAPIVersion"]
#     cli_minv = default_img["cliAPIMinVersion"]
#     ctl_v = default_img["controllerAPIVersion"]
#     ctl_minv = default_img["controllerAPIMinVersion"]
#     data_v = default_img["dataFormatVersion"]
#     data_minv = default_img["dataFormatMinVersion"]
#     engine_upgrade_image = common.get_upgrade_test_image(cli_v, cli_minv,
#                                                          ctl_v, ctl_minv,
#                                                          data_v, data_minv)
#
#     new_img = client.create_engine_image(image=engine_upgrade_image)
#     new_img_name = new_img["name"]
#     new_img = wait_for_engine_image_state(client, new_img_name, "ready")
#     assert new_img["refCount"] == 0
#     assert new_img["noRefSince"] != ""
#
#     default_img = common.get_default_engine_image(client)
#     default_img_name = default_img["name"]
#
#     volume = client.create_volume(name=volume_name, size=SIZE,
#                                   numberOfReplicas=2)
#     volume = wait_for_volume_state(client, volume_name, "detached")
#     default_img = wait_for_engine_image_ref_count(client, default_img_name, 1)
#
#     assert volume["name"] == volume_name
#
#     original_engine_image = volume["engineImage"]
#     assert original_engine_image != engine_upgrade_image
#
#     volume = volume.attach(hostId=host_id)
#     volume = wait_for_volume_state(client, volume_name, "healthy")
#
#     volume.engineUpgrade(image=engine_upgrade_image)
#     volume = wait_for_volume_engine_image(client, volume_name,
#                                           engine_upgrade_image)
#
#     assert volume["controller"]["engineImage"] == engine_upgrade_image
#     default_img = wait_for_engine_image_ref_count(client, default_img_name, 0)
#     new_img = wait_for_engine_image_ref_count(client, new_img_name, 1)
#
#     count = 0
#     # old replica may be in deletion process
#     for replica in volume["replicas"]:
#         if replica["engineImage"] == engine_upgrade_image:
#             count += 1
#     assert count == REPLICA_COUNT
#
#     volume = volume.detach()
#     volume = wait_for_volume_state(client, volume_name, "detached")
#     assert len(volume["replicas"]) == REPLICA_COUNT
#
#     volume = volume.attach(hostId=host_id)
#     volume = wait_for_volume_state(client, volume_name, "healthy")
#
#     volume.engineUpgrade(image=original_engine_image)
#     volume = wait_for_volume_engine_image(client, volume_name,
#                                           original_engine_image)
#     default_img = wait_for_engine_image_ref_count(client, default_img_name, 1)
#     new_img = wait_for_engine_image_ref_count(client, new_img_name, 0)
#
#     assert volume["engineImage"] == original_engine_image
#
#     assert volume["controller"]["engineImage"] == original_engine_image
#     count = 0
#     # old replica may be in deletion process
#     for replica in volume["replicas"]:
#         if replica["engineImage"] == original_engine_image:
#             count += 1
#     assert count == REPLICA_COUNT
#
#     volume = volume.detach()
#     volume = wait_for_volume_state(client, volume_name, "detached")
#     assert len(volume["replicas"]) == REPLICA_COUNT
#
#     client.delete(volume)
#     wait_for_volume_delete(client, volume_name)
#
#     client.delete(new_img)
#
#
# def test_engine_image_incompatible(clients, volume_name):  # NOQA
#     # get a random client
#     for host_id, client in clients.iteritems():
#         break
#
#     images = client.list_engine_image()
#     assert len(images) == 1
#     assert images[0]["default"]
#     assert images[0]["state"] == "ready"
#
#     cli_v = images[0]["cliAPIVersion"]
#     # cli_minv = images[0]["cliAPIMinVersion"]
#     ctl_v = images[0]["controllerAPIVersion"]
#     ctl_minv = images[0]["controllerAPIMinVersion"]
#     data_v = images[0]["dataFormatVersion"]
#     data_minv = images[0]["dataFormatMinVersion"]
#
#     fail_cli_v_image = common.get_compatibility_test_image(
#             cli_v - 1, cli_v - 1,
#             ctl_v, ctl_minv,
#             data_v, data_minv)
#     img = client.create_engine_image(image=fail_cli_v_image)
#     img_name = img["name"]
#     img = wait_for_engine_image_state(client, img_name, "incompatible")
#     assert img["state"] == "incompatible"
#     assert img["cliAPIVersion"] == cli_v - 1
#     assert img["cliAPIMinVersion"] == cli_v - 1
#     client.delete(img)
#
#     fail_cli_minv_image = common.get_compatibility_test_image(
#             cli_v + 1, cli_v + 1,
#             ctl_v, ctl_minv,
#             data_v, data_minv)
#     img = client.create_engine_image(image=fail_cli_minv_image)
#     img_name = img["name"]
#     img = wait_for_engine_image_state(client, img_name, "incompatible")
#     assert img["state"] == "incompatible"
#     assert img["cliAPIVersion"] == cli_v + 1
#     assert img["cliAPIMinVersion"] == cli_v + 1
#     client.delete(img)
#
#
# def test_engine_live_upgrade_rollback(clients, volume_name):  # NOQA
#     # get a random client
#     for host_id, client in clients.iteritems():
#         break
#
#     default_img = common.get_default_engine_image(client)
#     default_img_name = default_img["name"]
#     default_img = wait_for_engine_image_ref_count(client, default_img_name, 0)
#     cli_v = default_img["cliAPIVersion"]
#     cli_minv = default_img["cliAPIMinVersion"]
#     ctl_v = default_img["controllerAPIVersion"]
#     ctl_minv = default_img["controllerAPIMinVersion"]
#     data_v = default_img["dataFormatVersion"]
#     data_minv = default_img["dataFormatMinVersion"]
#     wrong_engine_upgrade_image = common.get_compatibility_test_image(
#             cli_v, cli_minv,
#             ctl_v, ctl_minv,
#             data_v, data_minv)
#     new_img = client.create_engine_image(image=wrong_engine_upgrade_image)
#     new_img_name = new_img["name"]
#     new_img = wait_for_engine_image_state(client, new_img_name, "ready")
#     assert new_img["refCount"] == 0
#     assert new_img["noRefSince"] != ""
#
#     default_img = common.get_default_engine_image(client)
#     default_img_name = default_img["name"]
#
#     volume = client.create_volume(name=volume_name, size=SIZE,
#                                   numberOfReplicas=2)
#     volume = wait_for_volume_state(client, volume_name, "detached")
#     default_img = wait_for_engine_image_ref_count(client, default_img_name, 1)
#
#     original_engine_image = volume["engineImage"]
#     assert original_engine_image != wrong_engine_upgrade_image
#
#     volume = volume.attach(hostId=host_id)
#     volume = wait_for_volume_state(client, volume_name, "healthy")
#
#     volume.engineUpgrade(image=wrong_engine_upgrade_image)
#     with pytest.raises(Exception):
#         # this will timeout
#         wait_for_volume_engine_image(client, volume_name,
#                                      wrong_engine_upgrade_image)
#
#     # rollback
#     volume.engineUpgrade(image=original_engine_image)
#     wait_for_volume_engine_image(client, volume_name,
#                                  original_engine_image)
#
#     volume = common.wait_for_volume_replica_count(client, volume_name,
#                                                   REPLICA_COUNT)
#     assert volume["state"] == "healthy"
#
#     client.delete(volume)
#     wait_for_volume_delete(client, volume_name)
#
#     client.delete(new_img)
