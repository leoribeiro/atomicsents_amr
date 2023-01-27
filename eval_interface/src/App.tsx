import React, {useState} from 'react';
import './App.css';
//import stus from './data/pyrxsum/pyrxsum-stus.json';
//import smus from './data/pyrxsum/pyrxsum-smus-sg2.json';
//import scus from './data/pyrxsum/pyrxsum-scus.json';
//import acc from './data/pyrxsum/pyrxsum-acc-sg2.json';
import stus from './data/realsumm/realsumm-stus.json';
import smus from './data/realsumm/realsumm-smus-sg2.json';
import scus from './data/realsumm/realsumm-scus.json';
import acc from './data/realsumm/realsumm-acc-sg2.json';


import CustomTable from "./CustomTable";
import {Button} from "@mui/material";

function App() {
    const [isDetailOpen, setIsDetailOpen] = useState(true);

    return (
        <div className="App">
            <header className="header">
                <h1>Evaluation interface</h1>
            </header>
            <body>
            <div className='Settings'>
                <Button variant="contained"
                        aria-label="collapse"
                        onClick={() => setIsDetailOpen(!isDetailOpen)}
                        className='Button'
                        style={{
                            borderRadius: 10,
                            backgroundColor: "#488ab6",
                        }}
                >
                    {isDetailOpen ? <h4>Hide details</h4> : <h4>Show details</h4>}
                </Button>
            </div>
            <div>
                {scus.map((ex, ind) => (
                    <CustomTable key={ex.instance_id} ex={ex} ind={ind} isDetailOpen={isDetailOpen}/>
                ))}
            </div>
            </body>
        </div>
    );
}

export default App;
