import React from "react";
import '../App.css';

interface Props {
    scus: string[]
    smus: string[]
    trees: string[]
    stus: string[]
    accSMUs: number
    accSTUs: number
    stu_pos: number[][]
    smu_pos: number[][]
    isDetailOpen: boolean
}

export function TableElements(props: Props) {
    const {scus, smus, trees, stus, accSMUs, accSTUs, stu_pos, smu_pos, isDetailOpen} = props

    const max = Math.max(scus.length)//, smus.length, stus.length, trees.length)
    const output = []

    for (let i = 0; i < max; i++) {
        output.push(
            isDetailOpen?
            <tr key={i}>
                <td>{scus.length > i ? scus[i] : ''}</td>
                <td>{stu_pos.length > i ? stus[stu_pos[i][0]] : ''}</td>
                <td>{stu_pos.length > i ? stu_pos[i][1].toFixed(3) : ''}</td>
                <td>{smu_pos.length > i ? smus[smu_pos[i][0]] : ''}</td>
                <td>{smu_pos.length > i ? smu_pos[i][1].toFixed(3) : ''}</td>
                <td className="trees">{smu_pos.length > i ? trees[smu_pos[i][0]] : ''}</td>
            </tr>
                :
                <tr key={i}>
                    <td>{scus.length > i ? scus[i] : ''}</td>
                    <td>{stu_pos.length > i ? stus[stu_pos[i][0]] : ''}</td>
                    <td>{smu_pos.length > i ? smus[smu_pos[i][0]] : ''}</td>
                </tr>
        )
    }
    return (
        isDetailOpen?
        <table>
            <tr>
                <th>SCUs</th>
                <th>STUs, {accSTUs.toFixed(3)} Easiness</th>
                <th>STU scores</th>
                <th>SMUs, {accSMUs.toFixed(3)} Easiness</th>
                <th>SMU scores</th>
                <th>SMU trees</th>
            </tr>
            {output}
        </table>
            :
            <table>
                <tr>
                    <th>SCUs</th>
                    <th>STUs, {accSTUs.toFixed(3)} Easiness</th>
                    <th>SMUs, {accSMUs.toFixed(3)} Easiness</th>
                </tr>
                {output}
            </table>
    );
}