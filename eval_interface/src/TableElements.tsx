import './TableElements.css';

interface Props {
    scus: string[]
    smus: string[]

    trees: string[]
    stus: string[]
    accSMUs: number
    accSTUs: number
    stu_pos: number[][]
    smu_pos: number[][]
}

export function TableElements(props: Props) {
    const { scus, smus, trees, stus, accSMUs, accSTUs, stu_pos, smu_pos } = props

    const max = Math.max(scus.length)//, smus.length, stus.length, trees.length)
    const output = []

    for (let i = 0; i < max; i++) {
        output.push(
            <tr key={i}>
                <td>{scus.length > i ? scus[i] : ''}</td>
                <td>{stu_pos.length > i ? stus[stu_pos[i][0]] : ''}</td>
                <td>{stu_pos.length > i ? stu_pos[i][1] : ''}</td>
                <td>{smu_pos.length > i ? smus[smu_pos[i][0]] : ''}</td>
                <td>{smu_pos.length > i ? smu_pos[i][1] : ''}</td>
                <td className="trees">{smu_pos.length > i ? trees[smu_pos[i][0]]: ''}</td>
            </tr>
        )
    }
    return (<table>
        <tr >
            <th>SCUs</th>
            <th>STUs, {Math.round(accSTUs * 1000) / 1000} Easiness</th>
            <th>STU scores</th>
            <th>SMUs, {Math.round(accSMUs * 1000) / 1000} Easiness</th>
            <th>SMU scores</th>
            <th>SMU trees</th>
        </tr>
        {output}
    </table>
    );
}