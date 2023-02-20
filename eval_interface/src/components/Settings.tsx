import {Button, FormControl, InputLabel, MenuItem, SelectChangeEvent} from "@mui/material";
import Select from "@mui/material/Select";
import React from "react";
import {Dataset, Metric, Subgraph} from "./Enums";

export interface SettingsProps {
    isDetailOpen: boolean
    setIsDetailOpen: Function
    chosenDataset: string
    setChosenDataset: Function
    chosenMetric: string
    setChosenMetric: Function
    chosenSubgraph: string
    setChosenSubgraph: Function
}

const Settings = (props: SettingsProps) => {

    const {
        isDetailOpen,
        setIsDetailOpen,
        chosenDataset,
        setChosenDataset,
        chosenMetric,
        setChosenMetric,
        chosenSubgraph,
        setChosenSubgraph
    } = props;

    const handleChangeDataset = (event: SelectChangeEvent) => {
        setChosenDataset(event.target.value as string);
    };
    const handleChangeMetric = (event: SelectChangeEvent) => {
        setChosenMetric(event.target.value as string);
    };
    const handleChangeSubgraph = (event: SelectChangeEvent) => {
        setChosenSubgraph(event.target.value as string);
    };
    const datasets: string[] = Object.values(Dataset);
    const metrics: string[] = Object.values(Metric);
    const subgraphs: string[] = Object.values(Subgraph);
    return (
        <div className='Settings'>
            <FormControl sx={{m: 1, minWidth: 120}} size="small" style={{margin: "0.5rem 2rem 0.5rem 0rem"}}>
                <InputLabel id="dataset-dropdown">Dataset</InputLabel>
                <Select
                    labelId="dataset-dropdown-label"
                    id="dataset-dropdown"
                    value={chosenDataset}
                    label="Dataset"
                    onChange={handleChangeDataset}
                >
                    {datasets.map((val) =>
                        <MenuItem key={val} value={val}>{val} </MenuItem>
                    )}

                </Select>
            </FormControl>
            <FormControl sx={{m: 1, minWidth: 120}} size="small" style={{margin: "0.5rem 2rem 0.5rem 0rem"}}>
                <InputLabel id="metric-dropdown">Evaluation Metric</InputLabel>
                <Select
                    labelId="metric-dropdown-label"
                    id="metric-dropdown"
                    value={chosenMetric}
                    label="Metric"
                    onChange={handleChangeMetric}
                >
                    {metrics.map((val) =>
                        <MenuItem key={val} value={val}>{val} </MenuItem>
                    )}

                </Select>
            </FormControl>
            <FormControl sx={{m: 1, minWidth: 120}} size="small" style={{margin: "0.5rem 2rem 0.5rem 0rem"}}>
                <InputLabel id="subgraph-dropdown">Subgraph Method</InputLabel>
                <Select
                    labelId="subgraph-dropdown-label"
                    id="subgraph-dropdown"
                    value={chosenSubgraph}
                    label="Subgraph"
                    onChange={handleChangeSubgraph}
                >
                    {subgraphs.map((val) =>
                        <MenuItem key={val} value={val}>{val} </MenuItem>
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
    );
};

export default Settings;
