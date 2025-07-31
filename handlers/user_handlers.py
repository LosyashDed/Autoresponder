import logging
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command

from keyboards.reply import get_main_keyboard
from keyboards.inline import get_contact_keyboard, get_channel_keyboard
from config import Config
from services import CONSULTATION_TYPES

user_router = Router()

@user_router.message(CommandStart(), flags={"subscription": True})
async def cmd_start(message: Message):
    await message.answer(
        "Здравствуйте! Выберите интересующий вас вид консультации:",
        reply_markup=get_main_keyboard()
    )

@user_router.message(Command(commands=["help"]), flags={"subscription": True})
async def cmd_help(message: Message):
    await cmd_start(message)

@user_router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: CallbackQuery, bot: Bot, config: Config):
    user_id = callback.from_user.id
    
    member = await bot.get_chat_member(chat_id=config.channel_id, user_id=user_id)
    
    if member.status in ['member', 'administrator', 'creator']:
        await callback.message.delete()
        await callback.answer("Спасибо за подписку! Ваш подарок уже в пути.", show_alert=True)
        try:
            await bot.send_document(user_id, document=FSInputFile('gift.pdf'))
            pass
        except Exception as e:
            logging.error(f"Failed to send gift to user {user_id}: {e}")
            pass
        
        await cmd_start(callback.message)
    else:
        await callback.answer(
            "Вы еще не подписались. Пожалуйста, подпишитесь на канал и нажмите кнопку ниже.",
            show_alert=True
        )

@user_router.message(F.text.in_(CONSULTATION_TYPES))
async def consultation_handler(message: Message):
    match message.text:
        case "Звонок - знакомство":
            await message.answer(
                """Первичная встреча проходит онлайн в формате видеозвонка и занимает 15–20 минут.

Цель — увидеться, почувствовать, комфортно ли нам общаться, и помочь вам трезво решить, хотите ли продолжить сотрудничество.

Звонок полностью бесплатный, но мы заранее договариваемся о подходящем времени.

Во время беседы я предложу вам коротко обозначить, что сейчас беспокоит, с какими трудностями сталкиваетесь и какого результата ждёте от терапии.

В ответ я расскажу, где действительно смогу помочь, что выходит за рамки моей компетенции и как обычно строится дальнейшая совместная работа.""",
                reply_markup=get_contact_keyboard()
            )
        case "Консультация":
            await message.answer(
                """Консультация проходит в виде единственной самостоятельной встречи и идеально подходит, если вы по-каким-то причинам пока не готовы к долгосрочной терапии.

За отведённое время вы сможете открыто рассказать о своих переживаниях и сложностях. Я помогу взглянуть глубже: разберём, откуда берётся трудность, как она «подпитывается» и какие есть альтернативные способы её воспринимать.

Кроме того, я проведу краткое психообразование и дам практические советы.

Стоимость: 4000 ₽ за час либо 5000 ₽ за двухчасовой формат.""",
                reply_markup=get_contact_keyboard()
            )
        case "Психотерапия":
            await message.answer(
                """Психотерапевтические встречи рассчитаны на тех, кто страдает тревогой либо другими внутренними сложностями и уже понял, что в одиночку справиться не получается.

Работа строится при вашем полном участии: мы вместе исследуем привычные схемы мыслей и действий, а затем вы закрепляете новое, выполняя подобранные под вас упражнения между сессиями. Без такой личной вовлечённости ждать результатов бессмысленно.

Главная задача процесса — дать вам практические инструменты, с помощью которых вы сами сможете корректировать эмоции, поведение и образ мышления в повседневной жизни.

Стоимость одной часовой сессии — 4000 рублей.""",
                reply_markup=get_contact_keyboard()
            )
        case "Консультация с ИИ":
            await message.answer(
                """Гибридная сессия сочетает экспертность психолога и вычислительную мощь искусственного интеллекта.

Сначала мы чётко формулируем ваш запрос, определяем конкретную цель и фиксируем препятствия, мешающие прогрессу.

Затем ИИ обрабатывает собранные данные, выявляет скрытые связи и, опираясь на принципы КПТ, предлагает детальный план действий и практические техники для преодоления барьеров.

Продолжительность встречи — 1 час, стоимость — 3500 ₽.""",
                reply_markup=get_contact_keyboard()
            )
        case "Семейная терапия":
            await message.answer(
                """Парная терапия предназначена для тех, кто хочет освоить основы результативного диалога: слышать друг друга, сокращать число ссор и возвращать эмоциональную близость.

Программа включает 10 встреч и растягивается примерно на два с половиной месяца; на каждой мы шаг за шагом отрабатываем конкретные техники улучшения общения.

Я не становлюсь на чью-то сторону и не выясняю «кто прав», а вместе с вами исследую, что скрывается за обидами и претензиями, какие реакции вызывают ваши поступки и как это изменить.

Стоимость — 45 000 ₽ за весь курс или 5 000 ₽ за разовую 90-минутную встречу.""",
                reply_markup=get_contact_keyboard()
            )


@user_router.callback_query(F.data == "contact_phone")
async def contact_phone_callback(callback: CallbackQuery, config: Config):
    await callback.message.answer(f"Чтобы связаться со мной по телефону, вы можете позвонить мне по номеру {config.contact_phone}.\n\nЕсли я не отвечаю, то скорее всего либо занята, либо вы попали в нерабочее время.\n\n В таком случае, оставьте пожалуйста сообщение на ватсап по этому же номеру и я вам отвечу сразу как только появится такая возможность.")
    await callback.answer()

@user_router.callback_query(F.data == "contact_messages")
async def contact_messages_callback(callback: CallbackQuery, config: Config):
    await callback.message.answer(f"Чтобы связаться со мной, пишите {config.contact_username}\n\nЯ отвечу вам сразу, так только появится возможность.")
    await callback.answer()
