import collections
from typing import NamedTuple

# A named tuple is a good way to represent a task
class YaoCiTask(NamedTuple):
    level: str
    name: str
    description: str
    reward_dao_xing: int
    reward_cheng_yi: int

class GuaCard:
    """Represents a Gua Card with its 6 Yao Ci tasks."""
    def __init__(self, name: str, associated_guas: tuple[str, str], tasks: list[YaoCiTask]):
        if len(tasks) != 6:
            raise ValueError("A GuaCard must have exactly 6 tasks.")
        self.name = name
        self.associated_guas = associated_guas
        # Tasks are ordered from bottom (index 0, 初爻) to top (index 5, 上爻)
        self.tasks = tasks

# --- Card Definitions ---

# Here we define the "乾为天" card based on our design document.
# Note: The rewards here are for *completing* the task. The effect of the task
# (e.g., gaining 3 Dao Xing for '潛龍勿用') would be implemented in the action logic.
qian_wei_tian_tasks = [
    YaoCiTask(level='地', name='初九：潜龙勿用。',
              description='在您的回合中，您可以选择跳过您的所有行动，并获得3点“道行”和1张额外的卦牌。',
              reward_dao_xing=1, reward_cheng_yi=0),
    YaoCiTask(level='地', name='九二：见龙在田，利见大人。',
              description='当您在某个“地部卦区”放置“影响力标记”时，可以额外放置1个。',
              reward_dao_xing=1, reward_cheng_yi=0),
    YaoCiTask(level='人', name='九三：君子终日乾乾，夕惕若，厉无咎。',
              description='在您的回合结束时，若您本回合没有获得任何“道行”，则您可以获得2点“道行”。',
              reward_dao_xing=0, reward_cheng_yi=1), # As per docs, reward is 诚意
    YaoCiTask(level='人', name='九四：或跃在渊，无咎。',
              description='支付3点“道行”，您可以立即从“人部”移动至“天部”，此次移动不消耗AP。',
              reward_dao_xing=0, reward_cheng_yi=1),
    YaoCiTask(level='天', name='九五：飞龙在天，利见大人。',
              description='在您的回合中，指定另一名玩家，您可以立即获得等同于其手牌数量的“道行”。',
              reward_dao_xing=0, reward_cheng_yi=2),
    YaoCiTask(level='天', name='上九：亢龙有悔。',
              description='若您是当前“道行”最高的玩家，您必须立刻弃掉所有手牌。此为盛极而衰之兆。',
              reward_dao_xing=0, reward_cheng_yi=5),
]

QIAN_WEI_TIAN = GuaCard(
    name="乾为天",
    associated_guas=("乾", "乾"), # This is a pure gua, associated with the same zone twice
    tasks=qian_wei_tian_tasks
)

# We can create a deck of cards for the game
GAME_DECK = [
    QIAN_WEI_TIAN,
    # In a full game, more cards would be defined and added here.
    # For the prototype, one card is enough to test the mechanics.
]
