Один из недавних проектов на Python. Его цель - облегчить заказчику рассылку по разным чатам в Telegram. 
В проект также входил непосредственно бот на pyrogram, совершающий рассылку, и бот на aiogram с применением aiogram-dialog и aiohttp для запросов к веб-сервису, осуществляющий управление списком чатов, раздачей команд на рссылку. 
Два бота коммуницировали посредством RabbitMQ, а данный веб-сервис принимал запросы от бота-менеджера: управлял базой данных аккаунтов для бота-рассыльщика и базой данных чатов под каждый проект заказчика
