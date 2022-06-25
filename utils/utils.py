from typing import Optional
import re
import datetime


class Validations:
    """
        Validations
    """

    @staticmethod
    def validate_email(email: Optional[str]) -> Optional[bool]:
        """
            Validate email
        :param email: string
        :return: boolean
        """
        rule = r"^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$"
        return True if re.search(rule, email) else False

    @staticmethod
    def validate_phone_number(phone_number: Optional[str]) -> Optional[bool]:
        """
            Validate phone number
        :param phone_number: string
        :return: boolean
        """
        rule = r"^\+(998)[0-9]{9}$"
        return True if re.search(rule, phone_number) else False

    @staticmethod
    def validate_date(date: Optional[str]) -> Optional[bool]:
        """
            Validate date
        :param date: string
        :return: boolean
        """
        try:
            datetime.datetime.strptime(date, "%d.%m.%Y")
            return True
        except Exception as e:
            print(e)
            return False


if __name__ == "__main__":
    # Validate date
    validator = Validations()
    print("Mail Validation\n", validator.validate_email("baxromov_shahzodbek@gmail.com"), "\n--------------------")
    phone = "+998901234567"
    print("Phone Validation\n", validator.validate_phone_number(phone), "\n--------------------")
    print(len(phone))
    print("Date Validation\n", validator.validate_date("20.02.1000"), "\n--------------------")