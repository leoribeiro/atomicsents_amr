import React, {useState} from 'react';
import './App.css';

import { Button, FormControl, InputLabel, MenuItem} from "@mui/material";
import Select, {SelectChangeEvent} from '@mui/material/Select';

import DatasetTable from "./components/DatasetTable";
import {Dataset} from "./components/Dataset";

function App() {
    const [isDetailOpen, setIsDetailOpen] = useState(true);
    const [choosenDataset, setChoosenDataset] = useState(Dataset.Realsumm.toString());

    const handleChange = (event: SelectChangeEvent) => {
        setChoosenDataset(event.target.value as string);
    };
    const datasets: string[] = Object.values(Dataset);
    return (
        <div className="App">
            <header className="header">
                <h1>Evaluation interface</h1>
            </header>
            <body>
            <div className='Settings'>
                <FormControl sx={{m: 1, minWidth: 120}} size="small" style={{margin: "0rem 2rem" }}>
                    <InputLabel id="dataset-dropdown">Dataset</InputLabel>
                    <Select
                        labelId="dataset-dropdown-label"
                        id="dataset-dropdown"
                        value={choosenDataset}
                        label="Dataset"
                        onChange={handleChange}
                    >
                        {datasets.map((val) =>
                            <MenuItem value={val}>{val} </MenuItem>
                        )}

                    </Select>
                </FormControl>

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
            <DatasetTable dataset={choosenDataset} isDetailOpen={isDetailOpen}/>
            </body>
        </div>
    );
}

export default App;
