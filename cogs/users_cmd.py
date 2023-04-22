import nextcord
from nextcord.ext import commands
import aiohttp, asyncio
import json
from database.crud import add_giveaway, get_all_giveaways, get_giveaway, create_user, giveaway_add_user, delete_giveaway
import datetime, time
import random
from main import bot

#
async def edit_message(message: nextcord.Message):

	giveaway = get_giveaway(id = None, message_id = message.id)

	embed = nextcord.Embed(
		title=giveaway.prize,
		timestamp=giveaway.ends_in,
		colour=nextcord.Colour.green(),
		description="Закончится: <t:{0}:R>\nСоздатель: <@{1}>\nУчаствуют: {2}".format(
			int(time.mktime(giveaway.ends_in.timetuple())),
			giveaway.host,
			len(giveaway.entries)
		)
	)


	await message.edit(embed = embed)

class Entrie(nextcord.ui.View):
	def __init__(self):
		super().__init__()
		self.value = None

	@nextcord.ui.button(label = "Участвовать", style=nextcord.ButtonStyle.green)
	async def entrie(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

		giveaway = get_giveaway(id = None, message_id=interaction.message.id)

		for e in giveaway.entries:
			if e.user_id == interaction.user.id:
				await interaction.response.send_message("Вы уже участвуете в конкурсе", ephemeral=True)
				return None

		user = create_user(interaction.user.id, giveaway)
		giveaway_add_user(giveaway, user)

		channel = interaction.channel
		message = await channel.fetch_message(giveaway.message_id)

		await edit_message(message)





class FormModal(nextcord.ui.Modal):

	def __init__(self):
		super().__init__(
			"Создать конкурс"
		)

		self.term = nextcord.ui.TextInput(label = "Конец в... (Указывать в минутах)", min_length=1, max_length=124, required=True, placeholder="Embed")
		self.add_item(self.term)
		self.prize = nextcord.ui.TextInput(label = "Приз", min_length=2, max_length=124, required=True, placeholder="Укажите приз (текст)")
		self.add_item(self.prize)
		self.desc = nextcord.ui.TextInput(label = "Описание", min_length=4, max_length=200, required=False, placeholder="Описание конкурса", style=nextcord.TextInputStyle.paragraph)
		self.add_item(self.desc)

	async def callback(self, interaction: nextcord.Interaction) -> None:
		view = Entrie()

		ends_in = datetime.datetime.now() + datetime.timedelta(minutes = int(self.term.value))

		embed = nextcord.Embed(
			title = self.prize.value,
			timestamp= ends_in,
			colour=nextcord.Colour.green(),
			description="Закончится: <t:{0}:R>\nСоздатель: <@{1}>\nУчаствуют: 0".format(
				int(time.mktime(ends_in.timetuple())),
				interaction.user.id
			))

		message = await interaction.response.send_message('', view=view, embed=embed)
		message = await message.fetch()

		add_giveaway(
			ends_in = ends_in,
			desc = self.desc.value,
			message_id = message.id,
			channel_id = message.channel.id,
			host = interaction.user.id,
			prize=self.prize.value)




class CMDUsers(commands.Cog):

	def __init__(self, bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_ready(self):

		while True:
			giveaways = get_all_giveaways()
			for g in giveaways:
				if g.ends_in.minute == datetime.datetime.now() and g.ends_in.second == datetime.datetime.now().second and g.ends_in.hour == datetime.datetime.hour:
					channel = await bot.fetch_channel(g.channel_id)

					message = await channel.fetch_message(g.message_id)

					await channel.send("<@{0}> выиграл {1}! Поздравляем!".format(
							g.entries[random.randint(0, len(g.entries) - 1)].user_id,
							g.prize
						), delete_after=120
					)

					delete_giveaway(g)

					await message.delete()

			await asyncio.sleep(2)







	@nextcord.slash_command()
	async def create_pool(self, intr: nextcord.Interaction):
		await intr.response.send_modal(FormModal())




def setup(bot):
	bot.add_cog(CMDUsers(bot))