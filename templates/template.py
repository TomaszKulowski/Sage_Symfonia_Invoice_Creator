"""This module contains functions for generating sections for the document template."""
from datetime import date, timedelta


def get_contractor(contractor_code: str) -> str:
    """Generate a contractor section for a document.

    Args:
        contractor_code (str): The code or identifier of the contractor.

    Returns:
        str: A formatted contractor section in the document.
    """
    contractor = 'Kontrahent{\n' \
                 f'\tkod = {contractor_code}\n' \
                 '}\n'

    return contractor


def get_all_contractor_data(name: str, address: str, number: str, local: str,
                            city: str, postal_code: str, tax_number: str) -> str:
    """Generate a section with all contractor data for a document.

    Args:
        name (str): The name of the contractor.
        address (str): The street address of the contractor.
        number (str): The house number of the contractor.
        local (str): The local information (if any) of the contractor.
        city (str): The city where the contractor is located.
        postal_code (str): The postal code of the contractor's location.
        tax_number (str): The tax identification number (NIP) of the contractor.

    Returns:
        str: A formatted section with all contractor data in the document.
    """
    contractor = '\tdaneKh{\n' \
                 f'\t\tKhKod = {name}\n' \
                 f'\t\tKhNazwa = {name}\n' \
                 f'\t\tKhUlica = {address}\n' \
                 f'\t\tKhDomu = {number}\n' \
                 f'\t\tKhLokal = {local}\n' \
                 f'\t\tKhMiasto = {city}\n' \
                 f'\t\tKhPoczta = {postal_code}\n' \
                 f'\t\tKhKodPocz = {postal_code}\n' \
                 f'\t\tKhNIP = {tax_number}\n' \
                 '\t\tkraj{\n' \
                 '\t\t\tsymbol = PL\n' \
                 '\t\t}\n' \
                 '\t}\n'

    return contractor


def get_document_date(due_days: int) -> str:
    """Generate a section with document dates and payment terms for a document.

    Args:
        due_days (int): The number of days until the payment is due.

    Returns:
        str: A formatted section with document dates and payment terms in the document.
    """
    current_date = date.today()
    due_date = current_date + timedelta(days=due_days)
    document_date = f'\tdataWystawienia = {current_date.strftime("%Y-%m-%d")}\n' \
                    f'\tdataRejestrVAT = {current_date.strftime("%Y-%m-%d")}\n' \
                    f'\tterminPlatnosci = {due_date.strftime("%Y-%m-%d")}\n' \
                    '\tformaPl{\n' \
                    '\t\tnazwa = przelew\n' \
                    f'\t\ttermin = {due_days}\n' \
                    '\t}\n'

    return document_date


def get_document_template(description: str, price: float, quantity: float) -> str:
    """Generate a section for a document template with item details.

    Args:
        description (str): The description or name of the item.
        price (float): The price of the item.
        quantity (float): The quantity of the item.

    Returns:
        str: A formatted section with item details in the document template.
    """
    position = '\tPozycja dokumentu{\n' \
               '\t\tkod =dzierzawa\n' \
               '\t\tNazwa_Dl{\n' \
               f'\t\t\topis ={description}\n' \
               '\t\t}\n' \
               f'\t\tcena ={price}\n' \
               f'\t\tilosc ={quantity}\n' \
               '\t\tjednostkaMiary =szt\n' \
               '\t}\n' \

    return position


def get_document_position(option: int, sn: str, description: str, counter: int, price: float, additional_counter: int = None):
    """Generate a document position based on the specified options.

    Args:
        option (int): The option to determine the position type.
        sn (str): The serial number of the item.
        description (str): The description template for the item.
        counter (int): The main counter value.
        price (float): The price of the item.
        additional_counter (int, optional): An additional counter value (used for color copies).

    Returns:
        str: A formatted document position based on the specified options.
    """
    description = description.replace('$sn$', sn)
    price = float(price)
    if option == 1:
        quantity = 1.0
        description = description.replace('$current_black_counter$', str(counter))\
            .replace('$current_color_counter$', str(additional_counter))
    elif option == 2:
        quantity = 1.0
        description = description.replace('$current_black_counter$', str(counter))
    elif option == 3:
        quantity = float(counter)
    elif option == 4:
        quantity = float(counter)

    position = get_document_template(description, price, quantity)
    return position
