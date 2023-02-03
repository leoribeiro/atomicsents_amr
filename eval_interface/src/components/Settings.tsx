import {Button, FormControl, InputLabel, MenuItem, SelectChangeEvent} from "@mui/material";
import Select from "@mui/material/Select";
import React from "react";
import {Dataset, Metric} from "./Enums";

export interface SettingsProps {
    isDetailOpen: boolean
    setIsDetailOpen: Function
    choosenDataset: string
    setChoosenDataset: Function
    choosenMetric: string
    setChoosenMetric: Function
}

const Settings = (props: SettingsProps) => {

    const {isDetailOpen, setIsDetailOpen, choosenDataset, setChoosenDataset, choosenMetric, setChoosenMetric} = props;

    const handleChangeDataset = (event: SelectChangeEvent) => {
        setChoosenDataset(event.target.value as string);
    };
    const handleChangeMetric = (event: SelectChangeEvent) => {
        setChoosenMetric(event.target.value as string);
    };
    const datasets: string[] = Object.values(Dataset);
    const metrics: string[] = Object.values(Metric);
    return (
        <div className='Settings'>
            <FormControl sx={{m: 1, minWidth: 120}} size="small" style={{margin: "0.5rem 2rem 0.5rem 0rem"}}>
                <InputLabel id="dataset-dropdown">Dataset</InputLabel>
                <Select
                    labelId="dataset-dropdown-label"
                    id="dataset-dropdown"
                    value={choosenDataset}
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
                    value={choosenMetric}
                    label="Metric"
                    onChange={handleChangeMetric}
                >
                    {metrics.map((val) =>
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
