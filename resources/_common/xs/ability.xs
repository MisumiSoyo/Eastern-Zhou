include "units.xs";


void NoDropsiteLumberjackApplier(int playerId = -1, int ObjectID = -1)
{
    for(taskId = 0; < xsGetObjectTaskCount(ObjectID, playerId))
    {
        xsObjectTaskAmount(ObjectID, playerId, taskId);
        int taskType = xsGetTaskAmount(cTaskAttrTaskType);
        if  (taskType == cTaskTypeHunt)
        {
            xsTaskAmount(cTaskAttrCombatLevelFlag, 1);
            xsModifyObjectTasks(ObjectID, playerId, taskId, true);
        }
    }
}