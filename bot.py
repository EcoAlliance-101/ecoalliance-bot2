import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Inserted bot config
BOT_TOKEN = "7895504257:AAFW_zU3EiS_avZCAYX5JFPMxMz3uJHHeNk"
ADMIN_ID = 7281379919
GROUP_ID = -1002844977077

# Logging
logging.basicConfig(level=logging.INFO)

# Bot and Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# /start command handler
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.answer("🌱 Welcome to EcoAlliance Bot!\nUse /submit to list your property.")

# /submit command handler
@dp.message_handler(commands=["submit"])
async def ask_details(message: types.Message):
    await message.answer("📋 Please send your property details as a photo with a caption.\n\nFormat:\n🏠 Title\n📍 Location\n💰 Price\n📞 Contact")

# Handle photo submission with caption
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_submission(message: types.Message):
    caption = message.caption or "No details provided"
    user = message.from_user.username or message.from_user.full_name

    # Forward to admin
    await bot.send_photo(ADMIN_ID, photo=message.photo[-1].file_id,
                         caption=f"📢 New Property Submission:\n{caption}\n👤 From: @{user}")

    # Optionally forward to group
    await bot.send_photo(GROUP_ID, photo=message.photo[-1].file_id,
                         caption=f"🏠 New Listing from @{user}:\n{caption}")

    await message.answer("✅ Your property was submitted successfully!")

# Start polling
if __name__ == '__main__':
    executor.start_polling(dp)
