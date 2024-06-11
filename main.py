import datetime

from yandex_shadow_app.app import Yandex_shadow_app
from windows_app.windows_app import Windows
import asyncio
async def main():
    date = ''
    app = Windows()
    app2 = Yandex_shadow_app()
    while True:
        await app.show_menu()
        a = (input('Выбор:'))
        cor_list = ['1','2','3','4','5','6']
        if a in cor_list:
            a = int(a)
            match a:
                case 1:
                    try:
                        contr = input('Хотите указать дату:')
                        if contr.lower() == 'да':
                            date = input('Укажите дату:')
                            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                            app2.last_result = []
                        else:
                            date = datetime.date.today()
                        await app.show(await app2.get_shadow_between_citis(date=date))
                    except (KeyError,ValueError):
                        print('Некорректные города')
                case 2:
                    res = await app.change_city()
                    app2.city_From = res[0]
                    app2.city_To = res[1]
                case 3:
                    try:
                        trsp = input('Тип транспорта:')
                        await app.tranport_type(await app2.get_shadow_between_citis(date=date), trsp)
                    except (KeyError, UnboundLocalError):
                        print('Введены некорректные данные')
                case 4:
                    try:
                        city = input('Введите город:')
                        await app.station(await app2.get_near_station(city))
                    except (KeyError, UnboundLocalError):
                        print('Введены некорректные данные')

                case 5:
                    try:
                        city = input('Введите город:')
                        stat = input('Введите название станции:')
                        codes = await app2.get_code_station(city=city,station=stat)
                        mdict = await app2.all_stationt(code=codes)
                        await app.all_races(mdict)
                    except (KeyError, UnboundLocalError):
                        print('Введены некорректные данные')

                case 6:
                    print('Exit')
                    break
        else:
            print('некорректные данные ')

if __name__ =='__main__':

    asyncio.run(main())
