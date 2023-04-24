from app.bot.dataclasses import BotCommand


commands = {
    "animal": BotCommand(
        name="animal",
        description="Команда для получения картинки с животными.",
        usage="По умолчанию - случайная картинка. Варианты:\n"
        "/animal рисунок - рисунок милых животных от нейросети.\n"
        "/animal кошка - случайное фото кошки.\n"
        "/animal кошара - случайное фото большой кошки.\n"
        "/animal собака - фото собачек.\n"
        "/animal лиса - фото лисичек.\n",
    ),
}
