import React, {useState} from 'react';
import ScrollToTop from "react-scroll-to-top";
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
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
            <div className="header">
                <h1>Evaluation interface</h1>
            </div>
            <div>
            <Settings isDetailOpen={isDetailOpen}
                      setIsDetailOpen={setIsDetailOpen}
                      choosenDataset={choosenDataset}
                      setChoosenDataset={setChoosenDataset}
                      choosenMetric={choosenMetric}
                      setChoosenMetric={setChoosenMetric}
            />
            <DatasetTable dataset={choosenDataset} isDetailOpen={isDetailOpen} metric={choosenMetric}/>
            </div>
            <ScrollToTop smooth className="scroll-to-top" component={<ArrowUpwardIcon />}/>
        </div>
    );
};

export default App;
