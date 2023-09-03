"""This module contains the implementation of the RentedDevice class, which represents a rented device
and its usage for generating document positions. The class is designed to calculate and generate
document positions based on the device's consumption compared to its settings.
"""
from json import load

from templates.template import get_document_position


class RentedDevice:
    """Class representing a rented device and its usage for generating document positions.

    This class is used to represent a rented device with attributes related to its usage and settings.
    It provides a method, `check_consumption`, to calculate and generate document positions based on
    the device's consumption.

    Attributes:
        basic_fee (float): The basic fee for renting the device.
        basic_black_copies (int): The number of basic black copies included in the rental.
        basic_color_copies (int): The number of basic color copies included in the rental.
        previous_black (int): The previous count of black copies.
        previous_color (int): The previous count of color copies.
        current_black (int): The current count of black copies.
        current_color (int): The current count of color copies.
        sn (str): The serial number of the rented device.

    Methods:
        check_consumption(): Calculate and yield document positions based on the device's consumption.
    """
    def __init__(self):
        self.settings = None

    def __call__(self, basic_fee: int, basic_black_copies: int, basic_color_copies: int, previous_black: int,
                 previous_color: int, current_black: int, current_color: int, sn: str):
        """
        Call method for initializing the device attributes.

        Args:
            basic_fee (int): The basic fee for renting the device.
            basic_black_copies (int): The number of basic black copies included in the rental.
            basic_color_copies (int): The number of basic color copies included in the rental.
            previous_black (int): The previous count of black copies.
            previous_color (int): The previous count of color copies.
            current_black (int): The current count of black copies.
            current_color (int): The current count of color copies.
            sn (str): The serial number of the rented device.
        """
        self.basic_fee = basic_fee
        self.basic_black_copies = basic_black_copies
        self.basic_color_copies = basic_color_copies
        self.previous_black = previous_black
        self.previous_color = previous_color
        self.current_black = current_black
        self.current_color = current_color
        self.sn = sn

    def _load_settings(self):
        """Load settings from 'settings.json' file and store them in the 'settings' attribute."""
        with open('settings.json', encoding='utf-8') as file:
            self.settings = load(file)

    def check_consumption(self):
        """Calculate and yield document positions based on the device's consumption.

        Yields:
            str: Document positions as formatted strings.
        """
        self._load_settings()
        black_difference = self.current_black - self.previous_black
        color_difference = self.current_color - self.previous_color
        black_over_more = black_difference - self.basic_black_copies
        color_over_more = color_difference - self.basic_color_copies

        if self.basic_color_copies != 0:
            yield get_document_position(
                option=1,
                sn=self.sn,
                description=self.settings['basic_color_text'],
                counter=self.current_black,
                additional_counter=self.current_color,
                price=self.basic_fee,
            )

        elif self.basic_color_copies == 0:
            yield get_document_position(
                option=2,
                sn=self.sn,
                description=self.settings['basic_black_text'],
                counter=self.current_black,
                price=self.basic_fee,
            )

        if black_over_more > 0:
            yield get_document_position(
                option=3,
                sn=self.sn,
                description=self.settings['extra_black_text'],
                counter=black_over_more,
                price=self.settings['price_extra_black'],
            )

        if color_over_more > 0:
            yield get_document_position(
                option=4,
                sn=self.sn,
                description=self.settings['extra_color_text'],
                counter=color_over_more,
                price=self.settings['price_extra_color'],
            )
