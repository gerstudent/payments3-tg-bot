from aiogram import Router, types, Bot, F
from aiogram.types import Message, PreCheckoutQuery
from aiogram.filters import Command, CommandStart
from config_data.config import load_config
from lexicon.lexicon import LEXICON

router = Router()
config = load_config()
PRICE_1 = types.LabeledPrice(label='Товар 1', amount=500 * 100)


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(LEXICON['/start'])


@router.message(Command(commands='buy'))
async def payment(message: Message, bot: Bot):
    PAYMENTS_TOKEN = config.tg_bot.PAYMENTS_TOKEN
    if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await message.answer('Тестовый платеж')
    await bot.send_invoice(
        chat_id=message.chat.id,
        title=LEXICON['product_1'],
        description=LEXICON['product_1_desc'],
        payload="test-invoice-payload",
        provider_token=PAYMENTS_TOKEN,
        currency="rub",
        prices=[PRICE_1, ],
        photo_url="https://img.freepik.com/premium-vector"
                  "/pizza-logo-template-suitable-for-rest"
                  "aurant-and-cafe-logo_607277-267.jpg?w=2000",
        photo_width=512,
        photo_height=512,
        photo_size=1000,
        is_flexible=False,
        start_parameter="product-1",
    )


@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True,
                                        error_message='Ошибка при совершении платежа!')


@router.message(F.successful_payment)
async def successful_payment(message: Message):
    await message.answer('Успешный платеж')
