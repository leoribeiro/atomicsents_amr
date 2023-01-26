import React, {useState} from 'react';
import './App.css';
import {TableElements} from './TableElements';
//import stus from './data/pyrxsum/pyrxsum-stus.json';
//import smus from './data/pyrxsum/pyrxsum-smus-sg2.json';
//import scus from './data/pyrxsum/pyrxsum-scus.json';
//import acc from './data/pyrxsum/pyrxsum-acc-sg2.json';
import stus from './data/realsumm/realsumm-stus.json';
import smus from './data/realsumm/realsumm-smus-sg2.json';
import scus from './data/realsumm/realsumm-scus.json';
import acc from './data/realsumm/realsumm-acc-sg2.json';

import CustomTable from "./CustomTable";


function App() {

    return (
        <div className="App">
            <header className="header">
                <div>
                    <h1>Evaluation interface</h1>
                </div>
            </header>
            <body>
            <div>
                {scus.map((ex, ind) => (
                    <CustomTable key={ex.instance_id} ex={ex} ind={ind}/>
                ))}
            </div>
            </body>
        </div>
    );
}

export default App;
