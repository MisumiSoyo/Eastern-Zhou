include "custom-constants.xs";
include "math.xs";


void ezsChooseFeudal()
{
    int playerId = xsGetGoal(512);
    int civ = xsGetPlayerCivilization(playerId);
    int TechStartID = xsPlayerAttribute(playerId, EzsSelectTechStartID);
    if (TechStartID == 0)
        return;

    int TownCenterUnitID = xsArrayGetInt(xsGetPlayerUnitIds(playerId, TownCenterID), 0);
    if (RandomChance(50))
        xsInitiateResearch(TownCenterUnitID, TechStartID);
    else
        xsInitiateResearch(TownCenterUnitID, TechStartID + 1);
}


void ezsChooseCastle()
{
    int playerId = xsGetGoal(512);
    int civ = xsGetPlayerCivilization(playerId);
    int TechStartID = xsPlayerAttribute(playerId, EzsSelectTechStartID);
    if (TechStartID == 0)
        return;

    int TownCenterUnitID = xsArrayGetInt(xsGetPlayerUnitIds(playerId, TownCenterID), 0);
    if (RandomChance(50))
        xsInitiateResearch(TownCenterUnitID, TechStartID + 2);
    else
        xsInitiateResearch(TownCenterUnitID, TechStartID + 3);
}


void ezsChooseImperial()
{
    int playerId = xsGetGoal(512);
    int civ = xsGetPlayerCivilization(playerId);
    int TechStartID = xsPlayerAttribute(playerId, EzsSelectTechStartID);
    if (TechStartID == 0)
        return;

    int TownCenterUnitID = xsArrayGetInt(xsGetPlayerUnitIds(playerId, TownCenterID), 0);
    if (RandomChance(50))
        xsInitiateResearch(TownCenterUnitID, TechStartID + 4);
    else
        xsInitiateResearch(TownCenterUnitID, TechStartID + 5);
}
