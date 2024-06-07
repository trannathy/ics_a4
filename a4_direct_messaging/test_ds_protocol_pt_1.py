import unittest
import time
import ds_protocol

class TestProtocol(unittest.TestCase):
    def test_get_dict_lists(self):
        self.assertEqual(ds_protocol.get_dict_lists({"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]}}),
                         (["type", "messages", "token"], ["ok", [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}], None]))
        self.assertEqual(ds_protocol.get_dict_lists({"response": {"type": "ok", "message": "", "token":"12345678-1234-1234-1234-123456789abc"}}),
                         (["type", "message", "token"], ["ok", "", "12345678-1234-1234-1234-123456789abc"]))
        self.assertIsInstance(ds_protocol.get_dict_lists({"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]}}),
                                                         tuple)

    def test_json_to_dict(self):
        self.assertEqual(ds_protocol.json_to_dict('{"response": {"type": "ok", "message": "", "token":"12345678-1234-1234-1234-123456789abc"}}'),
                         {"type": "ok", "message": "", "token":"12345678-1234-1234-1234-123456789abc"})
        self.assertEqual(ds_protocol.json_to_dict('{"response": {"type": "ok", "message": "Direct message sent"}}'),
                         {"type": "ok", "message": "Direct message sent", "token": None})
        self.assertIsNone(ds_protocol.json_to_dict('"response": {"type": "ok", "message": "", "token":"12345678-1234-1234-1234-123456789abc"}}'))

    def test_extract_json(self):
        self.assertEqual(ds_protocol.extract_json('{"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]}}'),
                         ds_protocol.Response("ok", [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}], None))
    
        self.assertEqual(ds_protocol.extract_json('{"response": {"type": "ok", "message": "", "token":"12345678-1234-1234-1234-123456789abc"}}'),
                         ds_protocol.Response("ok", "", "12345678-1234-1234-1234-123456789abc"))
        
        self.assertIsNone(ds_protocol.extract_json('{"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]}'))
        self.assertIsNone(ds_protocol.extract_json(""))
        self.assertIsInstance(ds_protocol.extract_json('{"response": {"type": "ok", "message": "Direct message sent"}}'),
                              ds_protocol.Response)

    def test_create_join_msg(self):
        self.assertEqual(ds_protocol.create_join_msg("ohhimark", "password123"),
                         '{"join": {"username": "ohhimark", "password": "password123", "token": ""}}')
        self.assertEqual(ds_protocol.create_join_msg("ohhimark", ""),
                         '{"join": {"username": "ohhimark", "password": "", "token": ""}}')
        self.assertEqual(ds_protocol.create_join_msg("", "password123"),
                         '{"join": {"username": "", "password": "password123", "token": ""}}')
        self.assertIsNotNone(ds_protocol.create_join_msg("", ""))
        self.assertIsInstance(ds_protocol.create_join_msg("", ""), str)

    def test_create_post_msg(self):
        self.assertEqual(ds_protocol.create_post_msg("Hello World!", "user_token"),
                f'{{"token": "user_token", "post": {{"entry": "Hello World!", "timestamp": "{time.time()}"}}}}')
        self.assertEqual(ds_protocol.create_post_msg("", "user_token"),
                f'{{"token": "user_token", "post": {{"entry": "", "timestamp": "{time.time()}"}}}}')
        self.assertEqual(ds_protocol.create_post_msg("Hello World!", ""),
                f'{{"token": "", "post": {{"entry": "Hello World!", "timestamp": "{time.time()}"}}}}')
        self.assertEqual(ds_protocol.create_post_msg("", ""),
                f'{{"token": "", "post": {{"entry": "", "timestamp": "{time.time()}"}}}}')
        self.assertIsNotNone(ds_protocol.create_post_msg("", ""))
        self.assertIsInstance(ds_protocol.create_post_msg("", ""), str)

    def test_create_bio_msg(self):
        self.assertEqual(ds_protocol.create_bio_msg("Hello World!", "user_token"),
                        f'{{"token": "user_token", "bio": {{"entry": "Hello World!", "timestamp": "{time.time()}"}}}}')
        self.assertEqual(ds_protocol.create_bio_msg("", "user_token"),
                        f'{{"token": "user_token", "bio": {{"entry": "", "timestamp": "{time.time()}"}}}}')
        self.assertEqual(ds_protocol.create_bio_msg("Hello World!", ""),
                        f'{{"token": "", "bio": {{"entry": "Hello World!", "timestamp": "{time.time()}"}}}}')
        self.assertEqual(ds_protocol.create_bio_msg("", ""),
                        f'{{"token": "", "bio": {{"entry": "", "timestamp": "{time.time()}"}}}}')
        self.assertIsNotNone(ds_protocol.create_bio_msg("", ""))
        self.assertIsInstance(ds_protocol.create_bio_msg("", ""), str)

    def test_create_send_dm_message(self):
        self.assertEqual(ds_protocol.create_send_dm_message("Hello World!", "ohhimark", "user_token"),
                        f'{{"token": "user_token", "directmessage": {{"entry": "Hello World!", "recipient": "ohhimark", "timestamp": "{time.time()}"}}}}')
        self.assertIsNotNone(ds_protocol.create_send_dm_message("", "", ""))

    def test_create_unread_dm_message(self):
        self.assertEqual(ds_protocol.create_unread_dm_message("user_token"),
                         '{"token": "user_token", "directmessage": "new"}')
        self.assertIsNotNone(ds_protocol.create_unread_dm_message(""))

    def test_create_all_dm_message(self):
        self.assertEqual(ds_protocol.create_all_dm_message("user_token"),
                         '{"token": "user_token", "directmessage": "all"}')
        self.assertIsNotNone(ds_protocol.create_all_dm_message(""))

    def test_get_msg_list_from_json(self):
        self.assertEqual(ds_protocol.get_msg_list_from_json('{"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]}}'),
                         [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}])
        self.assertIsNotNone(ds_protocol.get_msg_list_from_json('{"response": {"type": "ok", "messages": []}}'))
        self.assertIsInstance(ds_protocol.get_msg_list_from_json('{"response": {"type": "ok", "messages": []}}'), list)
    
    def test_interpet_svr_message_list(self):
        self.assertIsNone(ds_protocol.print_messages([{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]))

    def test_interpret_svr_message_list(self):
        self.assertEqual(ds_protocol.interpret_svr_message_list('{"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]}}'),
                         [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}])
        self.assertIsNotNone(ds_protocol.interpret_svr_message_list('{"response": {"type": "ok", "messages": []}}'))
        self.assertIsInstance(ds_protocol.interpret_svr_message_list('{"response": {"type": "ok", "messages": []}}'), list)

if __name__ == "__main__":
    unittest.main()
