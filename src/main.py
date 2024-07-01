from src.views import main_page_info


def main() -> None:
    user_data = input("Введите текущую дату и время в формате YYYY-MM-DD HH:MM:SS ")
    print(main_page_info(user_date=user_data))
    print("---------- ---------- ----------")


if __name__ == "__main__":
    main()
