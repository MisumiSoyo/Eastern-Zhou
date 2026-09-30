void FreeHanzu(int playerId = -1, int Time = -1)
{
    int HanzuPeriod = 120;
    if (xsPlayerAttribute(playerId, EzsAttrFlag1) < 1)
        return;
    int Timer = minInt(xsPlayerAttribute(playerId, EzsAttrTimer1) + 1, HanzuPeriod);

    if ((Timer >= HanzuPeriod) && (isPopLeft(playerId)))
    {
        SpawnUnit(playerId, EzsHanzuID, TownCenterID, 5, 1);
        Timer = Timer - HanzuPeriod;
    }
    SetResource(playerId, EzsAttrTimer1, Timer);
}



void TimerEvent(int playerId = -1, int Time = -1)
{
    int playerCiv = xsGetPlayerCivilization(playerId);

    switch (playerCiv)
    {
        case cJurchens:
        {
            break;
        }
        case cKoreans:
        {
            FreeHanzu(playerId, Time);
            break;
        }
        default:
        {
            break;
        }
    }
}


void EffectFunction10000(int playerId = -1)
{
    int Time = xsGetGameTime();
    int i = 0;
    for (i = 0; <= xsGetNumPlayers())
        if (xsPlayerAttribute(i, EzsAttrLastRuleTime) <= Time)
        {
            TimerEvent(i, Time);
            SetResource(i, EzsAttrLastRuleTime, Time + 1);
        }
}