from yandex_shadow_app.app import Yandex_shadow_app


class Windows:
    @classmethod
    async def change_city(cls):
        b = input('Город отправки:')
        c = input('Город прибытия:')
        return [b,c]
    @classmethod
    async def show_menu(cls):
        print('1 - Расписание между городами')
        print('2 -  Сменить города')
        print('3 - Рейсы с определенным транспортом')
        print('4 - Станции в городе')
        print('5 - Все рейсы станции')
        print('6 - Выход')

    @classmethod
    async def tranport_type(cls,mlist,trsp):
        shd = mlist
        for race in shd:
            if race['Транспорт'] == trsp:
                for key, value in race.items():
                    print(key, '-', value)
                print()
                print()

    async def all_races(self,mdict):

        print('Рейсы для выбранной станции:')
        for i in mdict['schedule']:
            print(f'    {i['thread']['title']}')
        print()
        print()
    @classmethod
    async def station(cls, mlist):
        print()
        for i in range(len(mlist['stations'])):
            print(f'{i+1}-{mlist['stations'][i]['title']}')
        print()
        print()
    @classmethod
    async def show(cls, mlist):
        shd = mlist
        for race in shd:
            for key, value in race.items():
                print(key, '-', value)
            print()
            print()

        # f'From:{shd['segments'][0]['from']['title']}\n'\
        #                 f'To:{shd['segments'][0]['to']['title']}\n'\
        #                 f'Transport:{shd['segments'][0]['from']['transport_type']}\n'\
        #                 # f'Price:{shd['segments'][0]['tickets_info']['places'][0]['price']['whole']}'


