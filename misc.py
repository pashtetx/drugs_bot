

async def message_formatter(data: dict):

	if data['earthCycle']['isDay']:
		return (f"В цетусе день! ({ data['earthCycle']['timeLeft'] } осталось)")
	else:
		return (f"В цетусе ночь! ({ data['earthCycle']['timeLeft'] } осталось)")

	if data["voidTrader"]["active"]:
		return (f"Баро КиТир появился в { data['voidTrader']['location'] }")
