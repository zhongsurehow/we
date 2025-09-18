from game_prototype.game_state import Avatar, AvatarName, BonusType

# This file centralizes game data for easy modification and collaboration.

# --- Data Definitions for Gua Zone Bonuses ---
GUA_ZONE_BONUSES = {
    "乾": {"bonus": BonusType.EXTRA_AP, "desc": "+1 AP during Action Phase"},
    "坤": {"bonus": BonusType.EXTRA_QI, "desc": "+2 Qi during Qi Phase"},
    "离": {"bonus": BonusType.DRAW_CARD, "desc": "Draw 1 card during End Phase"},
    "艮": {"bonus": BonusType.HAND_LIMIT, "desc": "+2 Hand Limit"},
    "震": {"bonus": BonusType.EXTRA_INFLUENCE, "desc": "Place 1 extra influence"},
    "巽": {"bonus": BonusType.FREE_STUDY, "desc": "Perform one free Study action"},
    "坎": {"bonus": BonusType.QI_DISCOUNT, "desc": "All Qi costs are reduced by 1"},
    "兑": {"bonus": BonusType.DAO_XING_ON_TASK, "desc": "+1 Dao Xing when completing a task"},
}

# --- Avatar Definitions ---
EMPEROR_AVATAR = Avatar(
    name=AvatarName.EMPEROR,
    description="您是前朝皇室的末裔，身负着复兴王朝、再定乾坤的沉重使命。",
    ability_description="王权: 在您的“演卦阶段”，您可以花费1点AP和3点“阴阳之气”，直接在一个您已拥有影响力标记的卦区，再额外放置一个影响力标记。"
)

HERMIT_AVATAR = Avatar(
    name=AvatarName.HERMIT,
    description="您曾是名满天下的智者，却看破了红尘纷争，选择归隐山林。",
    ability_description="逍遥游: 您执行“升沉”移动时，所需花费的“阴阳之气”-1。在您的“归元阶段”，若您本回合没有放置任何“影响力标记”，您可以摸一张卦牌。"
)

# --- Game Deck Construction ---
from game_prototype.cards_data import ALL_CARDS

# The GAME_DECK is now built from all the cards defined in the cards_data package.
GAME_DECK = ALL_CARDS

# For testing purposes, we provide easy access to a specific card.
QIAN_WEI_TIAN = ALL_CARDS[0]
