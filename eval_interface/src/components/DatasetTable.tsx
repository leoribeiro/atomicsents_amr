import DataUnitTable from "./DataUnitTable";
import React from "react";

import scusRealsumm from '../data/realsumm/realsumm-scus.json';
import stusRealsumm from '../data/realsumm/realsumm-stus.json';
import smusRealsumm from '../data/realsumm/realsumm-smus-sg2.json';
import accRealsumm from '../data/realsumm/realsumm-acc-sg2.json';

import scusPyrxsum from '../data/pyrxsum/pyrxsum-scus.json';
import stusPyrxsum from '../data/pyrxsum/pyrxsum-stus.json';
import smusPyrxsum from '../data/pyrxsum/pyrxsum-smus-sg2.json';
import accPyrxsum from '../data/pyrxsum/pyrxsum-acc-sg2.json';
/*
import scusTac08 from '../data/tac08/tac2008-scus.json';
import stusTac08 from '../data/tac08/tac2008-stus.json';
import smusTac08 from '../data/tac08/tac2008-smus.json';
import accTac08 from '../data/tac08/tac08-acc.json';

import scusTac09 from '../data/tac09/tac2009-scus.json';
import stusTac09 from '../data/tac09/tac2009-stus.json';
import smusTac09 from '../data/tac09/tac2009-smus.json';
import accTac09 from '../data/tac09/tac09-acc.json';*/

import {Dataset} from "./Dataset";

interface Props {
    dataset:string
    isDetailOpen: boolean
}

const DatasetTable = (props: Props)=>  {
    const {dataset, isDetailOpen} = props

    let stus: any[] =[]
    let smus: any[] = []
    let scus: any[] = []
    let acc: any[] = []

    switch (dataset) {
        case Dataset.Pyrxsum: {
            scus = scusPyrxsum;
            stus = stusPyrxsum;
            smus = smusPyrxsum;
            acc = accPyrxsum;
            break;
        }
        /*
        case Dataset.Tac08: {
            scus = scusTac08;
            stus = stusTac08;
            smus = smusTac08;
            acc = accTac08;
            break;
        }
       case Dataset.Tac09: {
           scus = scusTac09;
           stus = stusTac09;
           smus = smusTac09;
           acc = accTac09;
           break;
       }*/
        default:{
            scus = scusRealsumm;
            stus = stusRealsumm;
            smus = smusRealsumm;
            acc = accRealsumm;
            break;
        }
    }

    return (
        <div className='table-wrapper'>
            {scus.map((ex, ind) => (
                <DataUnitTable key={ex.instance_id} ex={ex} ind={ind} isDetailOpen={isDetailOpen} scus={scus} stus={stus} smus={smus} acc={acc}/>
            ))}
        </div>
    );
}

export default DatasetTable;
