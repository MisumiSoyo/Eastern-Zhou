//  10003 - Bloodlines
void EffectFunction10003(int playerId = -1)
{
    ModAttribute(playerId, EzsFireBullID, cHitpoints, 20);
}


//  10004 - Husbandry
void EffectFunction10004(int playerId = -1)
{
    MulAttribute(playerId, EzsFireBullID, cMovementSpeed, 1.1);
}


//  10011 - Conscription
void EffectFunction10011(int playerId = -1)
{
    MulAttribute(playerId, EzsConscriptionOfficeID, cWorkRate, 1.33);
}


//  10012 - Chemistry
void EffectFunction10012(int playerId = -1)
{
    ModAttack(playerId, EzsRepeatingCrossbowCartID, cDamageClassPierce, 1);
    ModAttack(playerId, EliteEzsRepeatingCrossbowCartID, cDamageClassPierce, 1);
}


//  10013 - Siege Engineers
void EffectFunction10013(int playerId = -1)
{
    ModAttribute(playerId, EzsRepeatingCrossbowCartID, cLineOfSight, 1);
    ModAttribute(playerId, EzsRepeatingCrossbowCartID, cMaxRange, 1);
    ModAttribute(playerId, EzsRepeatingCrossbowCartID, cSearchRadius, 1);
    ModAttribute(playerId, EliteEzsRepeatingCrossbowCartID, cLineOfSight, 1);
    ModAttribute(playerId, EliteEzsRepeatingCrossbowCartID, cMaxRange, 1);
    ModAttribute(playerId, EliteEzsRepeatingCrossbowCartID, cSearchRadius, 1);

    MulAttack(playerId, EzsRepeatingCrossbowCartID, cDamageClassAllBuildings, 1.2);
    MulAttack(playerId, EliteEzsRepeatingCrossbowCartID, cDamageClassAllBuildings, 1.2);
}


//  10014 - Parthian Tactics
void EffectFunction10014(int playerId = -1)
{
    ModArmor(playerId, EzsChariotArcherID, cDamageClassMelee, -1);
    ModArmor(playerId, EliteEzsChariotArcherID, cDamageClassMelee, -1);
    ModArmor(playerId, EzsChariotArcherID, cDamageClassPierce, -2);
    ModArmor(playerId, EliteEzsChariotArcherID, cDamageClassPierce, -2);
}