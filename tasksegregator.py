from typing import List
from taskdata import TaskData

def segregate_tasks(tasks : List[TaskData]):
    projtasks = dict()
    writertasks = dict()
    for task in tasks:
        writer = task.writer
        proj = task.project
        
        #saving to master projects map
        if(proj in projtasks):
            ts = projtasks.get(proj)
        else:
            ts = list()
        ts.append(task)
        projtasks[proj] = ts

        #saving to writer specific project map
        # writer contains projects. each project contains tasks.
        if writer in writertasks:
            writerprojs = writertasks.get(writer)
            if proj in writerprojs:
                wpts = writerprojs.get(proj)
            else:
                wpts = list()
            wpts.append(task)
            writerprojs[proj] = wpts
        else:
            wpts = list()
            wpts.append(task)
            wpmap = dict()
            wpmap[proj] = wpts
            writertasks[writer] = wpmap

    return projtasks, writertasks
