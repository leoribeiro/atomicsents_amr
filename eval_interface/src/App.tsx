import React, {useState} from 'react';
import './App.css';

import DatasetTable from "./components/DatasetTable";
import {Dataset, Metric} from "./components/Enums";
import Settings from "./components/Settings";

const App = () => {
    const [isDetailOpen, setIsDetailOpen] = useState(true);
    const [choosenDataset, setChoosenDataset] = useState(Dataset.Realsumm.toString());
    const [choosenMetric, setChoosenMetric] = useState(Metric.Rouge.toString());

    return (
        <div className="App">
            <header className="header">
                <h1>Evaluation interface</h1>
            </header>
            <body>
            <Settings isDetailOpen={isDetailOpen}
                      setIsDetailOpen={setIsDetailOpen}
                      choosenDataset={choosenDataset}
                      setChoosenDataset={setChoosenDataset}
                      choosenMetric={choosenMetric}
                      setChoosenMetric={setChoosenMetric}
            />
            <DatasetTable dataset={choosenDataset} isDetailOpen={isDetailOpen} metric={choosenMetric}/>
            </body>
        </div>
    );
};

export default App;
