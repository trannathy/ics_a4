from pathlib import Path
import unittest

from ds_client import DSUServerError
import ds_messenger
import Profile

class TestProtocol(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.dm = ds_messenger.DirectMessenger()
        self.dm.dsuserver = "168.235.86.101"
        self.dm.username = "thynt1"
        self.dm.password = "206060"

        self.dm_invalid = ds_messenger.DirectMessenger()
        self.dm_invalid.dsuserver = "168.235.86.101"
        self.dm_invalid.username = "thynt1"
        self.dm_invalid.password = "wrong_pass"

        self.wrong_server = ds_messenger.DirectMessenger()
        self.wrong_server.dsuserver = "168.235.86.100"
        self.wrong_server.username = "thynt1"
        self.wrong_server.password = "206060"

        self.dm_empty = ds_messenger.DirectMessenger()
    
    def test_connect_dm(self):
        self.assertIsInstance(self.dm.connect_dm(False), dict)
        self.assertRaises(DSUServerError, lambda: self.dm_invalid.connect_dm(False))
        self.assertRaises(DSUServerError, lambda: self.wrong_server.connect_dm(False))
        self.assertRaises(DSUServerError, lambda: self.dm_empty.connect_dm(False))

    def test_send(self):
        self.assertTrue(self.dm.send("nathalien", "hi"))
        #not testing empty message because the function is never called when empty
        self.assertFalse(self.dm_invalid.send("nathalien", "hi"))
        self.assertFalse(self.wrong_server.send("nathalien", "hi"))
        self.assertFalse(self.dm_empty.send("nathalien", "hi"))
    
    def test_get_messages_list(self):
        self.assertIsInstance(self.dm.get_messages_list(self.dm.connect_dm(False)["conn"], self.dm.connect_dm(False)["token"], True, False), list)
        self.assertIsInstance(self.dm.get_messages_list(self.dm.connect_dm(False)["conn"], self.dm.connect_dm(False)["token"], False, False), list)
        self.assertRaises(DSUServerError, lambda: self.dm_invalid.get_messages_list(self.dm_invalid.connect_dm(False)["conn"], self.dm_invalid.connect_dm(False)["token"], True, False))
        self.assertRaises(DSUServerError, lambda: self.dm_invalid.get_messages_list(self.dm_invalid.connect_dm(False)["conn"], self.dm_invalid.connect_dm(False)["token"], False, False))
        self.assertRaises(DSUServerError, lambda: self.wrong_server.get_messages_list(self.wrong_server.connect_dm(False)["conn"], self.wrong_server.connect_dm(False)["token"], True, False))
        self.assertRaises(DSUServerError, lambda: self.wrong_server.get_messages_list(self.wrong_server.connect_dm(False)["conn"], self.wrong_server.connect_dm(False)["token"], False, False))
        self.assertRaises(DSUServerError, lambda: self.dm_empty.get_messages_list(self.dm_empty.connect_dm(False)["conn"], self.dm_empty.connect_dm(False)["token"], True, False))
        self.assertRaises(DSUServerError, lambda: self.dm_empty.get_messages_list(self.dm_empty.connect_dm(False)["conn"], self.dm_empty.connect_dm(False)["token"], False, False))

    def test_retrieve_new(self):
        self.assertIsInstance(self.dm.retrieve_new(False), list)
        self.assertIsNone(self.dm_invalid.retrieve_new(False))
        self.assertIsNone(self.wrong_server.retrieve_new(False))
        self.assertIsNone(self.dm_empty.retrieve_new(False))

    def test_retrieve_all(self):
        self.assertIsInstance(self.dm.retrieve_all(False), list)
        self.assertIsNone(self.dm_invalid.retrieve_all(False))
        self.assertIsNone(self.wrong_server.retrieve_all(False))
        self.assertIsNone(self.dm_empty.retrieve_all(False))

    def test_save_dms_local(self):
        directory = Path(".")
        file_name = Path(self.dm.username + ".dsu")
        all_test_path = directory / file_name
    
        if not all_test_path.exists():
            all_test_path.touch()
            dm_prof = Profile.Profile(self.dm.dsuserver, self.dm.username,
                                       self.dm.password)
            dm_prof.save_profile

        self.assertTrue(self.dm.save_dms_local(all_test_path, True))
        self.assertTrue(self.dm.save_dms_local(all_test_path, False))
        self.assertTrue(self.dm.save_dms_local(all_test_path, msg_hist=[]))

        self.assertFalse(self.dm_invalid.save_dms_local(all_test_path, True))
        self.assertFalse(self.dm_invalid.save_dms_local(all_test_path, False))
        self.assertFalse(self.dm_invalid.save_dms_local(all_test_path, msg_hist=[]))

        self.assertFalse(self.wrong_server.save_dms_local(all_test_path, True))
        self.assertFalse(self.wrong_server.save_dms_local(all_test_path, False))
        self.assertFalse(self.wrong_server.save_dms_local(all_test_path, msg_hist=[]))

        self.assertFalse(self.dm_empty.save_dms_local(all_test_path, True))
        self.assertFalse(self.dm_empty.save_dms_local(all_test_path, False))
        self.assertFalse(self.dm_empty.save_dms_local(all_test_path, msg_hist=[]))


if __name__ == "__main__":
    unittest.main()
