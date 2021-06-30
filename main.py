import sc2
from sc2 import run_game, maps, Race, Difficulty, UnitTypeId
from sc2.player import Bot, Computer


class SelketBot(sc2.BotAI):

    async def print_info(self):
        print(">> 资产: %d 晶体矿, %d 高能瓦斯" % (self.minerals, self.vespene));

    async def build_workers(self):
        larvas = self.units(UnitTypeId.LARVA)

        # 如果能够支付的起工人
        if self.can_afford(UnitTypeId.DRONE) and larvas.exists and self.units(UnitTypeId.DRONE).amount < 36:
            print(">> 检测到 可训练工人, 即将训练工人.")
            # 让该目标制造一个工人
            larvas.random.train(UnitTypeId.DRONE)

    async def build_supply(self):
        if self.supply_left == 0:
            print(">> 没有任何补给, 即将训练补给")
            larvas = self.units(UnitTypeId.LARVA)

            if self.can_afford(UnitTypeId.OVERLORD) and larvas.exists:
                larvas.random.train(UnitTypeId.OVERLORD)

    async def expand(self):
        if self.units(UnitTypeId.HATCHERY).amount < 3 and self.can_afford(
                UnitTypeId.HATCHERY) and not self.already_pending(UnitTypeId.HATCHERY):
            await self.expand_now()

    async def on_start(self):
        print(">> 游戏已开始.");

    # 每个游戏刻中进行的操作.
    async def on_step(self, iteration: int):

        print(">> On Step()");

        # 输出当前的游戏信息
        await self.print_info()

        # 分配工人
        await self.distribute_workers()

        # 建造工人
        await self.build_workers()

        # 建造补给
        await self.build_supply()


# 启动游戏
run_game(maps.get("Abyssal Reef LE"), [
    Bot(Race.Zerg, SelketBot()),
    Computer(Race.Protoss, Difficulty.Medium)
], realtime=True)
