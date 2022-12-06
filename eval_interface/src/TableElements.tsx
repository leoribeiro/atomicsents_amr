interface Props {
    scus: string[]
    smus: string[]
    stus: string[]
    accSMUs: number
    accSTUs: number
}

export function TableElements(props: Props) {
    const { scus, smus, stus, accSMUs, accSTUs } = props

    const max = Math.max(scus.length, smus.length, stus.length)
    const output = []

    for (let i = 0; i < max; i++) {
        output.push(
            <tr>
                <td>{scus.length > i ? scus[i] : ''}</td>
                <td>{stus.length > i ? stus[i] : ''}</td>
                <td>{smus.length > i ? smus[i] : ''}</td>
            </tr>
        )
    }
    return (<table>
        <tr>
            <th>SCUs</th>
            <th>STUs, {Math.round(accSTUs * 1000) / 1000} Easiness</th>
            <th>SMUs, {Math.round(accSMUs * 1000) / 1000} Easiness</th>
        </tr>
        {output}
    </table>
    );
}