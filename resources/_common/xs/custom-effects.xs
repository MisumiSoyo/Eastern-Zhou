include "array.xs";
include "math.xs";
include "tech-adjustment.xs";
include "techtree.xs";
include "timer.xs";



//  10005 - Suanfu
void EffectFunction10005(int playerId = -1)
{
    xsResetTaskAmount();
    xsTaskAmount(cTaskAttrSearchWaitTime, 0.000001);
    xsTaskAmount(cTaskAttrProductivityResource, EzsAttrSuanfuProductivity);
    xsTaskAmount(cTaskAttrResourceOut, cAttributeGold);
    xsTaskAmount(cTaskAttrWorkValue1, 0.01);
    xsTaskAmount(cTaskAttrCombatLevelFlag, 2);
    ApplyAllToTarget(playerId, -1, cTaskTypeGenerateResources);
    xsResetTaskAmount();
    ModResource(playerId, EzsAttrSuanfuProductivity, 2.5);
}


//  10006 - Che Bin
void EffectFunction10006(int playerId = -1)
{
    xsResetTaskAmount();
    xsTaskAmount(cTaskAttrSearchWaitTime, 5.000001);
    xsTaskAmount(cTaskAttrWorkValue1, 1.15);
    xsTaskAmount(cTaskAttrWorkValue2, 1);
    xsTaskAmount(cTaskAttrWorkRange, 5);
    xsTaskAmount(cTaskAttrOwnerType, 1);
    xsTaskAmount(cTaskAttrCombatLevelFlag, 3);
    xsTask(EzsWarChariotID, cTaskTypeAura, cInfantryClass, playerId);
    xsTask(EliteEzsWarChariotID, cTaskTypeAura, cInfantryClass, playerId);
    xsTask(EzsChariotArcherID, cTaskTypeAura, cInfantryClass, playerId);
    xsTask(EliteEzsChariotArcherID, cTaskTypeAura, cInfantryClass, playerId);
    xsResetTaskAmount();
    ModAttribute(playerId, EzsWarChariotID, cCombatAbility, 32);
    ModAttribute(playerId, EliteEzsWarChariotID, cCombatAbility, 32);
    ModAttribute(playerId, EzsChariotArcherID, cCombatAbility, 32);
    ModAttribute(playerId, EliteEzsChariotArcherID, cCombatAbility, 32);
}


//  10007 - Huang Jin Tai
void EffectFunction10007(int playerId = -1)
{
    int i = 0;
    int TechCount = xsGetPlayerNumberOfTechs(playerId);
    for (i = 0; < TechCount)
        if (xsGetTechAttribute(playerId, i, cTechResearchTime) > 10)
            xsEffectAmount(cModifyTech, i, cAttrSetTime, 10, playerId);
}


//  10008 - Death Warriors
void EffectFunction10008(int playerId = -1)
{
    xsResetTaskAmount();
    xsTaskAmount(cTaskAttrSearchWaitTime, 9.000001);
    xsTaskAmount(cTaskAttrWorkValue1, 1);
    xsTaskAmount(cTaskAttrWorkValue2, 0.1);
    xsTaskAmount(cTaskAttrWorkRange, 0);
    xsTask(cInfantryClass, cTaskTypeHPModifier, -1, playerId);
    xsResetTaskAmount();
}


//  10009 - Anger of the North
void EffectFunction10009(int playerId = -1)
{
    ModAttribute(playerId, EzsYanBorderCavalryID, cFoodCost, xsGetObjectAttribute(playerId, EzsYanBorderCavalryID, cGoldCost));
    ModAttribute(playerId, EliteEzsYanBorderCavalryID, cFoodCost, xsGetObjectAttribute(playerId, EliteEzsYanBorderCavalryID, cGoldCost));
    SetAttribute(playerId, EzsYanBorderCavalryID, cGoldCost, 0);
    SetAttribute(playerId, EliteEzsYanBorderCavalryID, cGoldCost, 0);
}


//  10010 - Ji Xia Xue Gong
void EffectFunction10010(int playerId = -1)
{
    int i = 0;
    int TechCount = xsGetPlayerNumberOfTechs(playerId);
    for (i = 0; < TechCount)
        if (xsGetTechAttribute(playerId, i, cTechResearchLocation) == UniversityID)
            xsEffectAmount(cModifyTech, i, cAttrMulAllCosts, 0.67, playerId);
}



void main()
{
    xsChatData("Mod: Eastern Zhou States");
    xsChatData("Patch: 1.0b  2026.10.02");
    xsChatData("Author: Misumi Soyo");

    vector pos = xsVectorSet(0.0, 0.0, 0.0);
    int i = 0;
    for (i = 0; <= xsGetNumPlayers())
        SetAttribute(i, TimerBuildingID, cRegenerationHpPercent, -267);
    if (xsGetObjectCount(1, TimerBuildingID) <= 0)
        xsCreateUnit(TimerBuildingID, 1, pos, false, false);
}