# Source code of the Ubuntu-it website
# Copyright (C) 2024 Mattia Allegro <info@shadmod.it>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import random
import string
from datetime import datetime

import requests

from constants import DATETIME_FORMAT, MESSAGE_NOT_FOUND
from type_dict import AttachmentTypedDict


class TempMail:
    URL_MAIL = "https://www.1secmail.com/api/v1/?action="
    DOMAIN_LIST: list[str] = ["com", "org", "net"]
    LENGTH: int = 10

    def __init__(
        self,
        username: str | None,
        choice_domain: str | None = None,
    ):
        self.username = username if username else self.generate_random_username
        if choice_domain and choice_domain in self.DOMAIN_LIST:
            self.domain = f"1secmail.{choice_domain}"
        else:
            self.domain = f"1secmail.{random.choice(self.DOMAIN_LIST)}"

    @property
    def generate_random_username(self) -> str:
        """Generate a random username.

        Returns:
            str: Returns a random username.
        """
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for _ in range(self.LENGTH))

    @property
    def create_temp_email(self) -> str:
        """Create a temporary email.

        Returns:
            str: Returns a temporary email.
        """
        return f"{self.username}@{self.domain}"

    def get_messages(self) -> list[dict[str, str | int]]:
        """Retrieve all messages for temporary email

        Returns:
            list[dict[str, str | int]]: Returns a list of messages.
        """
        url = f"{self.URL_MAIL}getMessages&login={self.username}&domain={self.domain}"
        response = requests.get(url)
        return response.json()

    def get_all_messages_id(self) -> list[int]:
        """Retrieve all messages ID for temporary email.

        Returns:
            list[int]: Returns a list of messages ID.
        """
        message_id_list = [
            message["id"] for message in self.get_messages() if "id" in message
        ]
        return message_id_list

    def read_message(self, message_id: int) -> dict[str, str | int]:
        """Reads the content of a specific message ID

        Args:
            message_id (int): Message ID.

        Returns:
            dict[str, str | int]: Returns a dictionary of specific message.
        """
        url = f"{self.URL_MAIL}readMessage&login={self.username}&domain={self.domain}&id={message_id}"
        response = requests.get(url)
        if response.content.decode("utf-8") == MESSAGE_NOT_FOUND:
            return response.content.decode("utf-8")
        return response.json()

    def get_message_body(self, message_id: int) -> str:
        """Retrieve the body of a specific message ID.

        Args:
            message_id (int): Message ID.

        Returns:
            str: Returns the body of a specific message.
        """
        if isinstance(self.read_message(message_id), str):
            return self.read_message(message_id)
        return self.read_message(message_id).get("body", "No body")

    def get_message_from(self, message_id: int) -> str:
        """Retrieve who sent the message from a specific message ID.

        Args:
            message_id (int): Message ID.

        Returns:
            str: Returns who sent the message.
        """
        if isinstance(self.read_message(message_id), str):
            return self.read_message(message_id)
        return self.read_message(message_id).get("from", "No from")

    def get_message_date(self, message_id: int) -> datetime:
        """Retrieve the date of a specific message ID.

        Args:
            message_id (int): Message ID.

        Returns:
            datetime: Returns the date of a specific message.
        """
        if isinstance(self.read_message(message_id), str):
            return self.read_message(message_id)
        date_as_str = self.read_message(message_id).get("date", "No date")
        return datetime.strptime(date_as_str, DATETIME_FORMAT)

    def get_message_subject(self, message_id: int) -> str:
        """Retrieve the subject of a specific message ID.

        Args:
            message_id (int): Message ID.

        Returns:
            str: Returns the subject of a specific message.
        """
        if isinstance(self.read_message(message_id), str):
            return self.read_message(message_id)
        return self.read_message(message_id).get("subject", "No subject")

    def get_message_attachments(self, message_id: int) -> list[AttachmentTypedDict]:
        """Retrieve all attachments of a specific message ID.

        Args:
            message_id (int): Message ID.

        Returns:
            list[AttachmentTypedDict]: Returns a list of attachments.
        """
        if isinstance(self.read_message(message_id), str):
            return self.read_message(message_id)
        return self.read_message(message_id).get("attachments", [])

    def download_message_attachment(self, message_id: int, filename: str) -> bytes:
        """Download an attachment of a specific message ID and filename.

        Args:
            message_id (int): Message ID.
            filename (str): Filename of the attachment.

        Returns:
            bytes: Returns a bytes attachment.
        """
        url = f"{self.URL_MAIL}download&login={self.username}&domain={self.domain}&id={message_id}&file={filename}"
        response = requests.get(url)
        return response.content
