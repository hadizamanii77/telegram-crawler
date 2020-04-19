import csv
import os

from pathlib import Path
from datetime import datetime
from global_utils.make_dir import DirectoryMaker


class MessageSaver(DirectoryMaker):

    def __init__(self, channel):
        result_dir = os.path.join(Path(__file__).parent.parent, "result")
        self.result_dir = self.make_dir(result_dir)
        date = str(datetime.date(datetime.now()))
        subdir_date_path = os.path.join(self.result_dir, date)
        self.date_dir = self.make_dir(subdir_date_path)
        self.channel = channel.split('/')[-1]
        self.channel_result_address = '{}.csv'.format(os.path.join(self.date_dir, self.channel))
        self.clean_channel_result_file()
        self.row_name = ['date', 'message']

    def clean_channel_result_file(self):
        if os.path.isfile(self.channel_result_address):
            os.remove(self.channel_result_address)

    def save_messages(self, messages):

        with open(self.channel_result_address, 'a') as file:
            writer = csv.DictWriter(file, fieldnames=self.row_name)
            for message in messages:
                writer.writerow(self.serialize_data(message))

    @staticmethod
    def serialize_data(message):
        return {
            'date': message.date,
            'message': message.message
        }
