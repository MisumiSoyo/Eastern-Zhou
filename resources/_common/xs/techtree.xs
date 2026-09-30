include "ability.xs";



void EnableAllEconomicTechs(int playerId = -1)
{
    EnableTech(playerId, DoubleBitAxeTechID);
    EnableTech(playerId, BowSawTechID);
    EnableTech(playerId, TwoManSawTechID);
    EnableTech(playerId, HorseCollarTechID);
    EnableTech(playerId, HeavyPlowTechID);
    EnableTech(playerId, CropRotationTechID);
    EnableTech(playerId, GoldMiningTechID);
    EnableTech(playerId, StoneMiningTechID);
    EnableTech(playerId, GoldShaftMiningTechID);
    EnableTech(playerId, StoneShaftMiningTechID);
}


void EzsTechTreeAdjustment(int playerId = -1)
{
    DisableTech(playerId, GambesonsTechID);
}


// 10001 - Tech Tree Adjustment
void EffectFunction10001(int playerId = -1)
{
    int playerCiv = xsGetPlayerCivilization(playerId);

    EnableAllEconomicTechs(playerId);
    EzsTechTreeAdjustment(playerId);

    switch (playerCiv)
    {
        case cBritons:
        {
        }
        case cFranks:
        {
        }
        case cGoths:
        {
        }
        case cTeutons:
        {
        }
        case cJapanese:
        {
        }
        case cChinese:
        {
        }
        case cByzantines:
        {
        }
        case cPersians:
        {
            break;
        }
        case cSaracens:
        {
            break;
        }
        case cTurks:
        {
            break;
        }
        case cVikings:
        {
            break;
        }
        case cMongols:
        {
            break;
        }
        case cCelts:
        {
            break;
        }
        case cSpanish:
        {
            break;
        }
        case cAztecs:
        {
            break;
        }
        case cMayans:
        {
            break;
        }
        case cHuns:
        {
            break;
        }
        case cKoreans:
        {
            break;
        }
        case cItalians:
        {
            break;
        }
        case cIndians:
        {
            break;
        }
        case cIncas:
        {
            break;
        }
        case cMagyars:
        {
            break;
        }
        case cSlavs:
        {
            break;
        }
        case cPortuguese:
        {
            break;
        }
        case cEthiopians:
        {
            break;
        }
        case cMalians:
        {
            break;
        }
        case cBerbers:
        {
            break;
        }
        case cKhmer:
        {
            break;
        }
        case cMalay:
        {
            break;
        }
        case cBurmese:
        {
            break;
        }
        case cVietnamese:
        {
            break;
        }
        case cBulgarians:
        {
            break;
        }
        case cTatars:
        {
            break;
        }
        case cCumans:
        {
            break;
        }
        case cLithuanians:
        {
            break;
        }
        case cBurgundians:
        {
            break;
        }
        case cSicilians:
        {
            break;
        }
        case cPoles:
        {
            break;
        }
        case cBohemians:
        {
            break;
        }
        case cDravidians:
        {
            break;
        }
        case cBengalis:
        {
            break;
        }
        case cGurjaras:
        {
            break;
        }
        case cRomans:
        {
            break;
        }
        case cArmenians:
        {
            break;
        }
        case cGeorgians:
        {
            break;
        }
        case cShu:
        {
            break;
        }
        case cWu:
        {
            break;
        }
        case cWei:
        {
            break;
        }
        case cJurchens:
        {
            break;
        }
        case cKhitans:
        {
            break;
        }
        case cMuisca:
        {
            break;
        }
        case cMapuche:
        {
            break;
        }
        case cTupi:
        {
            break;
        }
        default:
            break;
    }
}


//  10002 - Disable EZS regionals
void EffectFunction10002(int playerId = -1)
{
    DisableTech(playerId, EzsWarChariotTechID);
    DisableTech(playerId, EliteEzsWarChariotTechID);
    DisableTech(playerId, EzsChariotArcherTechID);
    DisableTech(playerId, EliteEzsChariotArcherTechID);
    DisableTech(playerId, EzsScholarTechID);
}
